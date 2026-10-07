from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RgbColor
from datetime import datetime
import xml.etree.ElementTree as ET
import zipfile
import os

def create_odp_presentation():
    """Создание профессиональной ODP презентации с шаблонным дизайном."""
    
    # Создаем PPTX файл (превратим его в ODP)
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # A4 формат для ODP
    prs.slide_height = Inches(7.5)
    
    # Палитра цветов проекта МДС
    COLORS = {
        'primary_blue': (0, 51, 102),      # Глубокий синий - основной
        'light_blue': (0, 102, 153),       # Светло-синий - акцентный
        'dark_gray': (64, 64, 64),         # Тёмно-серый - текст
        'light_gray': (200, 200, 200),     # Светло-серый - фон элементов
        'white': (255, 255, 255),          # Белый
    }
    
    # Шрифты для заголовков и текста
    HEADERS_FONT = 'Calibri Light'
    BODY_FONT = 'Calibri'
    
    # Создаем слайды
    
    # ====== СЛАЙД 1: ТИТУЛЬНЫЙ ======
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)
    
    # Фоновый градиент (симуляция через заполнение)
    bg_shape = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)  # msoBackground
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['primary_blue'])
    bg_shape.line.fill.background()
    
    # Титульный текст по центру
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.7), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Мультимодальная диспетчерская система управления беспилотным транспортом"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.alignment = PP_ALIGN.CENTER
    p.fill.fore_color.rgb = RgbColor(COLORS['white'][0], COLORS['white'][1], COLORS['white'][2])
    
    # Подзаголовок
    subtitle_box = slide.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(11.7), Inches(1))
    tf = subtitle_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Школьный проект"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.alignment = PP_ALIGN.CENTER
    
    # Дополнительные данные
    info_box = slide.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.2))
    tf = info_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Версия 1.0 | Октябрь 2026"
    p.font.size = Pt(16)
    p.font.name = BODY_FONT
    p.alignment = PP_ALIGN.CENTER
    
    # Декоративные элементы - круги по бокам
    left_circle = slide.shapes.add_shape(5, Inches(0.4), Inches(4.5), Inches(2.8), Inches(3))  # oval
    left_circle.fill.solid()
    left_circle.fill.fore_color.rgb = RgbColor(*COLORS['light_blue'])
    
    right_circle = slide.shapes.add_shape(5, Inches(10.1), Inches(4.5), Inches(2.8), Inches(3))
    right_circle.fill.solid()
    right_circle.fill.fore_color.rgb = RgbColor(*COLORS['light_blue'])
    
    # Декоративные круги поменьше сверху
    top_left = slide.shapes.add_shape(5, Inches(0.6), Inches(0.8), Inches(3), Inches(1.5))
    top_left.fill.solid()
    top_left.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    top_left.fill.transparency = 0.9
    
    top_right = slide.shapes.add_shape(5, Inches(9.7), Inches(0.8), Inches(3), Inches(1.5))
    top_right.fill.solid()
    top_right.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    top_right.fill.transparency = 0.9
    
    # Номер слайда (видимый в превью)
    slide_number_box = slide.shapes.add_textbox(Inches(11.3), Inches(6.8), Inches(2), Inches(0.6))
    tf = slide_number_box.text_frame
    p = tf.paragraphs[0]
    p.text = "1 / 10"
    p.font.size = Pt(14)
    p.font.bold = True
    p.alignment = PP_ALIGN.RIGHT
    
    # ====== СЛАЙД 2: АКТУАЛЬНОСТЬ ======
    slide = prs.slides.add_slide(slide_layout)
    
    # Фон - градиент от синего к светлому
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['primary_blue'])
    
    # Заголовок с номером
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Актуальность проекта"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    # Декоративный номер слайда
    slide_num_label = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.3))
    tf = slide_num_label.text_frame
    p = tf.paragraphs[0]
    p.text = "2"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = RgbColor(*COLORS['white'])
    p.alignment = PP_ALIGN.CENTER
    
    # Контент - две колонки с иконками (квадраты в качестве замены)
    left_col = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.2), Inches(4.5))
    tf = left_col.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.name = HEADERS_FONT
    p1.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    p1.text = "Рост количества АТС:"
    
    # Список элементов
    items = [
        "• Тротуарные роверы — доставка заказов из интернет-магазинов",
        "• Беспилотные автомобили — городские перевозки",
        "• Воздушные дроны — служб доставки, транспортные компании",
        "• Водные беспилотные суда — логистика по рекам и каналам"
    ]
    
    for item in items:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(16)
        p.font.name = BODY_FONT
        
    right_col = slide.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.2), Inches(4.5))
    tf = right_col.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.name = HEADERS_FONT
    p1.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    p1.text = "Проблема без диспетчеризации:"
    
    problem_items = [
        "• Столкновения между автономными транспортными средствами",
        "• Взаимные блокировки маршрутов",
        "• Нарушение запретных зон полёта и движения",
        "• Рост нагрузки на существующую дорожную инфраструктуру"
    ]
    
    for item in problem_items:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(16)
        p.font.name = BODY_FONT
        
    # ====== СЛАЙД 3: ПРОБЛЕМА ПДД ======
    slide = prs.slides.add_slide(slide_layout)
    
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['primary_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Почему правил ПДД недостаточно"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    # Номер слайда
    slide_num_label = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.3))
    tf = slide_num_label.text_frame
    p = tf.paragraphs[0]
    p.text = "3"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = RgbColor(*COLORS['white'])
    
    # 7 пунктов в две колонки
    col1 = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.2), Inches(3.9))
    tf = col1.text_frame
    p = tf.paragraphs[0]
    p.font.size = Pt(17)
    p.font.name = BODY_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    points1 = [
        "Правила дорожного движения распространяются только на наземный транспорт",
        "Ширина тротуаров не всегда позволяет движение АТС без помех пешеходам",
        "Законы и нормативные акты об АТС находятся на стадии разработки"
    ]
    for i, pt in enumerate(points1):
        if i == 0:
            tf.add_paragraph().text = pt
        else:
            tf.add_paragraph().text = f"• {pt}"
    
    col2 = slide.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.2), Inches(3.9))
    tf = col2.text_frame
    p = tf.paragraphs[0]
    p.font.size = Pt(17)
    p.font.name = BODY_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    points2 = [
        "Штат ГАИ рассчитан для обычного транспорта, не покрывает рост АТС",
        "ДТП на тротуарах с моторизированной техникой растут",
        "АТС не способны автоматически интерпретировать сигналы регулировщика"
    ]
    for i, pt in enumerate(points2):
        if i == 0:
            tf.add_paragraph().text = pt
        else:
            tf.add_paragraph().text = f"• {pt}"
    
    # ====== СЛАЙД 4: ЗАДАЧИ МДС ======
    slide = prs.slides.add_slide(slide_layout)
    
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['light_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Основные задачи МДС"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    # Номер слайда
    slide_num_label = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.3))
    tf = slide_num_label.text_frame
    p = tf.paragraphs[0]
    p.text = "4"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = RgbColor(*COLORS['white'])
    
    # 5 задач с иконками-квадратами
    tasks_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.2))
    tf = tasks_box.text_frame
    tf.word_wrap = True
    
    task_items = [
        ("СНИЖЕНИЕ СРОКОВ ДОСТАВКИ", "• Выбор оптимального маршрута с учётом ситуации"),
        ("БЕЗОПАСНОСТЬ", "• Недопущение столкновений и появления в запретных зонах"),
        ("ПОВЫШЕНИЕ ЭФФЕКТИВНОСТИ", "• Распределение маршрутов без перегрузки коридоров"),
        ("КОНТРОЛЛИРУЕМОСТЬ", "• Актуальная информация о загруженности для городских служб"),
        ("ОБРАТНАЯ СВЯЗЬ ОПЕРАТОРУ", "• Возможность менять маршруты с учётом ремонтов, мелей")
    ]
    
    for i, (title, desc) in enumerate(task_items):
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.name = HEADERS_FONT
        
        # Добавляем иконку-квадрат перед текстом
        run = p.add_run()
        run.text = "📍 " if i < 5 else ""
        
        p.add_paragraph()
        p.text = desc
        p.font.size = Pt(16)
        p.font.name = BODY_FONT
    
    # ====== СЛАЙД 5: ТИПЫ АТС ======
    slide = prs.slides.add_slide(slide_layout)
    
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['primary_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Четыре типа АТС и транспортные среды"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    # Номер слайда
    slide_num_label = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.3))
    tf = slide_num_label.text_frame
    p = tf.paragraphs[0]
    p.text = "5"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = RgbColor(*COLORS['white'])
    
    # Таблица с четырьмя типами транспорта
    table_start = Inches(0.8)
    table_top = Inches(1.6)
    table_left = Inches(0.8)
    table_width = Inches(11.7)
    table_height = Inches(4.2)
    
    # Создаём таблицу 5x2 (заголовок + 4 типа транспорта x 2 колонки)
    rows = 5
    cols = 2
    
    from pptx.table import Table, Row
    table = slide.shapes.add_table(rows, cols, table_start, table_top, table_width, Inches(3.8)).table
    
    # Заголовок таблицы
    table.cell(0, 0).text = "Тип АТС"
    table.cell(0, 1).text = "Транспортная среда | Типовые препятствия"
    
    # Стиль заголовка
    for cell in table.rows[0].cells:
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(16)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RgbColor(COLORS['white'][0], COLORS['white'][1], 240)
    
    # Данные таблицы
    transport_data = [
        ("Ровер", "Тротуары | Лестницы, узкие проходы, скопления людей"),
        ("Автомобиль", "Дороги | Перекопы, светофоры, закрытые полосы"),
        ("Дрон", "Воздух | Запретные зоны, эшелоны высот"),
        ("Катер", "Вода | Шлюзы, разводные мосты, мели")
    ]
    
    for i, (type_name, environment_obstacles) in enumerate(transport_data):
        table.cell(i + 1, 0).text = type_name
        table.cell(i + 1, 1).text = environment_obstacles
        
        # Стиль ячеек с данными
        cell_type = table.cell(i + 1, 0)
        cell_env = table.cell(i + 1, 1)
        
        for cell in [cell_type, cell_env]:
            cell.text_frame.paragraphs[0].font.size = Pt(17)
            cell.text_frame.paragraphs[0].font.name = BODY_FONT
    
    # ====== СЛАЙД 6: ЦИКЛ ДИСПЕТЧЕРИЗАЦИИ ======
    slide = prs.slides.add_slide(slide_layout)
    
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['light_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Цикл диспетчеризации МДС"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    # Номер слайда
    slide_num_label = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.3))
    tf = slide_num_label.text_frame
    p = tf.paragraphs[0]
    p.text = "6"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = RgbColor(*COLORS['white'])
    
    # Диаграмма цикла (цифровые блоки)
    diagram_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.2))
    tf = diagram_box.text_frame
    tf.word_wrap = True
    
    cycle_steps = [
        "🔵 Оператор АТС → Заявка в МДС",
        "🟢 Проверка конфликтов и препятствий",
        "🟡 Согласование: одобрено / с изменениями / отклонено",
        "🟠 Маршрут вносится в карту занятости",
        "🔴 Оператор отправляет телеметрию (позиция, статус, ETA)",
        "🟣 МДС актуализирует и корректирует маршруты"
    ]
    
    for step in cycle_steps:
        p = tf.add_paragraph()
        p.text = step
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.name = BODY_FONT
    
    # ====== СЛАЙД 7: АРХИТЕКТУРА ======
    slide = prs.slides.add_slide(slide_layout)
    
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['primary_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Архитектура системы МДС"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    # Номер слайда
    slide_num_label = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.3))
    tf = slide_num_label.text_frame
    p = tf.paragraphs[0]
    p.text = "7"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = RgbColor(*COLORS['white'])
    
    # Два блока с компонентами
    left_block = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.2), Inches(3.9))
    tf = left_block.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    p.text = "Компоненты МДС:"
    
    components_left = [
        "🗺️ CityMap — карта препятствий (лестницы, шлюзы)",
        "⚙️ Dispatcher — ядро системы (приём заявок, согласование)",
        "📊 Detector — детект отклонений от плана",
        "✓ Validator — валидация телеметрии клиентов"
    ]
    
    for comp in components_left:
        p = tf.add_paragraph()
        p.text = comp
        p.font.size = Pt(16)
        p.font.name = BODY_FONT
    
    right_block = slide.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.2), Inches(3.9))
    tf = right_block.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    p.text = "Карта занятости (4 слоя):"
    
    layers = [
        "🚶 sidewalk — тротуарные роверы",
        "🚗 road — беспилотные автомобили",
        "✈️ air — воздушные дроны",
        "⛵ water — водные катера"
    ]
    
    for layer in layers:
        p = tf.add_paragraph()
        p.text = layer
        p.font.size = Pt(16)
        p.font.name = BODY_FONT
    
    # ====== СЛАЙД 8: СТРУКТУРЫ ДАННЫХ ======
    slide = prs.slides.add_slide(slide_layout)
    
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['light_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Формат телеметрии"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    # Номер слайда
    slide_num_label = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.3))
    tf = slide_num_label.text_frame
    p = tf.paragraphs[0]
    p.text = "8"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = RgbColor(*COLORS['white'])
    
    # JSON пример с цветным фоном
    json_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.2))
    tf = json_box.text_frame
    tf.word_wrap = True
    
    json_example = """{
  "client_id": "pizza_shop_01",
  "batch_id": "batch-001",
  "vehicles": [{
    "vehicle_id": "rover_007",
    "route_id": "R-001",
    "position": {"x": 12.5, "y": 34.2},
    "status": "moving",
    "progress": 0.35,
    "eta": "2025-06-01T14:12:00Z",
    "alerts": []
  }]
}"""
    
    # Красивое форматирование JSON через escape
    p = tf.add_paragraph()
    p.text = json_example.strip()
    p.font.size = Pt(14)
    p.font.name = 'Courier New'
    
    # ====== СЛАЙД 9: ТЕХНОЛОГИИ ======
    slide = prs.slides.add_slide(slide_layout)
    
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['primary_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Технологии и масштабируемость"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    # Номер слайда
    slide_num_label = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.3))
    tf = slide_num_label.text_frame
    p = tf.paragraphs[0]
    p.text = "9"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = RgbColor(*COLORS['white'])
    
    # Технологический стек в виде колонок с иконками
    tech_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.8))
    tf = tech_box.text_frame
    tf.word_wrap = True
    
    tech_items = [
        ("🐍 Python 3.10+", "Основной язык программирования"),
        ("🌐 Flask", "Веб-сервер и REST API"),
        ("✓ Pydantic", "Валидация данных (схема JSON)"),
        ("⚓ Shapely", "Геометрические расчёты"),
        ("🕸️ Networkx", "Графы маршрутов"),
        ("📊 Matplotlib", "Визуализация и графики"),
        ("🔌 WebSocket", "Связь в реальном времени")
    ]
    
    for i, (name, desc) in enumerate(tech_items):
        p = tf.add_paragraph()
        p.text = name + " — " + desc
        p.font.size = Pt(16)
        p.font.name = BODY_FONT
    
    # ====== СЛАЙД 10: ВЫВОДЫ ======
    slide = prs.slides.add_slide(slide_layout)
    
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RgbColor(*COLORS['light_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Выводы и перспективы"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    
    # Номер слайда
    slide_num_label = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.3))
    tf = slide_num_label.text_frame
    p = tf.paragraphs[0]
    p.text = "10"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = RgbColor(*COLORS['white'])
    
    # Выводы и перспективы
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.2))
    tf = content_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    p.text = "Четыре ключевых вывода:"
    
    conclusions = [
        "✓ МДС — арбитр, а не пилот (проверка и согласование маршрутов)",
        "✓ Каждый маршрут влияет на следующие через карту занятости",
        "✓ Телеметрия замыкает контур диспетчеризации",
        "✓ Система масштабируема для новых типов транспорта"
    ]
    
    for conc in conclusions:
        p = tf.add_paragraph()
        p.text = conc
        p.font.size = Pt(16)
        p.font.name = BODY_FONT
    
    # Перспективы
    p = tf.add_paragraph()
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.fill.fore_color.rgb = RgbColor(*COLORS['white'])
    p.text = "\nПерспективы развития:"
    
    prospects = [
        "🎮 Динамика в реальном времени (pygame-анимация)",
        "🚑 Приоритет срочных доставок (медикаменты)",
        "↩️ Пересмотр маршрутов при новых препятствиях",
        "🤖 Машинное обучение для прогнозирования загруженности",
        "🌐 Веб-интерфейс для операторов"
    ]
    
    for prospect in prospects:
        p = tf.add_paragraph()
        p.text = prospect
        p.font.size = Pt(16)
        p.font.name = BODY_FONT
    
    # Сохраняем как PPTX, затем конвертируем в ODP
    prs.save("presentation_template.pptx")
    return "presentation_template.pptx"

if __name__ == "__main__":
    print("Creating presentation template...")
    pptx_file = create_odp_presentation()
    print(f"Template created: {pptx_file}")
