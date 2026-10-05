import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

# ============ НАСТРОЙКИ ============
INPUT_DIR   = Path(r".\interviews")
PATTERN     = "int_*"
EXTENSIONS  = {".txt"}
SAMPLE_RATE = 48000
MAX_CHARS   = 800
PAUSE_SEC   = 0.35
OVERWRITE   = True

MP3_BITRATE  = "128k"
MP3_CHANNELS = 1
KEEP_WAV     = False

# --- Шум ---
NOISE_FILE    = Path(r".\interviews\noise_1.wav")
NOISE_SNR_DB  = 12.0
NOISE_GAIN_DB = -3.0

ALL_VOICES = ["aidar", "baya", "kseniya", "xenia", "eugene"]

ROLE_ALIASES = {
    "ведущий": "kseniya",
    "гость":   "aidar",
}
DEFAULT_VOICE = "kseniya"
# ===================================

ROLE_RE = re.compile(r"^\s*([А-Яа-яЁёA-Za-z]+)\s*:\s*(.*)$")


def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    sentences = re.split(r"(?<=[.!?…])\s+", text.strip())
    chunks, current = [], ""
    for s in sentences:
        if not s:
            continue
        if len(current) + len(s) + 1 <= max_chars:
            current = f"{current} {s}".strip()
        else:
            if current:
                chunks.append(current)
            while len(s) > max_chars:
                cut = s.rfind(" ", 0, max_chars)
                if cut == -1:
                    cut = max_chars
                chunks.append(s[:cut].strip())
                s = s[cut:].strip()
            current = s
    if current:
        chunks.append(current)
    return chunks


def resolve_voice(prefix: str) -> str | None:
    key = prefix.lower()
    if key in ALL_VOICES:
        return key
    if key in ROLE_ALIASES:
        return ROLE_ALIASES[key]
    return None


def parse_lines(text: str) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        voice = DEFAULT_VOICE
        m = ROLE_RE.match(line)
        if m:
            resolved = resolve_voice(m.group(1))
            if resolved is not None:
                voice = resolved
                line = m.group(2).strip()
        if not line:
            continue
        for chunk in split_text(line):
            result.append((voice, chunk))
    return result


def find_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        raise SystemExit("ffmpeg не найден в PATH.")
    return exe


def wav_to_mp3(wav_path: Path, mp3_path: Path) -> None:
    ffmpeg = find_ffmpeg()
    cmd = [
        ffmpeg, "-y",
        "-i", str(wav_path),
        "-ac", str(MP3_CHANNELS),
        "-b:a", MP3_BITRATE,
        "-codec:a", "libmp3lame",
        str(mp3_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def mix_noise_ffmpeg(speech_wav: Path, noise_path: Path, out_wav: Path) -> None:
    """Зацикливает шум на всю длину речи и подмешивает по SNR."""
    ffmpeg = find_ffmpeg()

    def rms_db(path: Path) -> float:
        cmd = [
            ffmpeg, "-hide_banner", "-i", str(path),
            "-af", "astats=metadata=1:reset=0",
            "-f", "null", "-",
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        m = re.search(r"Overall.*?RMS level dB:\s*(-?\d+(?:\.\d+)?)", res.stderr, re.S)
        if not m:
            m = re.search(r"RMS level dB:\s*(-?\d+(?:\.\d+)?)", res.stderr)
        return float(m.group(1)) if m else -20.0

    speech_rms = rms_db(speech_wav)
    noise_rms  = rms_db(noise_path)
    noise_gain_db = speech_rms - noise_rms - NOISE_SNR_DB + NOISE_GAIN_DB

    # aloop=-1: бесконечно; atrim=0:speech_dur — обрезаем по длине речи
    cmd = [
        ffmpeg, "-y",
        "-i", str(speech_wav),
        "-i", str(noise_path),
        "-filter_complex",
        (
            f"[0:a]apad=whole_dur=999999[sp];"
            f"[1:a]aloop=loop=-1:size=2e9,volume={noise_gain_db:.2f}dB[noise];"
            f"[sp][noise]amix=inputs=2:duration=first:normalize=0[out]"
        ),
        "-map", "[out]",
        "-ar", str(SAMPLE_RATE),
        "-ac", "1",
        str(out_wav),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def tts_file(model, src: Path, dst_mp3: Path) -> None:
    text = src.read_text(encoding="utf-8")
    items = parse_lines(text)
    if not items:
        print(f"  ⚠ нет текста, пропуск: {src.name}")
        return

    print(f"  {len(items)} фрагмент(ов)")
    pause = np.zeros(int(SAMPLE_RATE * PAUSE_SEC), dtype=np.float32)
    parts: list[np.ndarray] = []

    for i, (voice, chunk) in enumerate(items, 1):
        preview = chunk[:60].replace("\n", " ")
        print(f"  [{i}/{len(items)}] ({voice}) {preview}...")
        audio = model.apply_tts(
            text=chunk,
            speaker=voice,
            sample_rate=SAMPLE_RATE,
            put_accent=True,
            put_yo=True,
            put_stress_homo=True,
            put_yo_homo=True,
        )
        if torch.is_tensor(audio):
            audio = audio.cpu().numpy()
        parts.append(audio.astype(np.float32))
        parts.append(pause)

    full = np.concatenate(parts)

    noise = NOISE_FILE if (NOISE_FILE and NOISE_FILE.is_file()) else None
    if noise:
        print(f"  + шум: {noise.name} (SNR ≈ {NOISE_SNR_DB} дБ, циклично)")
    else:
        if NOISE_FILE:
            print(f"  · шум не найден: {NOISE_FILE} — синтез без шума")
        else:
            print("  · шум не задан — синтез без шума")

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = Path(tmpdir) / (src.stem + ".wav")
        sf.write(wav_path, full, SAMPLE_RATE)

        if noise:
            mixed = Path(tmpdir) / (src.stem + "_noisy.wav")
            mix_noise_ffmpeg(wav_path, noise, mixed)
            final_wav = mixed
        else:
            final_wav = wav_path

        wav_to_mp3(final_wav, dst_mp3)

        if KEEP_WAV:
            shutil.copy2(final_wav, dst_mp3.with_suffix(".wav"))

    dur = len(full) / SAMPLE_RATE
    size_kb = dst_mp3.stat().st_size / 1024
    print(f"  ✓ {dst_mp3.name}  ({dur:.1f} сек, {size_kb:.0f} КБ)")


def main() -> None:
    if not INPUT_DIR.is_dir():
        raise SystemExit(f"Папка не найдена: {INPUT_DIR}")

    files = sorted(
        p for p in INPUT_DIR.glob(PATTERN)
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    )
    if not files:
        print(f"Файлы '{PATTERN}' не найдены в {INPUT_DIR}")
        return

    print(f"Найдено файлов: {len(files)}")
    for p in files:
        print(f"  • {p.name}")

    find_ffmpeg()

    print("\nЗагружаю модель Silero...")
    device = torch.device("cpu")
    model, _ = torch.hub.load(
        repo_or_dir="snakers4/silero-models",
        model="silero_tts",
        language="ru",
        speaker="v5_ru",
        trust_repo=True,
    )
    model.to(device)
    print("Модель готова.\n")

    for src in files:
        dst = src.with_suffix(".mp3")
        print(f"→ {src.name}  →  {dst.name}")
        if dst.exists() and not OVERWRITE:
            print("  ⏭ уже существует, пропуск")
            continue
        try:
            tts_file(model, src, dst)
        except Exception as e:
            print(f"  ✗ Ошибка: {e}")
        print()


if __name__ == "__main__":
    main()