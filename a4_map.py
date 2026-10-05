from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode
from io import BytesIO
from reportlab.lib.utils import ImageReader
import os

# --- Шрифт с кириллицей ---
FONT_PATHS = [
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_NAME = "Helvetica"
for p in FONT_PATHS:
    if os.path.exists(p):
        pdfmetrics.registerFont(TTFont("Cyr", p))
        FONT_NAME = "Cyr"
        break

# --- Параметры поля ---
CELL = 50 * mm
COLS = 20
ROWS = 20

# --- Параметры листа А4 ---
PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
CUT_PAD = 3 * mm

CELLS_X = int((PAGE_W - 2 * MARGIN) // CELL)  # 3
CELLS_Y = int((PAGE_H - 2 * MARGIN) // CELL)  # 5

sheets_x = -(-COLS // CELLS_X)  # 7
sheets_y = -(-ROWS // CELLS_Y)  # 4

def cell_name(col, row):
    letters = "ABCDEFGHIJKLMNOPQRST"
    return f"{letters[row]}{col + 1}"

def make_qr_image(text):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("1")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)

def draw_cross(c, x, y, size=3 * mm, width=0.8):
    c.setLineWidth(width)
    c.setStrokeColorRGB(0, 0, 0)
    c.line(x - size, y, x + size, y)
    c.line(x, y - size, x, y + size)

c = canvas.Canvas("field_1m_bw.pdf", pagesize=A4)

for sy in range(sheets_y):
    for sx in range(sheets_x):
        c.setPageSize(A4)
        
        cols_here = min(CELLS_X, COLS - sx * CELLS_X)
        rows_here = min(CELLS_Y, ROWS - sy * CELLS_Y)
        
        GRID_LEFT   = MARGIN
        GRID_TOP    = PAGE_H - MARGIN
        grid_right  = GRID_LEFT + cols_here * CELL
        grid_bottom = GRID_TOP - rows_here * CELL
        
        # --- 1. QR-коды ---
        for iy in range(rows_here):
            for ix in range(cols_here):
                col = sx * CELLS_X + ix
                row = sy * CELLS_Y + iy
                x = GRID_LEFT + ix * CELL
                y = GRID_TOP - (iy + 1) * CELL
                qr_img = make_qr_image(cell_name(col, row))
                c.drawImage(qr_img, x, y, width=CELL, height=CELL)
        
        # --- 2. Линии сетки ---
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.4)
        for ix in range(cols_here + 1):
            x = GRID_LEFT + ix * CELL
            c.line(x, grid_bottom, x, GRID_TOP)
        for iy in range(rows_here + 1):
            y = GRID_TOP - iy * CELL
            c.line(GRID_LEFT, y, grid_right, y)
        
        # --- 3. Реперные крестики в углах сетки ---
        draw_cross(c, GRID_LEFT,  GRID_TOP)
        draw_cross(c, grid_right, GRID_TOP)
        draw_cross(c, GRID_LEFT,  grid_bottom)
        draw_cross(c, grid_right, grid_bottom)
        
        # --- 4. Линии обрезки — только на внутренних стыках ---
        c.setLineWidth(1.0)
        c.setDash(4, 3)
        c.setStrokeColorRGB(0, 0, 0)
        
        # Есть ли сосед слева / справа / сверху / снизу
        has_left   = sx > 0
        has_right  = sx < sheets_x - 1 and cols_here == CELLS_X
        has_top    = sy > 0
        has_bottom = sy < sheets_y - 1 and rows_here == CELLS_Y
        
        # Левая сторона: режем, если есть сосед слева
        if has_left:
            x = GRID_LEFT - CUT_PAD
            c.line(x, grid_bottom - CUT_PAD, x, GRID_TOP + CUT_PAD)
        
        # Правая сторона
        if has_right:
            x = grid_right + CUT_PAD
            c.line(x, grid_bottom - CUT_PAD, x, GRID_TOP + CUT_PAD)
        
        # Верхняя сторона
        if has_top:
            y = GRID_TOP + CUT_PAD
            c.line(GRID_LEFT - CUT_PAD, y, grid_right + CUT_PAD, y)
        
        # Нижняя сторона
        if has_bottom:
            y = grid_bottom - CUT_PAD
            c.line(GRID_LEFT - CUT_PAD, y, grid_right + CUT_PAD, y)
        
        # Уголки-засечки на пересечении разрезов (чтобы было видно, где остановиться)
        # Рисуем короткие штрихи у краёв разреза
        c.setDash()
        
        # --- 5. Только подписи осей ---
        c.setFillColorRGB(0, 0, 0)
        c.setFont(FONT_NAME, 16)
        
        # Буквы строк — слева и справа
        for iy in range(rows_here):
            row = sy * CELLS_Y + iy
            letter = "ABCDEFGHIJKLMNOPQRST"[row]
            y_center = GRID_TOP - iy * CELL - CELL / 2 - 6
            c.drawRightString(GRID_LEFT - 5 * mm, y_center, letter)
            c.drawString(grid_right + 5 * mm, y_center, letter)
        
        # Цифры столбцов — сверху и снизу
        for ix in range(cols_here):
            col = sx * CELLS_X + ix
            number = str(col + 1)
            x_center = GRID_LEFT + ix * CELL + CELL / 2
            c.drawCentredString(x_center, GRID_TOP + 6 * mm, number)
            c.drawCentredString(x_center, grid_bottom - 12 * mm, number)
        
        c.showPage()

c.save()
print("Готово: field_1m_bw.pdf")