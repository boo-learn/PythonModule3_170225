import sqlite3
import random
from datetime import datetime

import database
from helpers.connection import Connect
from pathlib import Path

PATH_TO_DB = Path('vocabulary.db')

def choose_test_type()->str:
    print("  🧠 Выберите тип теста:")
    print("       1️⃣ Английский ➡️ Русский (en_ru)")
    print("       2️⃣ Русский ➡️ Английский (ru_en)")
    while True:
        choice = input("Введите 1️⃣ / 2️⃣: ").strip()
        if choice == '1':
            return 'en_ru'
        elif choice == '2':
            return 'ru_en'
        else:
            print("       ⚠️ Неверный выбор. Пожалуйста, введите 1 или 2.")

def show_words(PATH_TO_DB):
    rows = database.view_words(PATH_TO_DB)
    if rows:
        print(f"🗂️    {'Слово':<13} |   {'Перевод':<13} |")
        for index, row in enumerate(rows):
            print(f" \033[31m{index +1}\033[0m    \033[94m{row[0]:<13}\033[0m |   \033[93m{row[1]:<13}\033[0m |")
    else:
        print("❗ Словарь пуст.")
    input("\033[90m<-press Enter->\033[0m")

def start_test(PATH_TO_DB):
    """Запускает режим тестирования."""
    all_words = database.get_words(PATH_TO_DB)
    if not all_words:
        return

    flag = True
    correct_answers_session = 0
    total_questions = 0
    test_type = choose_test_type()

    if test_type == 'en_ru':
        # Для en_ru: вопрос по english_word, ожидаем russian_translation
        get_question_word = lambda word_data: word_data[1]  # english_word
        get_expected_answer = lambda word_data: word_data[2]  # russian_translation
        exit_test = "exit"
        print(f"▶️ Начинаем тест на перевод с EN на RU")
    else:# ru_en
        # Для ru_en: вопрос по russian_translation, ожидаем english_word
        get_question_word = lambda word_data: word_data[2]  # russian_translation
        get_expected_answer = lambda word_data: word_data[1]  # english_word
        exit_test = "стоп"
        print(f"▶️ Начинаем тест на перевод с RU на EN")
    while flag:
        new_all_words = random.sample(all_words, len(all_words))
        for word_id, english_word, russian_translation in new_all_words:
            # Получаем слово для вопроса и ожидаемый ответ в зависимости от типа теста
            question_word = get_question_word((word_id, english_word, russian_translation))
            # print(f"question_word={question_word}")
            expected_answer = get_expected_answer((word_id, english_word, russian_translation))
            # print(f"expected_answer={expected_answer}")
            print(f"🧠 Как переводится \033[94m'{question_word}'\033[0m?")
            user_input = input(f"\033[91m'{exit_test}'\033[0m для выхода или ✍️ Введите ваш ответ: ").strip().lower()

            if user_input == exit_test:
                print("\n🛑 Тест остановлен пользователем.")
                flag = False
                break
            if user_input == expected_answer:
                correct_answers_session += 1
                is_correct = 1
                print("✅ Верно!\n")
            else:
                is_correct = 0
                print(f"❌ Неверно. Правильный перевод: \033[93m'{expected_answer}'\033[0m.\n")
            # print("-" * 20)  # Разделитель для следующего вопроса
            total_questions += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            database.log_answer(word_id, timestamp,test_type ,is_correct ,PATH_TO_DB)
    print(f"📊 Статистика:\n   Всего вопросов: {total_questions}\n   Правильных: {correct_answers_session} 📈\n"
          f"   Ошибок: {total_questions - correct_answers_session} ❌\n")
    input("\033[90m<-press Enter->\033[0m")



