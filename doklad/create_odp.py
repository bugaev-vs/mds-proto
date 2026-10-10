from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_presentation():
    """Создание ODP презентации с улучшенным дизайном."""
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    COLORS = {
        'primary_blue': (0, 51, 102),
        'light_blue': (0, 102, 153),
        'white': (255, 255, 255),
    }
    
    HEADERS_FONT = 'Calibri Light'
    BODY_FONT = 'Calibri'
    
    # ====== СЛАЙД 1: ТИТУЛЬНЫЙ ======
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    bg_shape = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['primary_blue'])
    bg_shape.line.fill.background()
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.7), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Мультимодальная диспетчерская система управления беспилотным транспортом"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.alignment = PP_ALIGN.CENTER
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(11.7), Inches(1))
    tf = subtitle_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Школьный проект"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    p.alignment = PP_ALIGN.CENTER
    
    info_box = slide.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.2))
    tf = info_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Версия 1.0 | Октябрь 2026"
    p.font.size = Pt(16)
    p.font.name = BODY_FONT
    p.alignment = PP_ALIGN.CENTER
    
    left_circle = slide.shapes.add_shape(5, Inches(0.4), Inches(4.5), Inches(2.8), Inches(3))
    left_circle.fill.solid()
    left_circle.fill.fore_color.rgb = RGBColor(*COLORS['light_blue'])
    
    right_circle = slide.shapes.add_shape(5, Inches(10.1), Inches(4.5), Inches(2.8), Inches(3))
    right_circle.fill.solid()
    right_circle.fill.fore_color.rgb = RGBColor(*COLORS['light_blue'])
    
    # ====== СЛАЙД 2: АКТУАЛЬНОСТЬ ======
    slide = prs.slides.add_slide(slide_layout)
    bg_shape = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['primary_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Актуальность проекта"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = HEADERS_FONT
    
    slide_num = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.4))
    tf = slide_num.text_frame
    p = tf.paragraphs[0]
    p.text = "2"
    p.font.size = Pt(50)
    p.font.bold = True
    
    left_col = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.2), Inches(4.5))
    tf = left_col.text_frame
    p = tf.paragraphs[0]
    p.text = "Рост количества АТС:\n• Тротуарные роверы\n• Беспилотные автомобили\n• Воздушные дроны\n• Водные беспилотные суда"
    
    right_col = slide.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.2), Inches(4.5))
    tf = right_col.text_frame
    p = tf.paragraphs[0]
    p.text = "Проблема без диспетчеризации:\n• Столкновения\n• Взаимные блокировки\n• Нарушение запретных зон"
    
    # ====== СЛАЙД 3: ПРОБЛЕМА ПДД ======
    slide = prs.slides.add_slide(slide_layout)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['primary_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Почему правил ПДД недостаточно"
    
    slide_num = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.4))
    tf = slide_num.text_frame
    p = tf.paragraphs[0]
    p.text = "3"
    p.font.size = Pt(50)
    
    col1 = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.2), Inches(4))
    tf = col1.text_frame
    p = tf.paragraphs[0]
    p.text = "Правила распространяются только на наземный транспорт\n• Ширина тротуаров не всегда позволяет движение АТС\n• Законы об АТС на стадии разработки"
    
    col2 = slide.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.2), Inches(4))
    tf = col2.text_frame
    p = tf.paragraphs[0]
    p.text = "Штат ГАИ не покрывает рост АТС\n• ДТП с техникой растут\n• АТС не умеют интерпретировать регулировщика"
    
    # ====== СЛАЙД 4: ЗАДАЧИ МДС ======
    slide = prs.slides.add_slide(slide_layout)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['light_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Основные задачи МДС"
    
    slide_num = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.4))
    tf = slide_num.text_frame
    p = tf.paragraphs[0]
    p.text = "4"
    p.font.size = Pt(50)
    
    tasks_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.2))
    tf = tasks_box.text_frame
    
    tasks = [
        "СНИЖЕНИЕ СРОКОВ ДОСТАВКИ - выбор оптимального маршрута",
        "БЕЗОПАСНОСТЬ - недопущение столкновений",
        "ПОВЫШЕНИЕ ЭФФЕКТИВНОСТИ - без перегрузки коридоров",
        "КОНТРОЛЛИРУЕМОСТЬ - информация для городских служб",
        "ОБРАТНАЯ СВЯЗЬ - изменение маршрутов при ремонтах"
    ]
    
    for task in tasks:
        tf.add_paragraph().text = task
    
    # ====== СЛАЙД 5: ТИПЫ АТС ======
    slide = prs.slides.add_slide(slide_layout)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['primary_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Четыре типа АТС и транспортные среды"
    
    slide_num = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.4))
    tf = slide_num.text_frame
    p = tf.paragraphs[0]
    p.text = "5"
    p.font.size = Pt(50)
    
    table = slide.shapes.add_table(5, 3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4)).table
    
    # ====== СЛАЙД 6: ЦИКЛ ======
    slide = prs.slides.add_slide(slide_layout)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['light_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Цикл диспетчеризации МДС"
    
    slide_num = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.4))
    tf = slide_num.text_frame
    p = tf.paragraphs[0]
    p.text = "6"
    p.font.size = Pt(50)
    
    cycle_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(4))
    tf = cycle_box.text_frame
    
    cycle_steps = [
        "Оператор АТС -> Заявка в МДС",
        "Проверка конфликтов и препятствий",
        "Согласование: одобрено / с изменениями / отклонено",
        "Маршрут вносится в карту занятости",
        "Оператор отправляет телеметрию",
        "МДС актуализирует маршруты"
    ]
    
    for step in cycle_steps:
        tf.add_paragraph().text = step
    
    # ====== СЛАЙД 7: АРХИТЕКТУРА ======
    slide = prs.slides.add_slide(slide_layout)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['primary_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Архитектура системы МДС"
    
    slide_num = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.4))
    tf = slide_num.text_frame
    p = tf.paragraphs[0]
    p.text = "7"
    p.font.size = Pt(50)
    
    left_block = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.2), Inches(3.9))
    tf = left_block.text_frame
    
    comp_left = [
        "CityMap - карта препятствий",
        "Dispatcher - ядро системы",
        "Detector - детект отклонений",
        "Validator - валидация телеметрии"
    ]
    
    for comp in comp_left:
        tf.add_paragraph().text = comp
    
    right_block = slide.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.2), Inches(3.9))
    tf = right_block.text_frame
    
    layers = [
        "sidewalk - тротуарные роверы",
        "road - беспилотные автомобили",
        "air - воздушные дроны",
        "water - водные катера"
    ]
    
    for layer in layers:
        tf.add_paragraph().text = layer
    
    # ====== СЛАЙД 8: ФОРМАТЫ ======
    slide = prs.slides.add_slide(slide_layout)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['light_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Формат телеметрии"
    
    slide_num = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.4))
    tf = slide_num.text_frame
    p = tf.paragraphs[0]
    p.text = "8"
    p.font.size = Pt(50)
    
    json_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(4))
    tf = json_box.text_frame
    
    json_example = """{
  "client_id": "pizza_shop_01",
  "batch_id": "batch-001",
  "vehicles": [{
    "vehicle_id": "rover_007",
    "route_id": "R-001",
    "position": {"x": 12.5, "y": 34.2},
    "status": "moving",
    "progress": 0.35,
    "eta": "2025-06-01T14:12:00Z"
  }]
}"""
    
    p = tf.add_paragraph()
    p.text = json_example.strip()
    p.font.name = 'Courier New'
    
    # ====== СЛАЙД 9: ТЕХНОЛОГИИ ======
    slide = prs.slides.add_slide(slide_layout)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['primary_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Технологии и масштабируемость"
    
    slide_num = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.4))
    tf = slide_num.text_frame
    p = tf.paragraphs[0]
    p.text = "9"
    p.font.size = Pt(50)
    
    tech_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.8))
    tf = tech_box.text_frame
    
    tech_items = [
        "Python 3.10+ - основной язык",
        "Flask - веб-сервер и REST API",
        "Pydantic - валидация данных",
        "Shapely - геометрические расчёты",
        "Networkx - графы маршрутов",
        "Matplotlib - визуализация",
        "WebSocket - связь в реальном времени"
    ]
    
    for tech in tech_items:
        tf.add_paragraph().text = tech
    
    # ====== СЛАЙД 10: ВЫВОДЫ ======
    slide = prs.slides.add_slide(slide_layout)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*COLORS['light_blue'])
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Выводы и перспективы"
    
    slide_num = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(2), Inches(0.4))
    tf = slide_num.text_frame
    p = tf.paragraphs[0]
    p.text = "10"
    p.font.size = Pt(50)
    
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.2))
    tf = content_box.text_frame
    
    conclusions = [
        "МДС - арбитр, а не пилот",
        "Каждый маршрут влияет на следующие через карту занятости",
        "Телеметрия замыкает контур диспетчеризации",
        "Система масштабируема для новых типов транспорта"
    ]
    
    for conc in conclusions:
        tf.add_paragraph().text = conc
    
    prospects = [
        "Динамика в реальном времени (pygame)",
        "Приоритет срочных доставок",
        "Пересмотр маршрутов при препятствиях",
        "Машинное обучение для прогнозов",
        "Веб-интерфейс для операторов"
    ]
    
    tf.add_paragraph().text = "\nПерспективы развития:"
    for prospect in prospects:
        tf.add_paragraph().text = prospect
    
    prs.save("presentation_mds.odp")
    return "presentation_mds.odp"

if __name__ == "__main__":
    pptx_file = create_presentation()
    print(f"Презентация создана: {pptx_file}")
