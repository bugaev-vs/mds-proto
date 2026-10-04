# gantt.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

from visualize import COLORS


def draw_gantt(dispatcher):
    """
    Диаграмма Ганта: горизонтальные полосы по времени для каждого
    согласованного маршрута, окрашенные по типу транспорта.
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    routes = dispatcher.approved
    if not routes:
        ax.text(0.5, 0.5, "Нет согласованных маршрутов",
                ha='center', va='center', fontsize=14)
        ax.set_title("График согласованных маршрутов (Gantt)",
                     fontweight='bold')
        plt.tight_layout()
        plt.savefig("gantt.png", dpi=150)
        plt.show()
        return

    for i, route in enumerate(routes):
        start = mdates.date2num(route.time_window[0])
        end = mdates.date2num(route.time_window[1])
        color = COLORS[route.transport_type.value]

        ax.barh(i, end - start, left=start, height=0.6,
                color=color, alpha=0.75, edgecolor='black')
        ax.text(start + 0.0005, i, f"{route.route_id}",
                va='center', fontsize=9, color='white', fontweight='bold')

    ax.set_yticks(range(len(routes)))
    ax.set_yticklabels([r.transport_type.value for r in routes])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlabel("Время")
    ax.set_title("График согласованных маршрутов (Gantt)",
                 fontweight='bold')
    ax.grid(True, axis='x', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig("gantt.png", dpi=150)
    plt.show()