def view_overall_status(PATH_TO_DB):
    rows = database.view_overall_stats(PATH_TO_DB)
    print("\n--- 📊 Общая статистика по словам ---")
    print(f"   {'Слово':<15} | {'Перевод':<15} | Всего | \033[92m✔\033[0m Верно | ✘ Неверно | Точность %")
    print("-" * 75)
    for index, row in enumerate(rows):
        eng, rus, total, correct, incorrect, accuracy = row
        accuracy_str = f"{accuracy}%" if accuracy is not None else "—"
        print(f"\033[31m{index +1}.\033[0m \033[94m{eng:<15}\033[0m | \033[93m{rus:<15}\033[0m | {total:^5} | \033[92m{correct:^7}\033[0m | {incorrect:^9} | {accuracy_str:^10}")
    input("\033[90m<-press Enter->\033[0m")

def get_problem_words(PATH_TO_DB):
    limit = 5           # Максимальное количество слов для вывода (топ N).
    min_attempts = 1    # Минимальное количество попыток для слова, чтобы оно было включено в выборку.
    # ANSI-коды # Оттенки от красного (яркий) до серого (тусклый)
    gradient_colors = [196, 160, 131, 102, 245]
    reset = "\033[0m"
    try:
        problem_words = database.view_problem_words(limit, min_attempts, PATH_TO_DB)
        if not problem_words:
            print("Пока нет слов, достаточно протестированных для выявления проблемных, "
                  "или по всем словам хорошие результаты.")
        else:
            print("\n--- 🔍 Проблемные слова TOP 5 ---")
            print(f"  {'Слово':<13} |   {'Перевод':<13} | Всего | ✔ Верно | ✘ Неверно | Точность %")
            print("-" * 75)
            for index, word in enumerate(problem_words):
                en, ru, total, wrong, correct, acc = word
                if index >= len(gradient_colors) - 1: # если limit > 5 делаем защиту, что бы не вылететь за пределы массива gradient_colors
                    index = len(gradient_colors) - 1
                color = f"\033[38;5;{gradient_colors[index]}m"
                print(f"{color}  {en:<13} |   {ru:<13} | {total:^5} | {correct:^7} | {wrong:^9} | {acc:^10}%{reset}")
        input("\033[90m<-press Enter->\033[0m")
    except sqlite3.Error as e:
        print(f"Ошибка при получении проблемных слов: {e}")

def delete_word_db(english, PATH_TO_DB) -> None:
    count = database.delete_word(english, PATH_TO_DB)
    if count == 0:
        print(f"❗ Слово \033[31m{english}\033[0m в словаре не найдено")
    else:
        print(f"🗑️ Слово \033[31m{english}\033[0m удалено!")


def main_menu(PATH_TO_DB):
    """Главное меню приложения."""
    while True:
        print("\n--- 📘 Меню приложения 'Английский для новичков' ---")
        print(" 1. ➕ Добавить слово")
        print(" 2. 🗂️ Посмотреть слова")
        print(" 3. 🗑️ Удалить слово")
        print(" 4. ▶️ Начать тест")
        print(" 5. 📊 Общая статистика по словам")
        print(" 6. 🐌 Слова с проблемами")
        print(" 7. 🚪 Выход")
        print("-------------------------------------------------")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            english = input("📥 Введите английское слово: ").strip().lower()
            russian = input("📥 Введите русский перевод: ").strip().lower()
            database.add_word(english, russian, PATH_TO_DB)
        elif choice == '2':
            show_words(PATH_TO_DB)
        elif choice == '3':
            english = input("🗑️ Введите английское слово, которое хотите удалить: ").strip().lower()
            delete_word_db(english, PATH_TO_DB)
        elif choice == '4':
            start_test(PATH_TO_DB)
        elif choice == '5':
            view_overall_status(PATH_TO_DB)
        elif choice == '6':
            get_problem_words(PATH_TO_DB)
        elif choice == '7':
            print("👋 До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 5.")


if __name__ == "__main__":
    database.init_db(PATH_TO_DB)
    main_menu(PATH_TO_DB)
