import random
import sqlite3
from pathlib import Path
from helpers.connection import Connect

DATABASE_NAME = 'vocabulary.db'


def init_db(db_path: Path = Path(DATABASE_NAME)):
    """Инициализирует базу данных, создает таблицу words, если ее нет."""
    sql_words = """
    CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    english_word TEXT NOT NULL UNIQUE,
    russian_translation TEXT NOT NULL
    );"""

    sql_answers = """CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    test_type TEXT NOT NULL CHECK (test_type IN ('en_ru', 'ru_en')),
    is_correct INTEGER NOT NULL CHECK (is_correct IN (0, 1)),  
    FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE
    );
    """
    try:
        with Connect(db_path) as cursor:
            cursor.execute(sql_words)
            cursor.execute(sql_answers)
        print("База данных готова.")
    except sqlite3.Error as e:
        print(f"Не удалось инициализировать базу данных: {e}")


def add_word(english_word: str, russian_translation: str, db_path: Path = Path(DATABASE_NAME)) -> None:
    """Позволяет пользователю добавить новое слово и перевод."""
    sql_insert = """INSERT INTO words (english_word, russian_translation) VALUES (?, ?)"""
    if english_word == "" or russian_translation == "":
        raise ValueError("Английское слово и русский перевод не могут быть пустыми.")
    try:
        with Connect(db_path) as cursor:
            cursor.execute(sql_insert, (english_word.lower().strip(), russian_translation.lower().strip()))
        print("🆕✅ Слово добавлено в словарь.")
    except sqlite3.Error as e:
        print(f"Дідько!!! Не удалось добавить слово в базу данных: {e}")
        raise ValueError

def log_answer(word_id: int, timestamp: str, test_type: str, is_correct: int, db_path: Path = Path(DATABASE_NAME))-> None:
    sql_insert_log = """INSERT INTO answers (word_id, timestamp, test_type, is_correct) VALUES (?, ?, ?, ?)"""
    try:
        with Connect(db_path) as cursor:
            cursor.execute(sql_insert_log, (word_id, timestamp, test_type, is_correct))
        # print(f"Log добавлен. word_id={word_id} timestamp={timestamp} test_type={test_type} is_correct={is_correct}")
    except sqlite3.Error as e:
        print(f"Не удалось добавить log_answer в базу данных: {e}")
        raise ValueError

def view_overall_stats(db_path: Path = Path(DATABASE_NAME))->list:
    """
    Показывает агрегированную статистику по каждому слову в словаре:
    общее количество, верные/неверные ответы, процент верных.
    """
    sql = """
    SELECT
        w.english_word,
        w.russian_translation,
        COUNT(a.id) AS total,
        SUM(CASE WHEN a.is_correct = 1 THEN 1 ELSE 0 END) AS correct,
        SUM(CASE WHEN a.is_correct = 0 THEN 1 ELSE 0 END) AS incorrect,
        CASE 
            WHEN COUNT(a.id) > 0 THEN
                ROUND(100.0 * SUM(CASE WHEN a.is_correct = 1 THEN 1 ELSE 0 END) / COUNT(a.id), 2)
            ELSE NULL
        END AS accuracy
    FROM words w
    LEFT JOIN answers a ON w.id = a.word_id
    GROUP BY w.id
    ORDER BY w.english_word;
    """
    try:
        with Connect(db_path) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    except sqlite3.Error as e:
        raise ValueError(f"Не удалось получить общую статистику: {e}")


def view_problem_words(limit: int =5, min_attempts: int = 1, db_path: Path = Path(DATABASE_NAME))-> list[tuple[str, str, int, int, int, float]]:
    """Args:
        limit (int): Максимальное количество слов для вывода (топ N).
        min_attempts (int): Минимальное количество попыток для слова, чтобы оно было включено в выборку.
    """
    sql_problematic = """
    SELECT
        w.english_word,
        w.russian_translation,
        COUNT(a.id) AS total_attempts,
        SUM(CASE WHEN a.is_correct = 0 THEN 1 ELSE 0 END) AS wrong_answers,
        SUM(CASE WHEN a.is_correct = 1 THEN 1 ELSE 0 END) AS correct_answers,
        ROUND(100.0 * SUM(CASE WHEN a.is_correct = 1 THEN 1 ELSE 0 END) / COUNT(a.id), 2) AS accuracy
    FROM words w
    JOIN answers a ON w.id = a.word_id
    GROUP BY w.id
    HAVING total_attempts >= ?
    ORDER BY accuracy ASC
    LIMIT ?;
    """
    try:
        with Connect(db_path) as cursor:
            cursor.execute(sql_problematic, (min_attempts, limit))
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Не удалось получить проблемные слова: {e}")

def view_words(db_path: Path = Path(DATABASE_NAME)) -> list:
    """Отображает все слова в словаре."""
    sql_select = "SELECT english_word, russian_translation FROM words"
    try:
        with Connect(db_path) as cursor:
            cursor.execute(sql_select)
            rows = cursor.fetchall()
            return rows
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Не удалось получить слова из базы данных: {e}")


def get_words(db_path: Path = Path(DATABASE_NAME)) -> list:
    sql = "SELECT id, english_word, russian_translation FROM words"
    try:
        with Connect(db_path) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        if not rows:
            print("❗ Словарь пуст. Добавьте слова, для запуска теста.")
            return []
        return rows #all_words
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Не удалось получить слова из базы данных: {e}")

def delete_word(english_word: str, db_path: Path = Path(DATABASE_NAME)) -> int:
    """Удаляет слово из словаря по английскому слову."""
    sql_delete = """DELETE FROM words WHERE english_word = ?"""
    try:
        with Connect(db_path) as cursor:
            cursor.execute(sql_delete, (english_word,))
            return cursor.rowcount
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Не удалось удалить слово из базы данных: {e}")


def get_all_tables(db_path: Path = Path(DATABASE_NAME)):
    """Вспомогательная функция для получения списка всех таблиц в БД (для тестов)."""
    with Connect(db_path) as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]


def get_table_info(db_path: Path = Path(DATABASE_NAME), table_name: str=""):
    """Вспомогательная функция для получения информации о таблице (для тестов)."""
    with Connect(db_path) as cursor:
        cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()
