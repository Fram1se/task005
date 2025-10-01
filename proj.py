import datetime
import json
import os

# Файл для хранения данных
DATA_FILE = "students_data.json"

def load_students():
    """Загрузка данных студентов из файла"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            print("Ошибка загрузки данных. Будет создана новая база.")
    
    # Возвращаем базовую базу данных, если файла нет
    return {
        "Иванов Иван Иванович": {
            "группа": "ТВ-101",
            "колледж": "Технический колледж", 
            "год_поступления": 2023,
            "курс": 2
        },
        "Петрова Анна Сергеевна": {
            "группа": "ИС-102",
            "колледж": "Колледж информационных систем",
            "год_поступления": 2022,
            "курс": 3
        },
        "Сидоров Алексей Петрович": {
            "группа": "ЭК-103", 
            "колледж": "Экономический колледж",
            "год_поступления": 2023,
            "курс": 2
        },
        "Козлова Мария Дмитриевна": {
            "группа": "ДЗ-104",
            "колледж": "Колледж дизайна",
            "год_поступления": 2024,
            "курс": 1
        },
        "Николаев Денис Сергеевич": {
            "группа": "МТ-105",
            "колледж": "Механико-технологический колледж", 
            "год_поступления": 2022,
            "курс": 3
        }
    }

def save_students(students_data):
    """Сохранение данных студентов в файл"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(students_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")
        return False

def calculate_current_course(admission_year):
    """Расчет текущего курса на основе года поступления"""
    current_year = datetime.datetime.now().year
    current_course = current_year - admission_year + 1
    return max(1, min(4, current_course))

def search_students(students_data, search_term, search_field="все"):
    """
    Поиск студентов по различным критериям:cite[1]:cite[4]
    
    search_field может быть:
    - "фамилия", "имя", "отчество" - поиск по частям ФИО
    - "группа", "колледж" - поиск по конкретным полям
    - "все" - поиск по всем полям
    """
    search_term_lower = search_term.lower()
    found_students = {}
    
    for full_name, data in students_data.items():
        # Разбиваем ФИО на части
        name_parts = full_name.split()
        last_name = name_parts[0] if len(name_parts) > 0 else ""
        first_name = name_parts[1] if len(name_parts) > 1 else ""
        middle_name = name_parts[2] if len(name_parts) > 2 else ""
        
        match = False
        
        if search_field == "все":
            # Поиск по всем полям:cite[1]
            match = (search_term_lower in last_name.lower() or
                    search_term_lower in first_name.lower() or
                    search_term_lower in middle_name.lower() or
                    search_term_lower in data['группа'].lower() or
                    search_term_lower in data['колледж'].lower())
        
        elif search_field == "фамилия":
            match = search_term_lower in last_name.lower()
        
        elif search_field == "имя":
            match = search_term_lower in first_name.lower()
        
        elif search_field == "отчество":
            match = search_term_lower in middle_name.lower()
        
        elif search_field == "группа":
            match = search_term_lower in data['группа'].lower()
        
        elif search_field == "колледж":
            match = search_term_lower in data['колледж'].lower()
        
        if match:
            found_students[full_name] = data
    
    return found_students

def display_student_info(full_name, student_data):
    """Отображение информации о студенте"""
    current_course = calculate_current_course(student_data["год_поступления"])
    
    print(f"\nНайден студент: {full_name}")
    print("=" * 50)
    print(f"Группа: {student_data['группа']}")
    print(f"Колледж: {student_data['колледж']}")
    print(f"Год поступления: {student_data['год_поступления']}")
    print(f"Текущий курс: {current_course}")
    print("=" * 50)

