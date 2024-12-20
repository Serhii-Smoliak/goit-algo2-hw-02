# Завдання 1. Оптимізація черги 3D-принтера в університетській лабораторії

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    # Створюємо об'єкти завдань на друк
    jobs = [PrintJob(**job) for job in print_jobs]

    # Сортуємо завдання за пріоритетом (спочатку найвищий) і часом друку (спочатку мінімальний)
    jobs.sort(key=lambda job: (job.priority, job.print_time))

    # Ініціалізація для групування завдань
    print_order = []
    total_time = 0
    current_group = []
    current_volume = 0
    current_items = 0

    # Групуємо завдання за обсягом і кількістю, не перевищуючи обмеження
    for job in jobs:
        if current_items < constraints["max_items"] and current_volume + job.volume <= constraints["max_volume"]:
            current_group.append(job)
            current_volume += job.volume
            current_items += 1
        else:
            # Додаємо попередню групу до списку і перезапускаємо групу
            if current_group:
                print_order.append([job.id for job in current_group])
                total_time += max(job.print_time for job in current_group)
            current_group = [job]
            current_volume = job.volume
            current_items = 1

    # Додаємо останню групу
    if current_group:
        print_order.append([job.id for job in current_group])
        total_time += max(job.print_time for job in current_group)

    # Повертаємо результат
    return {
        "print_order": [job for group in print_order for job in group],
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
