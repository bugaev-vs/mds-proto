# visualize.py
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Circle
from shapely.geometry import Polygon as ShpPolygon

COLORS = {
    "sidewalk_rover": "#2ecc71",   # зелёный
    "autonomous_car": "#3498db",   # синий
    "aerial_drone":   "#e74c3c",   # красный
    "water_vessel":   "#9b59b6",   # фиолетовый
}

def draw_city(city_map, dispatcher, figsize=(14, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    
    # 1. Препятствия
    for obs in city_map.obstacles:
        geom = obs.geometry
        color = {
            "full_block": "black",
            "slowdown": "orange",
            "restriction": "gray"
        }.get(obs.severity, "gray")
        
        if isinstance(geom, ShpPolygon):
            xs, ys = geom.exterior.xy
            ax.fill(xs, ys, alpha=0.3, color=color, label=obs.obstacle_id)
            ax.plot(xs, ys, color=color, linewidth=1.5)
        else:
            # Point.buffer → Polygon
            xs, ys = geom.exterior.xy
            ax.fill(xs, ys, alpha=0.3, color=color)
    
    # 2. Согласованные маршруты
    for route in dispatcher.approved:
        xs = [wp.x for wp in route.waypoints]
        ys = [wp.y for wp in route.waypoints]
        color = COLORS[route.transport_type.value]
        ax.plot(xs, ys, color=color, linewidth=2.5,
                marker='o', markersize=6,
                label=f"{route.route_id} ({route.transport_type.value})")
    
    # 3. Легенда и оформление
    handles, labels = ax.get_legend_handles_labels()
    seen = set()
    uniq = [(h, l) for h, l in zip(handles, labels) if not (l in seen or seen.add(l))]
    ax.legend(*zip(*uniq), loc="upper left", fontsize=9)
    
    ax.set_title("Мультимодальная диспетчерская: карта города",
                 fontsize=14, fontweight='bold')
    ax.set_xlabel("X (условные единицы)")
    ax.set_ylabel("Y (условные единицы)")
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig("city_map.png", dpi=150)
    plt.show()
