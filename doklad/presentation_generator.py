from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from datetime import datetime

def create_presentation():
    """Создание презентации на 10 слайдов для защиты школьного проекта."""
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Слайд 1: Титульный
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Заголовок
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(2.0), Inches(12), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Мультимодальная диспетчерская система управления беспилотным транспортом"
    p.font.size = Pt(36)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    
    # Подзаголовок
    subtitle_box = slide.shapes.add_textbox(Inches(0.7), Inches(3.2), Inches(12), Inches(0.8))
    tf = subtitle_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Школьный проект"
    p.font.size = Pt(24)
    p.alignment = PP_ALIGN.CENTER
    
    # Дата и автор
    footer_box = slide.shapes.add_textbox(Inches(0.7), Inches(6.2), Inches(12), Inches(0.6))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Версия 1.0 | Октябрь 2026"
    p.font.size = Pt(14)
    p.alignment = PP_ALIGN.CENTER
    
    # Слайд 2: Актуальность проекта
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Актуальность проекта"
    p.font.size = Pt(36)
    p.font.bold = True
    
    content_left = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(5.5), Inches(4.5))
    tf = content_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """Рост количества автономных транспортных средств в городских условиях:
• Тротуарные роверы для доставки заказов
• Беспилотные автомобили
• Воздушные дроны служб доставки
• Водные беспилотные суда

Проблема: без единого координатора возможны столкновения, взаимные блокировки, нарушение запретных зон."""
    p.font.size = Pt(20)
    
    content_right = slide.shapes.add_textbox(Inches(6.7), Inches(1.8), Inches(5.5), Inches(4.5))
    tf = content_right.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """Целевая функция клиента:
min V(x)/C(x)

при условиях:
T(x) ≤ Tmax
C(x) ≤ Cmax

где V — скорость доставки, C — стоимость, T — время"""
    p.font.size = Pt(18)
    
    # Слайд 3: Почему не хватает существующих правил ПДД
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Почему существующих правил ПДД недостаточно"
    p.font.size = Pt(36)
    p.font.bold = True
    
    content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(11.6), Inches(4.5))
    tf = content_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """1. ПДД распространяются только на наземный транспорт
2. Ширина тротуаров не всегда позволяет движение АТС без помех пешеходам
3. Законы об АТС находятся на стадии разработки
4. Штат ГАИ рассчитан для обычного транспорта, не покрывает рост АТС
5. ДТП на тротуарах с моторизированной техникой растут
6. АТС не умеют интерпретировать сигналы регулировщика автоматически
7. Рост риска незаконного использования АТС требует оперативного контроля"""
    p.font.size = Pt(18)
    
    # Слайд 4: Основные задачи МДС
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Основные задачи МДС"
    p.font.size = Pt(36)
    p.font.bold = True
    
    content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(11.6), Inches(4.5))
    tf = content_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """1. СНИЖЕНИЕ СРОКОВ ДОСТАВКИ — выбор оптимального маршрута с учётом ситуации
2. БЕЗОПАСНОСТЬ — не допускать столкновений и появления в запретных зонах
3. ПОВЫШЕНИЕ ЭФФЕКТИВНОСТИ — распределение маршрутов без перегрузки коридоров
4. КОНТРОЛЛИРУЕМОСТЬ — актуальная информация о загруженности дорог для городских служб
5. ОБРАТНАЯ СВЯЗЬ ОПЕРАТОРУ — возможность менять маршруты с учётом ремонтов, мелей, закрытых зон"""
    p.font.size = Pt(20)
    
    # Слайд 5: Четыре типа АТС и препятствия
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Четыре типа АТС и транспортные среды"
    p.font.size = Pt(36)
    p.font.bold = True
    
    content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(11.6), Inches(4.5))
    tf = content_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """| Тип АТС | Транспортная среда | Типовые препятствия |
|---------|-------------------|---------------------|
| Ровер | Тротуары | Лестницы, узкие проходы, скопления людей |
| Автомобиль | Дороги | Перекопы, светофоры, закрытые полосы |
| Дрон | Воздух | Запретные зоны, эшелоны высот |
| Катер | Вода | Шлюзы, разводные мосты, мели, осадка"""
    p.font.size = Pt(20)
    
    # Слайд 6: Как работает МДС — цикл диспетчеризации
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Цикл диспетчеризации МДС"
    p.font.size = Pt(36)
    p.font.bold = True
    
    content_left = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(5.5), Inches(4.5))
    tf = content_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """Цикл работы МДС:

Оператор АТС → Заявка в МДС → Проверка → Согласование → Движение АТС → Телеметрия от АТС → Актуализация"""
    p.font.size = Pt(20)
    
    content_right = slide.shapes.add_textbox(Inches(6.7), Inches(1.8), Inches(5.5), Inches(4.5))
    tf = content_right.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """Ключевые этапы:
1. Оператор подаёт заявку (точки, маршрут, тип транспорта)
2. МДС проверяет конфликты и препятствия
3. Решение: согласовано / с изменениями / отклонено
4. Маршрут вносится в карту занятости
5. Оператор отправляет телеметрию (позиция, статус, ETA)
6. МДС актуализирует информацию и корректирует маршруты"""
    p.font.size = Pt(18)
    
    # Слайд 7: Архитектура системы
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Архитектура системы"
    p.font.size = Pt(36)
    p.font.bold = True
    
    content_left = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(5.5), Inches(4.5))
    tf = content_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """Компоненты МДС:
• CityMap — карта препятствий (лестницы, шлюзы, запретные зоны)
• Dispatcher — ядро системы (приём заявок, проверка, согласование)
• OccupancyMap — карта занятости маршрутов по времени
• Detector — детект отклонений от плана
• Validator — валидация телеметрии клиентов
• Visualizer — визуализация карты и метрик"""
    p.font.size = Pt(18)
    
    content_right = slide.shapes.add_textbox(Inches(6.7), Inches(1.8), Inches(5.5), Inches(4.5))
    tf = content_right.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """Единая карта занятости — четыре слоя:
• sidewalk — тротуарные роверы
• road — беспилотные автомобили
• air — воздушные дроны
• water — водные катера

Каждый слой независим, но координируется в точках пересечения"""
    p.font.size = Pt(18)
    
    # Слайд 8: Структуры данных и форматы
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Формат телеметрии"
    p.font.size = Pt(36)
    p.font.bold = True
    
    content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(11.6), Inches(4.5))
    tf = content_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """JSON-формат телеметрии:

{
  \"client_id\": \"pizza_shop_01\",
  \"batch_id\": \"batch-001\",
  \"vehicles\": [{
    \"vehicle_id\": \"rover_007\",
    \"route_id\": \"R-001\",
    \"position\": {\"x\": 12.5, \"y\": 34.2},
    \"status\": \"moving\",
    \"progress\": 0.35,
    \"eta\": \"2025-06-01T14:12:00Z\",
    \"alerts\": []
  }]
}

МДС валидирует структуру, проверяет принадлежность маршрута клиенту и актуальность данных."""
    p.font.size = Pt(17)
    
    # Слайд 9: Технологии и масштабируемость
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Технологии и масштабируемость"
    p.font.size = Pt(36)
    p.font.bold = True
    
    content_left = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(5.5), Inches(4.5))
    tf = content_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """Используемые технологии:
• Python 3.10+
• Flask — веб-сервер API
• Pydantic — валидация данных
• Shapely — геометрические операции
• networkx — графы маршрутов
• matplotlib — визуализация
• WebSocket — реальное время"""
    p.font.size = Pt(18)
    
    content_right = slide.shapes.add_textbox(Inches(6.7), Inches(1.8), Inches(5.5), Inches(4.5))
    tf = content_right.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """Принцип масштабируемости:
"Новый тип транспорта = новый модуль проверки, ядро не меняется"

Архитектура растёт линейно — сложность добавляется только в отдельные модули"""
    p.font.size = Pt(18)
    
    # Слайд 10: Выводы и перспективы
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Выводы и перспективы развития"
    p.font.size = Pt(36)
    p.font.bold = True
    
    content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(11.6), Inches(4.5))
    tf = content_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = """Выводы:
✓ МДС — арбитр, а не пилот (проверка и согласование маршрутов)
✓ Каждый согласованный маршрут влияет на следующие через карту занятости
✓ Телеметрия замыкает контур диспетчеризации
✓ Система масштабируема для новых типов транспорта

Перспективы развития:
• Динамика в реальном времени (pygame-анимация движения АТС)
• Приоритет срочных доставок (медикаменты)
• Пересмотр маршрутов при новых препятствиях
• Машинное обучение для прогнозирования загруженности
• Веб-интерфейс для клиентов"""
    p.font.size = Pt(19)
    
    # Сохранение презентации
    prs.save("presentation_mds.pptx")
    return "presentation_mds.pptx"

if __name__ == "__main__":
    file_path = create_presentation()
    print(f"Презентация создана: {file_path}")
