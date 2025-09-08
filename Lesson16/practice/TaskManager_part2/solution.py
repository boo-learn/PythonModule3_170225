from connection import Connect
from pathlib import Path
from typing import Optional, Literal



class Task:
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

    def __init__(self, title, description="", status="Pending", priority=3, id = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', description = '{self.description}', status = '{self.status}', priority={self.priority})"

    # Добавьте методы для изменения статуса
    def mark_as_completed(self):
        self.status = Task.COMPLETED

    def mark_as_in_progress(self):
        self.status = Task.IN_PROGRESS

    def mark_as_pending(self):
        self.status = Task.PENDING

    # Добавьте метод для изменения приоритета
    def set_priority(self, new_priority: int):
        if 1 <= new_priority <= 5:
            self.priority = new_priority
        else:
            # print("new_priority должен быть в диапазоне от 1 до 5")
            raise ValueError("new_priority должен быть в диапазоне от 1 до 5")


class TaskRepository:
    DB_FILE = Path("tasks.db")
    # Типы
    StatusType = Literal["Pending", "In Progress", "Completed"]
    PriorityType = Literal[1, 2, 3, 4, 5]
    Order_byType = Literal["ASC", "DESC"]

    def __init__(self):
        TaskRepository._ensure_db_table_exists()

    @staticmethod
    def _map_rows_to_tasks(tasks_data: list[tuple]) -> list[Task]:
        tasks = []
        for data in tasks_data:
            tasks.append(Task(*data[1:], data[0]))
        return tasks

    @classmethod
    def _ensure_db_table_exists(cls):
        """Создает таблицу tasks, если она еще не существует."""
        with Connect(cls.DB_FILE) as cursor:
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS tasks
                        (
                            task_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                            title       TEXT NOT NULL,
                            description TEXT,
                            status      TEXT CHECK (status IN ('Pending', 'In Progress', 'Completed')) DEFAULT 'Pending',
                            priority    INTEGER CHECK ( priority BETWEEN 1 AND 5) DEFAULT 3
                        );
                    ''')
    def save(self, task: Task):
        """
        Сохраняет или обновляет задачу в базе данных.
        Если id None, вставляет новую задачу. Иначе, обновляет существующую.
        """
        self._ensure_db_table_exists()
        sql_insert = "INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)"
        sql_update =  """
            UPDATE tasks 
            SET title = ?, description = ?, status = ?, priority = ?
            WHERE task_id = ?;
        """
        if task.id:
            with Connect(TaskRepository.DB_FILE) as cursor:
                cursor.execute(sql_update, (task.title, task.description, task.status, task.priority, task.id))
        else:
            with Connect(TaskRepository.DB_FILE) as cursor:
                cursor.execute(sql_insert, (task.title, task.description, task.status, task.priority))
                task.id = cursor.lastrowid

    def get_by_id(self, id) -> Optional['Task']:
        sql_select = "SELECT * FROM tasks WHERE task_id = ?"
        with Connect(self.DB_FILE) as cursor:
            cursor.execute(sql_select, (id,))
            data = cursor.fetchone()
            if data is not None:
                # return Task(id=data[0], title=data[1], description=data[2], status=data[3], priority=data[4])
                return Task(*data[1:], data[0])#
            else:
                print(f"Задача с id={id} отсутствует")
                return None

    def get_all_tasks(self) -> list['Task']:
        sql_select = "SELECT * FROM tasks"
        with Connect(self.DB_FILE) as cursor:
            cursor.execute(sql_select)
            return self._map_rows_to_tasks(cursor.fetchall())



    def delete(self, task: Task):
        """Удаляет задачу из базы данных."""
        sql_delete = "DELETE FROM tasks WHERE task_id = ?"
        if task is None or task.id is None:
            print("Нельзя удалить: задача отсутствует или не имеет id")
            return
        with Connect(self.DB_FILE) as cursor:
            cursor.execute(sql_delete, (task.id,))
            if cursor.rowcount > 0:
                print(f"Задача с id={task.id} удалена")
            else:
                print(f"Задача с id={task.id} не найдена")
            task.id = None

    def get_tasks_by_status(self, status: StatusType) -> list[Task]:
    # Возвращает список зада с определенным статусом.
        sql_select = "SELECT * FROM tasks WHERE status = ?"
        if status  in ['Pending', 'In Progress', 'Completed']:
            raise ValueError(f"status = {status} --> должен быть только из: 'Pending', 'In Progress', 'Completed'")
        with Connect(self.DB_FILE) as cursor:
            cursor.execute(sql_select, (status,))
            return self._map_rows_to_tasks(cursor.fetchall())

    def get_tasks_by_priority(self, priority: PriorityType) -> list[Task]:
    # Возвращает список задач с определенным приоритетом.
        sql_select = "SELECT * FROM tasks WHERE priority = ?"
        if isinstance(priority, int) and 1 <= priority <= 5:
            with Connect(self.DB_FILE) as cursor:
                cursor.execute(sql_select, (priority,))
                return self._map_rows_to_tasks(cursor.fetchall())
        else:
            raise ValueError(f"priority --> должен быть integer или : 1 <= priority <= 5")

    def get_completed_tasks(self) -> list[Task]:
    # Специализированный метод для получения всех завершенных задач.
        sql_select = "SELECT * FROM tasks WHERE status = 'Completed'"
        with Connect(self.DB_FILE) as cursor:
            cursor.execute(sql_select)
            return self._map_rows_to_tasks(cursor.fetchall())


    def get_tasks_by_title_contains(self, keyword: str) -> list[Task]:
    # Поиск задач по ключевому слову в заголовке.
        if not isinstance(keyword, str):
            raise TypeError("Ожидается строка для поиска в заголовке.")
        if not keyword.strip():
            raise ValueError("Ключевое слово не должно быть пустым.") # если отправить пустую строку, выдаст всю базу, такая функция уже есть
        sql_select = "SELECT * FROM tasks WHERE LOWER(title) LIKE LOWER(?)"
        pattern = f"%{keyword}%"
        with Connect(self.DB_FILE) as cursor:
            cursor.execute(sql_select, (pattern,))
            return self._map_rows_to_tasks(cursor.fetchall())

    def get_tasks_by_priority_range(self, min_priority: PriorityType, max_priority: PriorityType, order: Order_byType = 'ASC') -> list[Task]:
    # Задачи в заданном диапазоне приоритетов. Методы получения задач с сортировкой:
        if not all(isinstance(p, int) for p in (min_priority, max_priority)):
            raise TypeError("Оба значения должны быть целыми числами.")
        if not (1 <= min_priority <= 5 and 1 <= max_priority <= 5):
            raise ValueError("Приоритет должен быть в диапазоне от 1 до 5.")
        if min_priority > max_priority:
            raise ValueError("Минимальный приоритет не может быть больше максимального.")
        order = order.upper()
        if order not in ['ASC', 'DESC']:
            raise ValueError("Параметр 'order' должен быть 'ASC' или 'DESC'.")
        sql_select = f"""
        SELECT * FROM tasks 
        WHERE priority BETWEEN ? AND ?
        ORDER BY priority {order}
        """
        with Connect(self.DB_FILE) as cursor:
            cursor.execute(sql_select, (min_priority, max_priority))
            return self._map_rows_to_tasks(cursor.fetchall())

    def get_all_tasks_sorted_by_priority(self, order: Order_byType = 'ASC', ascending: bool = True) -> list[Task]:
    # Получает все задачи, отсортированные по приоритету.
        order = order.upper()
        if order not in ['ASC', 'DESC']:
            raise ValueError("Параметр 'order' должен быть 'ASC' или 'DESC'.")
        sql_select = f"SELECT * FROM tasks ORDER BY priority {order}"
        if ascending:
            with Connect(self.DB_FILE) as cursor:
                cursor.execute(sql_select)
                return self._map_rows_to_tasks(cursor.fetchall())
        else:
            return []

    def get_tasks_by_status_sorted_by_priority(self, status: StatusType, order: Order_byType = 'ASC', ascending: bool = True) -> list[Task]:
        #Получает задачи по статусу, отсортированные по приоритету.
        if status not in ['Pending', 'In Progress', 'Completed']:
            error_text = f"status = {status} --> должен быть только из: 'Pending', 'In Progress', 'Completed'"
            raise ValueError(error_text)
        order = order.upper()
        if order not in ['ASC', 'DESC']:
            raise ValueError("Параметр 'order' должен быть 'ASC' или 'DESC'.")
        sql = f"""
        SELECT * FROM tasks 
        WHERE status = ? ORDER BY priority {order}
        """
        if ascending:
            with Connect(self.DB_FILE) as cursor:
                cursor.execute(sql, (status,))
                return self._map_rows_to_tasks(cursor.fetchall())
        else:
            return []

    def delete_completed_tasks(self) -> int:
    # Удаляет все задачи со статусом "Завершено".
        sql = f"""
                   DELETE FROM tasks 
                   WHERE status = 'Completed'
                   """
        try:
            with Connect(self.DB_FILE) as cursor:
                cursor.execute(sql)
                deleted_count = cursor.rowcount # возвращает количество строк, затронутых последней операцией
                print(f"удалено задач: {deleted_count}")
                return deleted_count
        except Exception as e:
            raise Exception(f"Произошла непредвиденная ошибка при удалении завершенных задач: {e}") from e

    def delete_all_tasks(self) -> int:
    # Удаляет все задачи со статусом "Завершено".
        sql = f"DELETE FROM tasks"
        try:
            with Connect(self.DB_FILE) as cursor:
                cursor.execute(sql)
                deleted_count = cursor.rowcount # возвращает количество строк, затронутых последней операцией
                # print(f"удалено задач: {deleted_count}")
                return deleted_count
        except Exception as e:
            raise Exception(f"Произошла непредвиденная ошибка при удалении задач: {e}") from e

###################################
#
###################################

# tasks = [
#     Task("молоко в холодильнике", "найти молоко", status='Completed', priority=1),
#     Task("написать отчет", "сделать отчет по проекту до понедельника", status='In Progress', priority=5),
#     Task("купить хлеб", "зайти в ближайший магазин", status='Pending', priority=2),
#     Task("помыть посуду", "особенно кастрюли", status='Completed', priority=3),
#     Task("прочитать книгу", "прочитать хотя бы 50 страниц", status='In Progress', priority=4),
#     Task("записаться к врачу", "позвонить в клинику и записаться", status='Pending', priority=5),
#     Task("выучить 10 слов по немецкому", "использовать Quizlet", status='Pending', priority=4),
#     Task("забрать посылку", "отделение почты работает до 18:00", status='Completed', priority=2),
#     Task("позвонить другу", "спросить про планы на выходные", status='Pending', priority=3),
#     Task("подготовить презентацию", "для встречи в пятницу", status='In Progress', priority=1),
#     Task("оплатить интернет", "до 25 числа", status='Completed', priority=4),
#     Task("найти новую статью", "для курсовой работы", status='In Progress', priority=5)
# ]
# # # # Использование
# task_repository = TaskRepository() # Создаем экземпляр репозитория
# for task in tasks:
#     task_repository.save(task)

# show_tasks = task_repository.get_all_tasks()
# show_tasks = task_repository.get_tasks_by_status("Completed")
# show_tasks = task_repository.get_tasks_by_priority(2+1+1)
# show_tasks = task_repository.get_completed_tasks()
# show_tasks = task_repository.get_tasks_by_priority_range(1,5, "DESC")
# show_tasks = task_repository.get_all_tasks_sorted_by_priority()
# show_tasks = task_repository.get_tasks_by_status_sorted_by_priority('Completed')
# show_tasks = task_repository.get_all_tasks()

# for task in show_tasks:
#     print(task)

# task_repository.delete_all_tasks()
# task_repository.delete_completed_tasks()