def display_search_results(found_students, search_term, search_field):
    """Отображение результатов поиска"""
    if found_students:
        print(f"\nНайдено студентов: {len(found_students)}")
        print("Список найденных студентов:")
        for i, (full_name, student_data) in enumerate(found_students.items(), 1):
            current_course = calculate_current_course(student_data["год_поступления"])
            print(f"{i}. {full_name} - {student_data['группа']} ({student_data['колледж']}), курс {current_course}")
        
        # Предлагаем выбрать конкретного студента
        try:
            choice = input("\nВведите номер студента для подробной информации (или 0 для отмены): ")
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(found_students):
                    full_name = list(found_students.keys())[choice_num - 1]
                    display_student_info(full_name, found_students[full_name])
        except ValueError:
            pass
    else:
        print(f"\nСтуденты по запросу '{search_term}' не найдены.")

def register_new_student(students_data):
    """Регистрация нового студента"""
    try:
        print("\nВведите данные нового студента:")
        last_name = input("Фамилия: ").strip()
        first_name = input("Имя: ").strip()
        middle_name = input("Отчество: ").strip()
        
        full_name = f"{last_name} {first_name} {middle_name}"
        
        if full_name in students_data:
            print("Студент с таким ФИО уже существует!")
            return students_data
            
        group = input("Группа: ").strip()
        college = input("Колледж: ").strip()
        admission_year = int(input("Год поступления: "))
        
        # Проверка корректности года поступления
        current_year = datetime.datetime.now().year
        if admission_year > current_year or admission_year < current_year - 4:
            print("Предупреждение: Год поступления кажется некорректным!")
        
        initial_course = calculate_current_course(admission_year)
        
        # Добавление в базу
        students_data[full_name] = {
            "группа": group,
            "колледж": college,
            "год_поступления": admission_year,
            "курс": initial_course
        }
        
        if save_students(students_data):
            print(f"\nСтудент '{full_name}' успешно зарегистрирован!")
            print(f"Начальный курс: {initial_course}")
        else:
            print("Ошибка при сохранении данных!")
            del students_data[full_name]  # Удаляем если не сохранилось
                
    except ValueError:
        print("Ошибка: введите корректный год поступления!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    return students_data

def get_search_field_choice():
    """Выбор поля для поиска"""
    print("\nВыберите поле для поиска:")
    print("1 - Фамилия")
    print("2 - Имя") 
    print("3 - Отчество")
    print("4 - Группа")
    print("5 - Колледж")
    print("6 - Поиск по всем полям")
    
    choice = input("Введите номер (1-6): ").strip()
    
    field_map = {
        "1": "фамилия",
        "2": "имя",
        "3": "отчество", 
        "4": "группа",
        "5": "колледж",
        "6": "все"
    }
    
    return field_map.get(choice, "все")

def main():
    print("=== Универсальная система поиска студентов ===")
    
    # Загрузка данных при запуске
    students_data = load_students()
    print(f"Загружено записей: {len(students_data)}")
    
    while True:
        # Выбор типа поиска
        search_field = get_search_field_choice()
        field_display = "фамилии" if search_field == "фамилия" else \
                       "имени" if search_field == "имя" else \
                       "отчеству" if search_field == "отчество" else \
                       "группе" if search_field == "группа" else \
                       "колледжу" if search_field == "колледж" else "всем полям"
        
        search_term = input(f"\nВведите значение для поиска по {field_display}: ").strip()
        
        if not search_term:
            print("Пожалуйста, введите значение для поиска.")
            continue
            
        # Поиск студентов
        found_students = search_students(students_data, search_term, search_field)
        display_search_results(found_students, search_term, search_field)
        
        # Предложение зарегистрировать нового студента если ничего не найдено
        if not found_students:
            answer = input("Хотите зарегистрировать нового студента? (да/нет): ").strip().lower()
            if answer == 'да':
                students_data = register_new_student(students_data)
        
        # Запрос на продолжение
        continue_work = input("\nПродолжить поиск? (да/нет): ").strip().lower()
        if continue_work != 'да':
            # Сохраняем данные перед выходом
            if save_students(students_data):
                print("Данные успешно сохранены.")
            print("До свидания!")
            break

if __name__ == "__main__":
    main()
