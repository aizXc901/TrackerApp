import sqlite3
import os
from datetime import datetime, date, timedelta


class Database:
    def __init__(self, db_path="habits.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Таблица привычек (пользователь задает баллы)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                habit_type TEXT CHECK(habit_type IN ('develop', 'quit')) NOT NULL,
                points INTEGER DEFAULT 1,
                reminder_time TEXT,
                created_date DATE DEFAULT CURRENT_DATE
            )
        ''')

        # Таблица выполнения привычек
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                completion_date DATE NOT NULL,
                notes TEXT,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        ''')

        # Таблица заметок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_date DATE NOT NULL,
                title TEXT,
                content TEXT,
                image_path TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def get_total_completions_count(self):
        """Получить общее количество выполнений всех привычек"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM habit_completions')
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def add_habit(self, name, description, habit_type, points=1, reminder_time=None):
        """Добавление новой привычки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO habits (name, description, habit_type, points, reminder_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, habit_type, points, reminder_time))
        habit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return habit_id

    def get_all_habits(self):
        """Получение всех привычек"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habits')
        habits = cursor.fetchall()
        conn.close()
        return habits

    def mark_habit_completed(self, habit_id, completion_date=None, notes=None):
        """Отметка выполнения привычки"""
        if completion_date is None:
            completion_date = date.today().isoformat()
        else:
            completion_date = completion_date.isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Сначала проверим, существует ли уже такая запись
        cursor.execute('''
            SELECT COUNT(*) FROM habit_completions 
            WHERE habit_id = ? AND completion_date = ?
        ''', (habit_id, completion_date))

        existing_count = cursor.fetchone()[0]

        if existing_count > 0:
            print(f"⚠️ WARNING: Привычка {habit_id} уже отмечена как выполненная на {completion_date}")
            conn.close()
            return

        cursor.execute('''
            INSERT INTO habit_completions (habit_id, completion_date, notes)
            VALUES (?, ?, ?)
        ''', (habit_id, completion_date, notes))

        # Получим информацию о привычке для отладки
        cursor.execute('SELECT name, points, habit_type FROM habits WHERE id = ?', (habit_id,))
        habit_info = cursor.fetchone()

        print(f"✅ DEBUG: Привычка '{habit_info[0]}' отмечена как выполненная")
        print(f"✅ DEBUG: Баллы: {habit_info[1]}, Тип: {habit_info[2]}, Дата: {completion_date}")

        conn.commit()
        conn.close()

    def check_habit_completion(self, habit_id, date):
        """Проверяем, выполнена ли привычка в указанную дату"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM habit_completions 
            WHERE habit_id = ? AND completion_date = ?
        ''', (habit_id, date.isoformat()))

        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def get_habit_completions_for_date(self, date):
        """Получаем все выполнения привычек за указанную дату"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT h.id, h.name, h.habit_type 
            FROM habits h
            JOIN habit_completions hc ON h.id = hc.habit_id
            WHERE hc.completion_date = ?
        ''', (date.isoformat(),))

        completions = cursor.fetchall()
        conn.close()
        return completions

    def remove_habit_completion(self, habit_id, completion_date):
        """Удаление отметки о выполнении привычки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM habit_completions 
            WHERE habit_id = ? AND completion_date = ?
        ''', (habit_id, completion_date.isoformat()))

        conn.commit()
        conn.close()

    def calculate_total_points(self):
        """Рассчитываем общее количество баллов"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        print(f"🔍 DEBUG: Расчет общих баллов")

        # Суммируем баллы за выполненные привычки "развивать"
        cursor.execute('''
            SELECT h.id, h.name, h.points, h.habit_type
            FROM habit_completions hc
            JOIN habits h ON hc.habit_id = h.id
            WHERE h.habit_type = 'develop'
        ''')

        positive_habits = cursor.fetchall()
        positive_points = sum(habit[2] for habit in positive_habits) if positive_habits else 0

        print(f"🔍 DEBUG: Все привычки 'развивать':")
        for habit in positive_habits:
            print(f"  - {habit[1]}: {habit[2]} баллов (ID: {habit[0]})")
        print(f"🔍 DEBUG: Всего баллов за 'развивать': {positive_points}")

        # Вычитаем баллы за выполненные привычки "избавиться"
        cursor.execute('''
            SELECT h.id, h.name, h.points, h.habit_type
            FROM habit_completions hc
            JOIN habits h ON hc.habit_id = h.id
            WHERE h.habit_type = 'quit'
        ''')

        negative_habits = cursor.fetchall()
        negative_points = sum(habit[2] for habit in negative_habits) if negative_habits else 0

        print(f"🔍 DEBUG: Все привычки 'избавиться':")
        for habit in negative_habits:
            print(f"  - {habit[1]}: -{habit[2]} баллов (ID: {habit[0]})")
        print(f"🔍 DEBUG: Всего баллов за 'избавиться': -{negative_points}")

        total_points = positive_points - negative_points
        print(f"🔍 DEBUG: ОБЩИЙ ИТОГ: {total_points} баллов")

        conn.close()
        return total_points

    def calculate_points_for_period(self, period="today"):
        """Рассчитываем баллы за период"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Определяем даты периода
        today = date.today()
        if period == "today":
            start_date = today
            end_date = today
        elif period == "week":
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif period == "month":
            start_date = today.replace(day=1)
            end_date = today
        else:
            start_date = today
            end_date = today

        print(f"🔍 DEBUG: Расчет баллов за период {period}")
        print(f"🔍 DEBUG: Дата начала: {start_date}, Дата окончания: {end_date}")

        # Баллы за привычки "развивать"
        cursor.execute('''
            SELECT h.id, h.name, h.points, h.habit_type
            FROM habit_completions hc
            JOIN habits h ON hc.habit_id = h.id
            WHERE h.habit_type = 'develop' 
            AND hc.completion_date BETWEEN ? AND ?
        ''', (start_date.isoformat(), end_date.isoformat()))

        positive_habits = cursor.fetchall()
        positive_points = sum(habit[2] for habit in positive_habits) if positive_habits else 0

        print(f"🔍 DEBUG: Привычки 'развивать' за период:")
        for habit in positive_habits:
            print(f"  - {habit[1]}: {habit[2]} баллов (ID: {habit[0]})")
        print(f"🔍 DEBUG: Всего баллов за 'развивать': {positive_points}")

        # Баллы за привычки "избавиться" (вычитаем)
        cursor.execute('''
            SELECT h.id, h.name, h.points, h.habit_type
            FROM habit_completions hc
            JOIN habits h ON hc.habit_id = h.id
            WHERE h.habit_type = 'quit' 
            AND hc.completion_date BETWEEN ? AND ?
        ''', (start_date.isoformat(), end_date.isoformat()))

        negative_habits = cursor.fetchall()
        negative_points = sum(habit[2] for habit in negative_habits) if negative_habits else 0

        print(f"🔍 DEBUG: Привычки 'избавиться' за период:")
        for habit in negative_habits:
            print(f"  - {habit[1]}: -{habit[2]} баллов (ID: {habit[0]})")
        print(f"🔍 DEBUG: Всего баллов за 'избавиться': -{negative_points}")

        total_points = positive_points - negative_points
        print(f"🔍 DEBUG: ИТОГО баллов за период: {total_points}")

        conn.close()
        return total_points

    def debug_habit_completions(self):
        """Отладочный метод для проверки всех выполненных привычек"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT hc.id, hc.habit_id, h.name, h.habit_type, h.points, hc.completion_date
            FROM habit_completions hc
            JOIN habits h ON hc.habit_id = h.id
            ORDER BY hc.completion_date DESC
        ''')

        completions = cursor.fetchall()

        print("🔍 DEBUG: Все выполненные привычки в базе:")
        print("ID | Habit_ID | Name | Type | Points | Date")
        print("-" * 60)
        for comp in completions:
            print(f"{comp[0]} | {comp[1]} | {comp[2]} | {comp[3]} | {comp[4]} | {comp[5]}")

        conn.close()
        return completions

    def add_note(self, note_date, title, content, image_path=None):
        """Добавление новой заметки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO notes (note_date, title, content, image_path)
            VALUES (?, ?, ?, ?)
        ''', (note_date.isoformat(), title, content, image_path))
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return note_id

    def get_notes_for_date(self, date):
        """Получение заметок за указанную дату"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM notes 
            WHERE note_date = ?
            ORDER BY id DESC
        ''', (date.isoformat(),))
        notes = cursor.fetchall()
        conn.close()
        return notes

    def get_all_notes(self):
        """Получение всех заметок"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM notes 
            ORDER BY note_date DESC, id DESC
        ''')
        notes = cursor.fetchall()
        conn.close()
        return notes

    def delete_note(self, note_id):
        """Удаление заметки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        conn.close()

    def get_habit_completion_count(self, habit_id):
        """Подсчет количества выполнений привычки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM habit_completions 
            WHERE habit_id = ?
        ''', (habit_id,))

        count = cursor.fetchone()[0]
        conn.close()
        return count

    def habit_exists(self, habit_id):
        """Проверяет, существует ли привычка"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM habits WHERE id = ?', (habit_id,))
        count = cursor.fetchone()[0]
        conn.close()

        return count > 0

    def get_habits_with_reminders(self):
        """Получение привычек с напоминаниями"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM habits 
            WHERE reminder_time IS NOT NULL AND habit_type = 'develop'
        ''')
        habits = cursor.fetchall()
        conn.close()
        return habits

    def update_reminder_time(self, habit_id, reminder_time):
        """Обновление времени напоминания"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE habits 
            SET reminder_time = ? 
            WHERE id = ?
        ''', (reminder_time, habit_id))
        conn.commit()
        conn.close()

    def delete_habit(self, habit_id):
        """Удаление привычки и всех связанных данных"""
        # Сначала проверяем, существует ли привычка
        if not self.habit_exists(habit_id):
            print(f"Привычка {habit_id} не найдена")
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Сначала удаляем все выполнения этой привычки
            cursor.execute('DELETE FROM habit_completions WHERE habit_id = ?', (habit_id,))

            # Затем удаляем саму привычку
            cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))

            conn.commit()
            print(f"Привычка {habit_id} и все её выполнения удалены")
            return True

        except Exception as e:
            conn.rollback()
            print(f"Ошибка при удалении привычки: {e}")
            return False
        finally:
            conn.close()

