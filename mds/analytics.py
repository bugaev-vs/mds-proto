# analytics.py
import matplotlib.pyplot as plt
from collections import Counter

from visualize import COLORS


def draw_load_analytics(dispatcher):
    """
    Два графика:
    1. Круговая — распределение согласованных маршрутов по типам транспорта.
    2. Столбчатая — распределение заявок по статусам (approved / ... / rejected).
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # --- 1. Круговая: по типам транспорта ---
    types = [r.transport_type.value for r in dispatcher.approved]
    counts = Counter(types)

    if counts:
        ax1.pie(
            counts.values(),
            labels=list(counts.keys()),
            autopct='%1.0f%%',
            colors=[COLORS[k] for k in counts.keys()],
            startangle=90,
        )
    else:
        ax1.text(0.5, 0.5, "Нет данных", ha='center', va='center')
    ax1.set_title("Согласованные маршруты по типам транспорта",
                  fontweight='bold')

    # --- 2. Столбчатая: по статусам ---
    statuses = Counter(r.status.value for r in dispatcher.requests.values())
    status_colors = {
        "approved": "#2ecc71",
        "approved_with_changes": "#f39c12",
        "rejected": "#e74c3c",
        "pending": "#95a5a6",
    }

    if statuses:
        keys = list(statuses.keys())
        ax2.bar(
            keys,
            [statuses[k] for k in keys],
            color=[status_colors.get(k, "#95a5a6") for k in keys],
        )
        for i, k in enumerate(keys):
            ax2.text(i, statuses[k] + 0.05, str(statuses[k]),
                     ha='center', fontweight='bold')

    ax2.set_title("Распределение заявок по статусам", fontweight='bold')
    ax2.set_ylabel("Количество")

    plt.tight_layout()
    plt.savefig("analytics.png", dpi=150)
    plt.show()
