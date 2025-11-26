import customtkinter as ctk
from datetime import datetime, date
import calendar
from typing import Optional
import os
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Pillow не установлен. Функционал изображений будет ограничен.")


class ModernCalendarWidget:
    """Современный виджет календаря с улучшенным дизайном"""

    def __init__(self, parent, on_date_select=None):
        self.parent = parent
        self.on_date_select = on_date_select
        self.current_date = date.today()
        self.selected_date = None
        self.setup_calendar()

    def setup_calendar(self):
        """Настройка современного календаря"""
        self.calendar_frame = ctk.CTkFrame(self.parent, fg_color="transparent")

        # Основной контейнер с карточным дизайном
        self.main_container = ctk.CTkFrame(
            self.calendar_frame,
            corner_radius=20,
            fg_color="#2b2b2b"
        )
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.create_header()
        self.create_week_days()
        self.create_calendar_grid()

    def create_header(self):
        """Создание современного заголовка"""
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)

        # Навигация
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.pack(fill="x")

        # Кнопка предыдущий месяц
        prev_btn = ctk.CTkButton(
            nav_frame, text="‹", width=45, height=45,
            command=self.previous_month,
            fg_color="transparent",
            hover_color="#3a3a3a",
            font=ctk.CTkFont(size=20, weight="bold"),
            corner_radius=10
        )
        prev_btn.pack(side="left", padx=5)

        # Текущий месяц и год
        self.month_year_label = ctk.CTkLabel(
            nav_frame,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        self.month_year_label.pack(side="left", expand=True, padx=10)

        # Кнопка следующий месяц
        next_btn = ctk.CTkButton(
            nav_frame, text="›", width=45, height=45,
            command=self.next_month,
            fg_color="transparent",
            hover_color="#3a3a3a",
            font=ctk.CTkFont(size=20, weight="bold"),
            corner_radius=10
        )
        next_btn.pack(side="right", padx=5)

        # Кнопка сегодня
        today_btn = ctk.CTkButton(
            nav_frame, text="Сегодня",
            command=self.go_to_today,
            fg_color="#4CC9F0",
            hover_color="#3a9bc8",
            width=90,
            height=35,
            corner_radius=8
        )
        today_btn.pack(side="right", padx=10)

        self.update_header()

    def update_header(self):
        """Обновление заголовка"""
        month_name = calendar.month_name[self.current_date.month]
        year = self.current_date.year
        self.month_year_label.configure(text=f"{month_name} {year}")

    def create_week_days(self):
        """Создание заголовков дней недели"""
        # Убираем старый фрейм, если он есть
        if hasattr(self, 'days_header_frame'):
            self.days_header_frame.destroy()

        self.days_header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.days_header_frame.pack(fill="x", padx=20, pady=10)

        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for col_idx, day in enumerate(days):
            is_weekend = col_idx >= 5
            day_label = ctk.CTkLabel(
                self.days_header_frame,
                text=day,
                width=45,
                height=35,
                font=ctk.CTkFont(weight="bold"),
                text_color="#FF6B6B" if is_weekend else "#ffffff",
                anchor="center"
            )
            day_label.grid(row=0, column=col_idx, padx=2, sticky="nsew")

        # Равномерное распределение по столбцам
        for col in range(7):
            self.days_header_frame.grid_columnconfigure(col, weight=1)

    def create_calendar_grid(self):
        """Создание сетки календаря"""
        self.days_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.days_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Настройка сетки
        for col in range(7):
            self.days_frame.grid_columnconfigure(col, weight=1)

        self.update_calendar()

    def update_calendar(self):
        """Обновление календаря"""
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        today = date.today()

        # Создаем grid-сетку
        for row_idx, week in enumerate(cal):
            for col_idx, day in enumerate(week):
                if day == 0:
                    # Пустая ячейка
                    empty_label = ctk.CTkLabel(
                        self.days_frame,
                        text="",
                        width=45,
                        height=45,
                        fg_color="transparent"
                    )
                    empty_label.grid(row=row_idx, column=col_idx, padx=2, pady=2)
                    continue

                current_date = date(self.current_date.year, self.current_date.month, day)
                is_today = (current_date == today)
                is_selected = (self.selected_date == current_date)
                is_weekend = current_date.weekday() >= 5

                # Стилизация
                if is_selected:
                    fg_color = "#4CC9F0"
                    text_color = "#ffffff"
                elif is_today:
                    fg_color = "#FFEB3B"
                    text_color = "#000000"
                elif is_weekend:
                    fg_color = "#3a3a3a"
                    text_color = "#FF6B6B"
                else:
                    fg_color = "#2b2b2b"
                    text_color = "#ffffff"

                # Создаем кнопку
                day_btn = ctk.CTkButton(
                    self.days_frame,
                    text=str(day),
                    fg_color=fg_color,
                    hover_color=fg_color,
                    text_color=text_color,
                    font=ctk.CTkFont(weight="bold" if is_today else "normal"),
                    width=45,
                    height=45,
                    corner_radius=22,
                    border_width=0,
                    anchor="center"
                )
                day_btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)

                # Привязываем команду
                if self.on_date_select:
                    day_btn.configure(command=lambda d=current_date: self.select_date(d))

    def select_date(self, selected_date):
        """Выбор даты"""
        self.selected_date = selected_date
        self.update_calendar()
        if self.on_date_select:
            self.on_date_select(selected_date)

    def previous_month(self):
        """Переход к предыдущему месяцу"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_header()
        self.update_calendar()

    def next_month(self):
        """Переход к следующему месяцу"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_header()
        self.update_calendar()

    def go_to_today(self):
        """Переход к сегодняшней дате"""
        self.current_date = date.today()
        self.selected_date = self.current_date
        self.update_header()
        self.update_calendar()

    def pack(self, **kwargs):
        """Упаковка виджета"""
        self.calendar_frame.pack(**kwargs)

    def get_selected_date(self) -> Optional[date]:
        """Получить выбранную дату"""
        return self.selected_date


class ModernHabitTrackerApp:
    def __init__(self):
        from database import Database
        self.db = Database()

        # Настройка современной темы
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("🌱 Трекер Привычек - Развитие 360")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 750)

        # Привязываем клавишу Escape для выхода из полноэкранного режима
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())

        # Центрируем окно
        self.center_window()
        self.setup_ui()
        self.setup_reminders()

    def exit_fullscreen(self):
        """Выход из полноэкранного режима по Escape"""
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
            self.root.geometry("1200x900")
            self.center_window()

    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Настройка современного пользовательского интерфейса"""
        # Основной контейнер с отступами
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        """Создание современной боковой панели"""
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            width=280,
            corner_radius=20,
            fg_color="#2b2b2b"
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 20))
        self.sidebar.pack_propagate(False)

        # Заголовок
        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(pady=30, padx=20, fill="x")

        title_label = ctk.CTkLabel(
            title_frame,
            text="🌱 Трекер Привычек",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Ваш путь к лучшей версии себя",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        subtitle_label.pack(pady=(5, 0))

        # Навигация
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=15, pady=30)

        buttons = [
            ("📅", "Календарь", self.show_calendar),
            ("➕", "Новая привычка", self.add_habit),
            ("📝", "Заметки", self.show_notes),  # <-- ДОБАВЬТЕ ЭТУ СТРОЧКУ
            ("📊", "Отчеты", self.show_reports)
        ]

        for icon, text, command in buttons:
            btn = ctk.CTkButton(
                nav_frame,
                text=f"   {icon}  {text}",
                command=command,
                fg_color="transparent",
                hover_color="#3a3a3a",
                anchor="w",
                height=50,
                font=ctk.CTkFont(size=14),
                corner_radius=12
            )
            btn.pack(pady=8, fill="x")

        # Статистика внизу
        self.create_sidebar_stats()

    def create_sidebar_stats(self):
        """Создание блока статистики в сайдбаре"""
        stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        stats_frame.pack(side="bottom", fill="x", padx=15, pady=20)

        # Разделитель
        separator = ctk.CTkFrame(stats_frame, height=1, fg_color="#444444")
        separator.pack(fill="x", pady=10)

        # Текущая статистика
        stats_label = ctk.CTkLabel(
            stats_frame,
            text="Сегодняшний прогресс",
            font=ctk.CTkFont(weight="bold"),
            text_color="#888888"
        )
        stats_label.pack(anchor="w", pady=(0, 10))

        self.today_stats_label = ctk.CTkLabel(
            stats_frame,
            text="Загрузка...",
            font=ctk.CTkFont(size=12),
            text_color="#4CC9F0"
        )
        self.today_stats_label.pack(anchor="w")

        # Обновляем статистику
        self.update_sidebar_stats()

    def update_sidebar_stats(self):
        """Обновление статистики в сайдбаре"""
        try:
            habits = self.db.get_all_habits()
            today = date.today()
            completed_count = self.get_completed_habits_count(habits, today)
            total_count = len(habits)

            if total_count > 0:
                progress = f"{completed_count}/{total_count} привычек"
                percentage = (completed_count / total_count) * 100
                self.today_stats_label.configure(
                    text=f"{progress} ({percentage:.0f}%)"
                )
            else:
                self.today_stats_label.configure(text="Добавьте первую привычку!")
        except:
            self.today_stats_label.configure(text="Ошибка загрузки")

    def create_main_content(self):
        """Создание основной области контента"""
        self.main_content = ctk.CTkFrame(
            self.main_container,
            corner_radius=20,
            fg_color="#1a1a1a"
        )
        self.main_content.pack(side="right", expand=True, fill="both")

        # Приветственный экран
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Показать современный приветственный экран с гайдом"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Основной контейнер с прокруткой для гайда
        scroll_container = ctk.CTkScrollableFrame(self.main_content, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True, padx=20, pady=20)

        welcome_container = ctk.CTkFrame(scroll_container, fg_color="transparent")
        welcome_container.pack(expand=True, fill="both", pady=20)

        # Анимированная иконка
        icon_label = ctk.CTkLabel(
            welcome_container,
            text="🌱",
            font=ctk.CTkFont(size=80)
        )
        icon_label.pack(pady=20)

        welcome_label = ctk.CTkLabel(
            welcome_container,
            text="Добро пожаловать в Трекер Привычек!",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        welcome_label.pack(pady=10)

        subtitle_label = ctk.CTkLabel(
            welcome_container,
            text="Ваш персональный помощник в формировании хороших привычек",
            font=ctk.CTkFont(size=16),
            text_color="#888888"
        )
        subtitle_label.pack(pady=5)

        # Кнопка полноэкранного режима
        fullscreen_frame = ctk.CTkFrame(welcome_container, fg_color="transparent")
        fullscreen_frame.pack(pady=20)

        fullscreen_btn = ctk.CTkButton(
            fullscreen_frame,
            text="🖥️ Развернуть на полный экран",
            command=self.toggle_fullscreen,
            fg_color="#6C63FF",
            hover_color="#5a52d6",
            width=220,
            height=40,
            font=ctk.CTkFont(size=13),
            corner_radius=10
        )
        fullscreen_btn.pack(pady=5)

        # Гайд по использованию
        guide_frame = ctk.CTkFrame(welcome_container, fg_color="#2b2b2b", corner_radius=15)
        guide_frame.pack(pady=30, padx=50, fill="x")

        # Заголовок гайда
        guide_title = ctk.CTkLabel(
            guide_frame,
            text="📚 Краткий гайд по использованию",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        guide_title.pack(pady=20)

        # Шаги гайда
        steps = [
            {
                "icon": "➕",
                "title": "Добавьте привычки",
                "description": "Создайте привычки, которые хотите развивать или от которых хотите избавиться"
            },
            {
                "icon": "📅",
                "title": "Отмечайте выполнение",
                "description": "В календаре выбирайте дату и отмечайте выполненные привычки"
            },
            {
                "icon": "✅",
                "title": "Следите за прогрессом",
                "description": "Привычки для развития: отмечайте галочкой когда выполнили\nПривычки для избавления: оставляйте пустыми если устояли"
            },
            {
                "icon": "📊",
                "title": "Анализируйте статистику",
                "description": "В разделе отчетов смотрите ваш прогресс и достижения"
            },
            {
                "icon": "💰",
                "title": "Система баллов",
                "description": "Получайте баллы за хорошие привычки и теряйте за плохие\nСледите за общим счетом в отчетах"
            }
        ]

        for i, step in enumerate(steps):
            step_frame = ctk.CTkFrame(guide_frame, fg_color="transparent")
            step_frame.pack(fill="x", padx=30, pady=15)

            # Номер шага
            number_frame = ctk.CTkFrame(step_frame, fg_color="#4CC9F0", width=30, height=30, corner_radius=15)
            number_frame.pack(side="left", padx=(0, 15))
            number_frame.pack_propagate(False)

            ctk.CTkLabel(
                number_frame,
                text=str(i + 1),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ffffff"
            ).pack(expand=True)

            # Иконка и текст
            content_frame = ctk.CTkFrame(step_frame, fg_color="transparent")
            content_frame.pack(side="left", fill="x", expand=True)

            step_header = ctk.CTkFrame(content_frame, fg_color="transparent")
            step_header.pack(fill="x")

            ctk.CTkLabel(
                step_header,
                text=f"{step['icon']} {step['title']}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#4CC9F0"
            ).pack(side="left")

            ctk.CTkLabel(
                content_frame,
                text=step['description'],
                font=ctk.CTkFont(size=14),
                text_color="#cccccc",
                justify="left",
                wraplength=600
            ).pack(anchor="w", pady=(5, 0))

        # Советы по продуктивности
        tips_frame = ctk.CTkFrame(welcome_container, fg_color="#2b2b2b", corner_radius=15)
        tips_frame.pack(pady=20, padx=50, fill="x")

        tips_title = ctk.CTkLabel(
            tips_frame,
            text="💡 Советы для успеха",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        tips_title.pack(pady=15)

        tips = [
            "🎯 Начинайте с малого - добавляйте 1-2 привычки за раз",
            "📝 Будьте конкретны в формулировках привычек",
            "🔄 Регулярно проверяйте свой прогресс в календаре",
            "🎉 Отмечайте маленькие победы - это мотивирует",
            "📱 Используйте напоминания для регулярности",
            "💪 Не ругайте себя за пропуски - просто продолжайте"
        ]

        for tip in tips:
            tip_label = ctk.CTkLabel(
                tips_frame,
                text=tip,
                font=ctk.CTkFont(size=14),
                text_color="#aaaaaa",
                justify="left"
            )
            tip_label.pack(anchor="w", padx=30, pady=8)

        # Быстрые действия
        quick_actions_frame = ctk.CTkFrame(welcome_container, fg_color="transparent")
        quick_actions_frame.pack(pady=40)

        quick_btn1 = ctk.CTkButton(
            quick_actions_frame,
            text="📅 Открыть календарь",
            command=self.show_calendar,
            fg_color="#4CC9F0",
            hover_color="#3a9bc8",
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        quick_btn1.pack(pady=10)

        quick_btn2 = ctk.CTkButton(
            quick_actions_frame,
            text="➕ Добавить привычку",
            command=self.add_habit,
            fg_color="#2AA876",
            hover_color="#218c61",
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        quick_btn2.pack(pady=10)

        quick_btn3 = ctk.CTkButton(
            quick_actions_frame,
            text="📊 Посмотреть отчеты",
            command=self.show_reports,
            fg_color="#FFA500",
            hover_color="#e69500",
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        quick_btn3.pack(pady=10)

    def toggle_fullscreen(self):
        """Переключение полноэкранного режима"""
        # Получаем текущее состояние полноэкранного режима
        current_state = self.root.attributes('-fullscreen')

        if current_state:
            # Выход из полноэкранного режима
            self.root.attributes('-fullscreen', False)
            # Возвращаем нормальный размер окна
            self.root.geometry("1200x900")
            # Центрируем окно
            self.center_window()
        else:
            # Вход в полноэкранный режим
            self.root.attributes('-fullscreen', True)

        # Обновляем интерфейс
        self.root.update()

    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()

        # Если не в полноэкранном режиме, центрируем
        if not self.root.attributes('-fullscreen'):
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f'{width}x{height}+{x}+{y}')

    def show_calendar(self):
        """Показать улучшенный календарь привычек"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Основной контейнер
        main_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text="📅 Календарь привычек",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")

        # Две колонки
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Левая колонка - календарь
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # Правая колонка - информация
        right_frame = ctk.CTkFrame(content_frame, width=300, corner_radius=15, fg_color="#2b2b2b")
        right_frame.pack(side="right", fill="y", padx=(15, 0))
        right_frame.pack_propagate(False)

        # Создаем современный календарь
        self.calendar_widget = ModernCalendarWidget(
            left_frame,
            on_date_select=self.on_calendar_date_select
        )
        self.calendar_widget.pack(fill="both", expand=True)

        # Правая панель с информацией
        self.setup_calendar_sidebar(right_frame)
        self.update_calendar_sidebar()

    def setup_calendar_sidebar(self, parent):
        """Настройка правой панели календаря"""
        # Заголовок
        sidebar_title = ctk.CTkLabel(
            parent,
            text="Детали дня",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        sidebar_title.pack(pady=25, padx=20, anchor="w")

        # Выбранная дата
        self.selected_date_frame = ctk.CTkFrame(parent, fg_color="#3a3a3a", corner_radius=12)
        self.selected_date_frame.pack(fill="x", padx=20, pady=15)

        self.selected_date_label = ctk.CTkLabel(
            self.selected_date_frame,
            text="Выберите дату в календаре",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.selected_date_label.pack(pady=15)

        # Прогресс
        self.progress_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.progress_frame.pack(fill="x", padx=20, pady=20)

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4CC9F0"
        )
        self.progress_label.pack()

        self.motivation_label = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.motivation_label.pack(pady=5)

        # Кнопка управления
        self.open_day_btn = ctk.CTkButton(
            parent,
            text="📝 Открыть привычки дня",
            command=self.open_selected_day_habits,
            fg_color="#2AA876",
            hover_color="#218c61",
            height=45,
            font=ctk.CTkFont(weight="bold"),
            state="disabled",
            corner_radius=10
        )
        self.open_day_btn.pack(pady=20, padx=20, fill="x")

        # Быстрое управление
        quick_frame = ctk.CTkFrame(parent, fg_color="transparent")
        quick_frame.pack(fill="x", padx=20, pady=10)

        quick_label = ctk.CTkLabel(
            quick_frame,
            text="Быстрое управление:",
            font=ctk.CTkFont(weight="bold"),
            text_color="#888888"
        )
        quick_label.pack(anchor="w", pady=(0, 10))

        today_btn = ctk.CTkButton(
            quick_frame,
            text="🗓️ Перейти на сегодня",
            command=self.go_to_today,
            fg_color="transparent",
            hover_color="#3a3a3a",
            border_width=1,
            border_color="#444444",
            corner_radius=8
        )
        today_btn.pack(fill="x", pady=2)

    def on_calendar_date_select(self, selected_date):
        """Обработчик выбора даты в календаре"""
        self.selected_date = selected_date
        self.update_calendar_sidebar()
        self.open_day_btn.configure(state="normal")

    def update_calendar_sidebar(self):
        """Обновление правой панели календаря"""
        if hasattr(self, 'selected_date'):
            date_str = self.selected_date.strftime("%d %B %Y")
            self.selected_date_label.configure(text=f"📅 {date_str}")

            habits = self.db.get_all_habits()
            completed_count = self.get_completed_habits_count(habits, self.selected_date)
            total_count = len(habits)

            self.progress_label.configure(text=f"{completed_count}/{total_count}")

            if total_count > 0:
                completion_rate = completed_count / total_count
                motivation_text = self.get_motivation_message(completion_rate)
                self.motivation_label.configure(
                    text=motivation_text,
                    text_color=self.get_motivation_color(completion_rate)
                )
            else:
                self.motivation_label.configure(text="Добавьте привычки для отслеживания")

    def open_selected_day_habits(self):
        """Открыть привычки для выбранной даты"""
        if hasattr(self, 'selected_date'):
            self.open_day_habits(self.selected_date)

    def go_to_today(self):
        """Перейти к сегодняшней дате"""
        if hasattr(self, 'calendar_widget'):
            self.calendar_widget.go_to_today()

    def add_habit(self):
        """Добавить новую привычку с улучшенным UI"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        main_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title_label = ctk.CTkLabel(
            main_container,
            text="➕ Новая привычка",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)

        # Карточка формы
        form_card = ctk.CTkFrame(main_container, corner_radius=20, fg_color="#2b2b2b")
        form_card.pack(pady=20, padx=50, fill="both", expand=True)

        # Название привычки
        ctk.CTkLabel(
            form_card,
            text="Название привычки:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(30, 5), anchor="w", padx=30)

        name_entry = ctk.CTkEntry(
            form_card,
            placeholder_text="Например: Читать 30 минут в день",
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        name_entry.pack(pady=5, fill="x", padx=30)

        # Описание
        ctk.CTkLabel(
            form_card,
            text="Описание:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 5), anchor="w", padx=30)

        desc_entry = ctk.CTkEntry(
            form_card,
            placeholder_text="Краткое описание привычки",
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        desc_entry.pack(pady=5, fill="x", padx=30)

        # Тип привычки
        ctk.CTkLabel(
            form_card,
            text="Тип привычки:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 10), anchor="w", padx=30)

        habit_type_var = ctk.StringVar(value="develop")

        type_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        type_frame.pack(fill="x", padx=30, pady=5)

        develop_radio = ctk.CTkRadioButton(
            type_frame,
            text="Развивать ✅",
            variable=habit_type_var,
            value="develop",
            font=ctk.CTkFont(size=14)
        )
        develop_radio.pack(side="left", padx=(0, 20))

        quit_radio = ctk.CTkRadioButton(
            type_frame,
            text="Избавиться ❌",
            variable=habit_type_var,
            value="quit",
            font=ctk.CTkFont(size=14)
        )
        quit_radio.pack(side="left")

        # Напоминание (только для привычек развития)
        ctk.CTkLabel(
            form_card,
            text="⏰ Напоминание (только для развития):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 5), anchor="w", padx=30)

        reminder_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        reminder_frame.pack(fill="x", padx=30, pady=5)

        # Выбор времени
        hours = [f"{i:02d}" for i in range(24)]
        minutes = [f"{i:02d}" for i in range(60)]

        hour_var = ctk.StringVar(value="09")
        minute_var = ctk.StringVar(value="00")

        hour_combo = ctk.CTkComboBox(
            reminder_frame,
            values=hours,
            variable=hour_var,
            width=80
        )
        hour_combo.pack(side="left", padx=(0, 5))

        ctk.CTkLabel(
            reminder_frame,
            text=":",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")

        minute_combo = ctk.CTkComboBox(
            reminder_frame,
            values=minutes,
            variable=minute_var,
            width=80
        )
        minute_combo.pack(side="left", padx=(5, 10))

        # Чекбокс для включения/выключения напоминания
        reminder_var = ctk.BooleanVar(value=False)

        def on_habit_type_change():
            """Обновление доступности напоминания при смене типа привычки"""
            if habit_type_var.get() == "develop":
                reminder_checkbox.configure(state="normal")
                hour_combo.configure(state="normal")
                minute_combo.configure(state="normal")
            else:
                reminder_checkbox.configure(state="disabled")
                hour_combo.configure(state="disabled")
                minute_combo.configure(state="disabled")
                reminder_var.set(False)

        reminder_checkbox = ctk.CTkCheckBox(
            reminder_frame,
            text="Включить напоминание",
            variable=reminder_var,
            command=on_habit_type_change
        )
        reminder_checkbox.pack(side="left")

        # Изначально настраиваем состояние
        on_habit_type_change()

        # Привязываем изменение типа привычки к обновлению состояния напоминаний
        habit_type_var.trace('w', lambda *args: on_habit_type_change())

        # Фрейм для кнопок
        buttons_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        buttons_frame.pack(side="bottom", pady=30, fill="x", padx=30)

        # Настройка сетки для кнопок
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        def save_habit():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            habit_type = habit_type_var.get()

            # Формируем время напоминания
            reminder_time = None
            if habit_type == "develop" and reminder_var.get():
                reminder_time = f"{hour_var.get()}:{minute_var.get()}"

            if not name:
                self.show_error_message("Введите название привычки!")
                return

            try:
                habit_id = self.db.add_habit(name, description, habit_type, 1, reminder_time)
                self.show_success_message("Привычка успешно добавлена!")
                self.update_sidebar_stats()
                self.show_welcome_screen()
            except Exception as e:
                self.show_error_message(f"Ошибка: {str(e)}")

        # Кнопка сохранения
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Сохранить привычку",
            command=save_habit,
            fg_color="#2AA876",
            hover_color="#218c61",
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        save_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # Кнопка отмены
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Отмена",
            command=self.show_welcome_screen,
            fg_color="#FF6B6B",
            hover_color="#e05555",
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        cancel_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # Фокус на поле ввода названия
        name_entry.focus()

    def show_notes(self):
        """Показать функционал заметок"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        main_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title_label = ctk.CTkLabel(
            main_container,
            text="📝 Заметки и размышления",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)

        # Две колонки
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Левая колонка - форма добавления заметки
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # Правая колонка - список заметок
        right_frame = ctk.CTkFrame(content_frame, width=400, corner_radius=15, fg_color="#2b2b2b")
        right_frame.pack(side="right", fill="y", padx=(15, 0))
        right_frame.pack_propagate(False)

        # Форма добавления заметки
        self.create_note_form(left_frame)

        # Список заметок
        self.create_notes_list(right_frame)

    def create_note_form(self, parent):
        """Создать форму для добавления заметки"""
        form_card = ctk.CTkFrame(parent, corner_radius=20, fg_color="#2b2b2b")
        form_card.pack(fill="both", expand=True, pady=10)

        # Заголовок формы
        form_title = ctk.CTkLabel(
            form_card,
            text="✏️ Новая заметка",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        form_title.pack(pady=20)

        # Дата заметки
        ctk.CTkLabel(
            form_card,
            text="Дата заметки:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5), anchor="w", padx=30)

        # Используем текущую дату по умолчанию
        current_date = date.today()
        self.note_date_var = ctk.StringVar(value=current_date.strftime("%d.%m.%Y"))

        date_entry = ctk.CTkEntry(
            form_card,
            textvariable=self.note_date_var,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        date_entry.pack(pady=5, fill="x", padx=30)

        # Заголовок заметки
        ctk.CTkLabel(
            form_card,
            text="Заголовок:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 5), anchor="w", padx=30)

        self.note_title_entry = ctk.CTkEntry(
            form_card,
            placeholder_text="Краткий заголовок заметки",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        self.note_title_entry.pack(pady=5, fill="x", padx=30)

        # Текст заметки
        ctk.CTkLabel(
            form_card,
            text="Текст заметки:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 5), anchor="w", padx=30)

        self.note_text_area = ctk.CTkTextbox(
            form_card,
            height=120,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.note_text_area.pack(pady=5, fill="x", padx=30)

        # Загрузка изображения
        ctk.CTkLabel(
            form_card,
            text="Изображение (опционально):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 5), anchor="w", padx=30)

        image_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        image_frame.pack(fill="x", padx=30, pady=5)

        self.note_image_path = None
        self.note_image_label = ctk.CTkLabel(
            image_frame,
            text="Файл не выбран",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.note_image_label.pack(side="left")

        def select_image():
            """Выбор изображения"""
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                title="Выберите изображение",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
            )
            if file_path:
                self.note_image_path = file_path
                # Показываем только имя файла
                file_name = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
                self.note_image_label.configure(text=file_name)

        select_image_btn = ctk.CTkButton(
            image_frame,
            text="📁 Выбрать файл",
            command=select_image,
            width=120,
            height=35,
            fg_color="#4CC9F0",
            hover_color="#3a9bc8"
        )
        select_image_btn.pack(side="right")

        # Кнопка сохранения
        def save_note():
            """Сохранение заметки"""
            note_date_str = self.note_date_var.get()
            title = self.note_title_entry.get().strip()
            content = self.note_text_area.get("1.0", "end-1c").strip()

            if not title:
                self.show_error_message("Введите заголовок заметки!")
                return

            if not content:
                self.show_error_message("Введите текст заметки!")
                return

            try:
                # Парсим дату
                try:
                    day, month, year = map(int, note_date_str.split('.'))
                    note_date = date(year, month, day)
                except:
                    self.show_error_message("Неверный формат даты! Используйте ДД.ММ.ГГГГ")
                    return

                # Сохраняем заметку
                note_id = self.db.add_note(note_date, title, content, self.note_image_path)
                self.show_success_message("Заметка успешно сохранена!")

                # Очищаем форму
                self.note_title_entry.delete(0, 'end')
                self.note_text_area.delete("1.0", "end")
                self.note_image_path = None
                self.note_image_label.configure(text="Файл не выбран")

                # Обновляем список заметок
                self.refresh_notes_list()

            except Exception as e:
                self.show_error_message(f"Ошибка при сохранении: {str(e)}")

        save_btn = ctk.CTkButton(
            form_card,
            text="💾 Сохранить заметку",
            command=save_note,
            fg_color="#2AA876",
            hover_color="#218c61",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        save_btn.pack(pady=20, padx=30, fill="x")

    def create_notes_list(self, parent):
        """Создать список заметок"""
        # Заголовок
        list_title = ctk.CTkLabel(
            parent,
            text="📋 Ваши заметки",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        list_title.pack(pady=20)

        # Прокручиваемая область
        self.notes_scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.notes_scroll_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Загружаем заметки
        self.refresh_notes_list()

    def refresh_notes_list(self):
        """Обновить список заметок"""
        # Очищаем текущий список
        for widget in self.notes_scroll_frame.winfo_children():
            widget.destroy()

        # Загружаем заметки из базы
        notes = self.db.get_all_notes()

        if not notes:
            # Сообщение, если заметок нет
            empty_label = ctk.CTkLabel(
                self.notes_scroll_frame,
                text="У вас пока нет заметок.\nДобавьте первую заметку!",
                font=ctk.CTkFont(size=14),
                text_color="#888888",
                justify="center"
            )
            empty_label.pack(pady=50)
            return

        # Сортируем заметки по дате (новые сначала)
        notes.sort(key=lambda x: x[1], reverse=True)

        for note in notes:
            note_id, note_date, title, content, image_path = note
            self.create_note_card(note_id, note_date, title, content, image_path)

    def create_note_card(self, note_id, note_date, title, content, image_path):
        """Создать карточку заметки"""
        card = ctk.CTkFrame(self.notes_scroll_frame, corner_radius=12, fg_color="#3a3a3a")
        card.pack(pady=8, padx=5, fill="x")

        # Основная информация
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", expand=True, padx=15, pady=12)

        # Заголовок и дата
        header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        header_frame.pack(fill="x")

        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
            text_color="#4CC9F0"
        )
        title_label.pack(side="left", anchor="w")

        # Форматируем дату
        try:
            note_date_obj = datetime.strptime(note_date, "%Y-%m-%d").date()
            date_str = note_date_obj.strftime("%d.%m.%Y")
        except:
            date_str = note_date

        date_label = ctk.CTkLabel(
            header_frame,
            text=date_str,
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        date_label.pack(side="right", anchor="e")

        # Текст заметки (обрезаем если длинный)
        content_preview = content
        if len(content) > 100:
            content_preview = content[:100] + "..."

        content_label = ctk.CTkLabel(
            info_frame,
            text=content_preview,
            font=ctk.CTkFont(size=13),
            anchor="w",
            justify="left",
            text_color="#cccccc",
            wraplength=350
        )
        content_label.pack(fill="x", pady=(8, 0))

        # Индикатор изображения
        if image_path:
            image_indicator = ctk.CTkLabel(
                info_frame,
                text="🖼️ Есть изображение",
                font=ctk.CTkFont(size=11),
                text_color="#FFA500"
            )
            image_indicator.pack(anchor="w", pady=(5, 0))

        # Кнопки управления
        buttons_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 0))

        def view_note():
            """Просмотр полной заметки"""
            self.view_note_details(note_id, note_date, title, content, image_path)

        def delete_note():
            """Удаление заметки"""
            self.delete_note_confirmation(note_id, card)

        view_btn = ctk.CTkButton(
            buttons_frame,
            text="👁️ Просмотреть",
            command=view_note,
            width=100,
            height=30,
            fg_color="#4CC9F0",
            hover_color="#3a9bc8",
            font=ctk.CTkFont(size=11)
        )
        view_btn.pack(side="left", padx=(0, 5))

        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Удалить",
            command=delete_note,
            width=80,
            height=30,
            fg_color="transparent",
            hover_color="#FF6B6B",
            border_width=1,
            border_color="#FF6B6B",
            text_color="#FF6B6B",
            font=ctk.CTkFont(size=11)
        )
        delete_btn.pack(side="left")

    def view_note_details(self, note_id, note_date, title, content, image_path):
        """Просмотр деталей заметки с отображением изображения"""
        note_window = ctk.CTkToplevel(self.root)
        note_window.title(f"Заметка: {title}")
        note_window.geometry("600x700")
        note_window.transient(self.root)
        note_window.grab_set()

        # Центрируем
        note_window.update_idletasks()
        x = (note_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (note_window.winfo_screenheight() // 2) - (700 // 2)
        note_window.geometry(f"600x700+{x}+{y}")

        main_container = ctk.CTkScrollableFrame(note_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Форматируем дату
        try:
            note_date_obj = datetime.strptime(note_date, "%Y-%m-%d").date()
            date_str = note_date_obj.strftime("%d %B %Y")
        except:
            date_str = note_date

        # Дата
        date_label = ctk.CTkLabel(
            main_container,
            text=f"📅 {date_str}",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        date_label.pack(anchor="w", pady=(0, 10))

        # Заголовок
        title_label = ctk.CTkLabel(
            main_container,
            text=title,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#4CC9F0",
            wraplength=550
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # Текст заметки
        text_frame = ctk.CTkFrame(main_container, fg_color="#2b2b2b", corner_radius=10)
        text_frame.pack(fill="x", pady=10)

        content_label = ctk.CTkLabel(
            text_frame,
            text=content,
            font=ctk.CTkFont(size=14),
            text_color="#ffffff",
            justify="left",
            wraplength=550
        )
        content_label.pack(padx=15, pady=15, anchor="w")

        # Изображение (если есть)
        if image_path and os.path.exists(image_path):
            if HAS_PIL:
                try:
                    # Загружаем изображение
                    image = Image.open(image_path)

                    # Получаем размеры окна для масштабирования
                    max_width = 550  # Максимальная ширина с учетом отступов
                    max_height = 300  # Максимальная высота для изображения

                    # Масштабируем изображение с сохранением пропорций
                    image_ratio = image.width / image.height
                    target_ratio = max_width / max_height

                    if image_ratio > target_ratio:
                        # Широкое изображение
                        new_width = max_width
                        new_height = int(max_width / image_ratio)
                    else:
                        # Высокое изображение
                        new_height = max_height
                        new_width = int(max_height * image_ratio)

                    # Масштабируем
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Конвертируем для CTk
                    ctk_image = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=(new_width, new_height)
                    )

                    # Создаем фрейм для изображения
                    image_frame = ctk.CTkFrame(main_container, fg_color="#3a3a3a", corner_radius=10)
                    image_frame.pack(fill="x", pady=10)

                    # Заголовок изображения
                    image_label_title = ctk.CTkLabel(
                        image_frame,
                        text="🖼️ Прикрепленное изображение:",
                        font=ctk.CTkFont(size=12, weight="bold"),
                        text_color="#FFA500"
                    )
                    image_label_title.pack(pady=(10, 5))

                    # Отображаем изображение
                    image_label = ctk.CTkLabel(
                        image_frame,
                        image=ctk_image,
                        text=""
                    )
                    image_label.pack(pady=10)

                    # Информация о файле
                    file_info = ctk.CTkLabel(
                        image_frame,
                        text=f"Файл: {os.path.basename(image_path)}",
                        font=ctk.CTkFont(size=10),
                        text_color="#888888"
                    )
                    file_info.pack(pady=(0, 10))

                except Exception as e:
                    self.show_image_error(main_container, image_path, str(e))
            else:
                self.show_image_error(main_container, image_path, "Pillow не установлен")

        # Кнопка закрытия
        close_btn = ctk.CTkButton(
            main_container,
            text="Закрыть",
            command=note_window.destroy,
            fg_color="#666666",
            hover_color="#555555",
            height=40
        )
        close_btn.pack(pady=20, fill="x")

    def show_image_error(self, parent, image_path, error_message):
        """Показать сообщение об ошибке загрузки изображения"""
        error_frame = ctk.CTkFrame(parent, fg_color="#3a3a3a", corner_radius=10)
        error_frame.pack(fill="x", pady=10)

        error_label = ctk.CTkLabel(
            error_frame,
            text=f"❌ Не удалось загрузить изображение:\n{error_message}",
            font=ctk.CTkFont(size=12),
            text_color="#FF6B6B",
            justify="left"
        )
        error_label.pack(padx=15, pady=15)

        # Показываем путь к файлу
        path_label = ctk.CTkLabel(
            error_frame,
            text=f"Путь: {image_path}",
            font=ctk.CTkFont(size=10),
            text_color="#888888"
        )
        path_label.pack(pady=(0, 10))

    def delete_note_confirmation(self, note_id, note_card):
        """Подтверждение удаления заметки"""

        def confirm_delete():
            self.db.delete_note(note_id)
            note_card.destroy()
            self.show_success_message("Заметка успешно удалена!")

        confirm_dialog = ctk.CTkToplevel(self.root)
        confirm_dialog.title("Подтверждение удаления")
        confirm_dialog.geometry("400x200")
        confirm_dialog.transient(self.root)
        confirm_dialog.grab_set()

        # Центрируем
        confirm_dialog.update_idletasks()
        x = (confirm_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (confirm_dialog.winfo_screenheight() // 2) - (200 // 2)
        confirm_dialog.geometry(f"400x200+{x}+{y}")

        main_frame = ctk.CTkFrame(confirm_dialog, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        message_label = ctk.CTkLabel(
            main_frame,
            text="Вы уверены, что хотите удалить эту заметку?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff",
            wraplength=350
        )
        message_label.pack(pady=20)

        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=15)

        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Удалить",
            command=lambda: [confirm_delete(), confirm_dialog.destroy()],
            fg_color="#FF6B6B",
            hover_color="#e05555",
            width=100
        )
        delete_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Отмена",
            command=confirm_dialog.destroy,
            fg_color="#666666",
            hover_color="#555555",
            width=100
        )
        cancel_btn.pack(side="left", padx=10)

    def open_day_habits(self, selected_date):
        """Открыть окно с привычками для выбранного дня"""
        habits = self.db.get_all_habits()

        if not habits:
            self.show_info_message("У вас пока нет привычек. Добавьте первую привычку!")
            return

        # Увеличиваем высоту окна для лучшего отображения кнопок
        day_window = ctk.CTkToplevel(self.root)
        day_window.title(f"Привычки за {selected_date}")
        day_window.geometry("500x750")  # Увеличили высоту с 700 до 750
        day_window.transient(self.root)
        day_window.grab_set()

        # Центрируем окно
        day_window.update_idletasks()
        x = (day_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (day_window.winfo_screenheight() // 2) - (750 // 2)
        day_window.geometry(f"500x750+{x}+{y}")

        main_container = ctk.CTkFrame(day_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            main_container,
            text=f"Привычки за {selected_date}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=15)

        scroll_frame = ctk.CTkScrollableFrame(main_container, height=450, corner_radius=15)
        scroll_frame.pack(pady=15, fill="both", expand=True)

        checkboxes = {}

        for habit in habits:
            habit_id, name, description, habit_type, points, reminder_time, created_date = habit
            is_completed = self.db.check_habit_completion(habit_id, selected_date)

            habit_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
            habit_frame.pack(pady=8, padx=5, fill="x")

            checkbox_var = ctk.BooleanVar(value=is_completed)
            checkbox = ctk.CTkCheckBox(
                habit_frame,
                text="",
                variable=checkbox_var,
                width=25,
                height=25,
                corner_radius=6
            )
            checkbox.pack(side="left", padx=15, pady=10)
            checkboxes[habit_id] = checkbox_var

            info_frame = ctk.CTkFrame(habit_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

            icon = "✅" if habit_type == "develop" else "❌"
            color = "#2AA876" if habit_type == "develop" else "#FF6B6B"

            habit_text = f"{icon} {name}"
            if description:
                habit_text += f"\n📝 {description}"

            habit_label = ctk.CTkLabel(
                info_frame,
                text=habit_text,
                font=ctk.CTkFont(size=13),
                anchor="w",
                justify="left",
                text_color=color
            )
            habit_label.pack(fill="x")

        def save_habits():
            changes_made = False
            for habit_id, checkbox_var in checkboxes.items():
                is_checked = checkbox_var.get()
                current_status = self.db.check_habit_completion(habit_id, selected_date)

                if is_checked != current_status:
                    changes_made = True
                    if is_checked:
                        self.db.mark_habit_completed(habit_id, selected_date)
                    else:
                        self.db.remove_habit_completion(habit_id, selected_date)

            day_window.destroy()
            if changes_made:
                self.show_success_message("Привычки успешно сохранены!")
                self.update_sidebar_stats()

        # Кнопки внизу - убедимся, что они видны
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.pack(side="bottom", pady=20, fill="x", padx=50)  # Используем side="bottom"

        # Настройка сетки
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Сохранить",
            command=save_habits,
            fg_color="#2AA876",
            hover_color="#218c61",
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        save_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Отмена",
            command=day_window.destroy,
            fg_color="#FF6B6B",
            hover_color="#e05555",
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        cancel_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def show_reports(self):
        """Показать современные отчеты - простой и надежный вариант"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        main_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            main_container,
            text="📊 Отчеты и Статистика",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)

        # Карточки статистики
        stats_container = ctk.CTkFrame(main_container, fg_color="transparent")
        stats_container.pack(pady=20, fill="both", expand=True)

        total_habits = len(self.db.get_all_habits())
        total_points = self.calculate_total_points()
        today_points = self.calculate_points_for_period("today")

        # Используем grid для точного позиционирования
        stats_container.grid_rowconfigure(0, weight=1)
        stats_container.grid_rowconfigure(1, weight=1)
        stats_container.grid_columnconfigure(0, weight=1)
        stats_container.grid_columnconfigure(1, weight=1)

        # Карточка 1: Всего привычек (кликабельная)
        habits_btn = ctk.CTkButton(
            stats_container,
            text=f"📊 Всего привычек\n\n{total_habits}\n\n↗️ Нажмите для просмотра",
            command=self.show_all_habits,
            fg_color="#4CC9F0",
            hover_color="#3a9bc8",
            corner_radius=15,
            font=ctk.CTkFont(size=16),
            text_color="#ffffff",
            anchor="center",
            height=120
        )
        habits_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Карточка 2: Всего баллов
        points_frame = ctk.CTkFrame(
            stats_container,
            fg_color="#2AA876",
            corner_radius=15,
            height=120
        )
        points_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        points_frame.grid_propagate(False)

        ctk.CTkLabel(
            points_frame,
            text=f"💰 Всего баллов\n\n{total_points}",
            font=ctk.CTkFont(size=16),
            text_color="#ffffff",
            justify="center"
        ).pack(expand=True, fill="both", padx=20, pady=20)

        # Карточка 3: Баллов сегодня (растягиваем на 2 колонки)
        today_frame = ctk.CTkFrame(
            stats_container,
            fg_color="#FFA500",
            corner_radius=15,
            height=120
        )
        today_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        today_frame.grid_propagate(False)

        ctk.CTkLabel(
            today_frame,
            text=f"🎯 Баллов сегодня\n\n{today_points}",
            font=ctk.CTkFont(size=16),
            text_color="#ffffff",
            justify="center"
        ).pack(expand=True, fill="both", padx=20, pady=20)

        # Дополнительная статистика
        self.create_detailed_stats(main_container)

    def adjust_color(self, color, amount):
        """Изменяет яркость цвета - исправленная версия"""
        try:
            # Преобразуем hex в RGB
            color = color.lstrip('#')
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)

            # Изменяем яркость
            r = max(0, min(255, r + amount))
            g = max(0, min(255, g + amount))
            b = max(0, min(255, b + amount))

            # Возвращаем обратно в hex
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            # Fallback цвета
            if color == "#4CC9F0":
                return "#3a9bc8"
            elif color == "#2AA876":
                return "#218c61"
            elif color == "#FFA500":
                return "#e69500"
            return color

    def create_detailed_stats(self, parent):
        """Создание детальной статистики - улучшенная версия"""
        detailed_frame = ctk.CTkFrame(parent, fg_color="transparent")
        detailed_frame.pack(pady=30, fill="x")

        # Заголовок
        detailed_label = ctk.CTkLabel(
            detailed_frame,
            text="📈 Детальная статистика",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        detailed_label.pack(anchor="w", pady=(0, 15))

        # Статистика по типам привычек
        habits = self.db.get_all_habits()
        develop_count = sum(1 for h in habits if h[3] == "develop")
        quit_count = sum(1 for h in habits if h[3] == "quit")

        stats_grid = ctk.CTkFrame(detailed_frame, fg_color="transparent")
        stats_grid.pack(fill="x")

        # Настройка сетки
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)

        stats_data = [
            ("✅ Привычки для развития", f"{develop_count}", "#2AA876"),
            ("❌ Привычки для избавления", f"{quit_count}", "#FF6B6B"),
            ("📅 Всего выполнений", f"{self.get_total_completions()}", "#4CC9F0"),
            ("⭐ Средний балл за день", f"{self.get_average_daily_points():.1f}", "#FFA500"),
        ]

        for i, (text, value, color) in enumerate(stats_data):
            row = i // 2
            col = i % 2

            stat_frame = ctk.CTkFrame(stats_grid, fg_color="#2b2b2b", corner_radius=10)
            stat_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            stat_text = ctk.CTkLabel(
                stat_frame,
                text=text,
                font=ctk.CTkFont(size=12),
                text_color="#888888"
            )
            stat_text.pack(pady=(8, 2))

            stat_value = ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color
            )
            stat_value.pack(pady=(2, 8))

    def get_total_completions(self):
        """Получить общее количество выполнений привычек"""
        habits = self.db.get_all_habits()
        total = 0
        for habit in habits:
            total += self.db.get_habit_completion_count(habit[0])
        return total

    def get_average_daily_points(self):
        """Получить среднее количество баллов за день"""
        # Простая реализация - можно улучшить
        total_points = self.calculate_total_points()
        return total_points / 30 if total_points > 0 else 0  # Примерно за месяц

    def calculate_total_points(self):
        """Общее количество баллов"""
        return self.db.calculate_total_points()

    def calculate_points_for_period(self, period="today"):
        """Баллы за период"""
        return self.db.calculate_points_for_period(period)

    def get_completed_habits_count(self, habits, current_date):
        """Подсчет количества выполненных привычек за день"""
        completed_count = 0
        for habit in habits:
            habit_id, name, description, habit_type, points, reminder_time, created_date = habit
            is_completed = self.db.check_habit_completion(habit_id, current_date)

            if habit_type == "develop":
                if is_completed:
                    completed_count += 1
            else:
                if not is_completed:
                    completed_count += 1

        return completed_count

    def get_motivation_message(self, completion_rate):
        """Получить мотивационное сообщение"""
        if completion_rate >= 0.75:
            return "🎉 Отличная работа! Вы молодец!"
        elif completion_rate >= 0.5:
            return "👍 Хороший результат! Продолжайте в том же духе!"
        elif completion_rate >= 0.25:
            return "💪 Не сдавайтесь! Завтра будет лучше!"
        else:
            return "🌱 Начните с малого! Каждый день - новая возможность!"

    def get_motivation_color(self, completion_rate):
        """Получить цвет мотивационного сообщения"""
        if completion_rate >= 0.75:
            return "#2AA876"
        elif completion_rate >= 0.5:
            return "#FFA500"
        elif completion_rate >= 0.25:
            return "#FF6B6B"
        else:
            return "#888888"

    def show_success_message(self, message):
        """Показать красивое сообщение об успехе"""
        self.show_message_dialog("✅ Успех", message, "#2AA876")

    def show_error_message(self, message):
        """Показать красивое сообщение об ошибке"""
        self.show_message_dialog("❌ Ошибка", message, "#FF6B6B")

    def show_info_message(self, message):
        """Показать красивое информационное сообщение"""
        self.show_message_dialog("ℹ️ Информация", message, "#4CC9F0")

    def show_message_dialog(self, title, message, color):
        """Показать диалоговое окно с сообщением"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x250")  # Увеличили высоту с 200 до 250
        dialog.transient(self.root)
        dialog.grab_set()

        # Центрируем
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)  # Обновили координату Y
        dialog.geometry(f"400x250+{x}+{y}")

        main_frame = ctk.CTkFrame(dialog, fg_color=color, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=20)

        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="#ffffff",
            wraplength=350
        )
        message_label.pack(pady=10)

        ok_btn = ctk.CTkButton(
            main_frame,
            text="OK",
            command=dialog.destroy,
            fg_color="#ffffff",
            text_color=color,
            hover_color="#f0f0f0",
            height=35
        )
        ok_btn.pack(pady=20)

    def show_all_habits(self):
        """Показать все привычки с возможностью удаления"""
        habits = self.db.get_all_habits()

        if not habits:
            self.show_info_message("У вас пока нет привычек. Добавьте первую привычку!")
            return

        # Создаем окно для отображения всех привычек
        habits_window = ctk.CTkToplevel(self.root)
        habits_window.title("📋 Все привычки")
        habits_window.geometry("700x600")
        habits_window.transient(self.root)
        habits_window.grab_set()

        # Центрируем окно
        habits_window.update_idletasks()
        x = (habits_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (habits_window.winfo_screenheight() // 2) - (600 // 2)
        habits_window.geometry(f"700x600+{x}+{y}")

        main_container = ctk.CTkFrame(habits_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title_label = ctk.CTkLabel(
            main_container,
            text="📋 Все ваши привычки",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack(pady=10)

        # Счетчик привычек
        count_label = ctk.CTkLabel(
            main_container,
            text=f"Всего привычек: {len(habits)}",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        count_label.pack(pady=5)

        # Прокручиваемая область для привычек
        scroll_frame = ctk.CTkScrollableFrame(main_container, height=400, corner_radius=15)
        scroll_frame.pack(pady=15, fill="both", expand=True)

        # Создаем карточки для каждой привычки
        habit_cards = []

        for habit in habits:
            habit_id, name, description, habit_type, points, reminder_time, created_date = habit

            # Создаем карточку привычки
            habit_card = self.create_habit_card(scroll_frame, habit_id, name, description, habit_type, points,
                                                created_date)
            habit_cards.append(habit_card)

        # Фрейм для кнопок
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.pack(side="bottom", pady=10, fill="x")

        def refresh_habits():
            """Обновить список привычек"""
            for card in habit_cards:
                card.destroy()

            habits_window.destroy()
            self.show_all_habits()

        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Закрыть",
            command=habits_window.destroy,
            fg_color="#FF6B6B",
            hover_color="#e05555",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        close_btn.pack(fill="x")

    def create_habit_card(self, parent, habit_id, name, description, habit_type, points, created_date):
        """Создать карточку привычки с возможностью удаления"""
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color="#2b2b2b")
        card.pack(pady=8, padx=5, fill="x")

        # Основная информация
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", expand=True, padx=15, pady=12)

        # Заголовок и тип
        header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        header_frame.pack(fill="x")

        icon = "✅" if habit_type == "develop" else "❌"
        color = "#2AA876" if habit_type == "develop" else "#FF6B6B"
        type_text = "Развивать" if habit_type == "develop" else "Избавиться"

        # Название и тип
        name_label = ctk.CTkLabel(
            header_frame,
            text=f"{icon} {name}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
            text_color=color
        )
        name_label.pack(side="left", anchor="w")

        type_label = ctk.CTkLabel(
            header_frame,
            text=type_text,
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        type_label.pack(side="right", anchor="e")

        # Описание (если есть)
        if description:
            desc_label = ctk.CTkLabel(
                info_frame,
                text=f"📝 {description}",
                font=ctk.CTkFont(size=13),
                anchor="w",
                justify="left",
                text_color="#aaaaaa"
            )
            desc_label.pack(fill="x", pady=(5, 0))

        # Детали привычки
        details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        details_frame.pack(fill="x", pady=(8, 0))

        # Баллы
        points_label = ctk.CTkLabel(
            details_frame,
            text=f"💰 Баллы: {points}",
            font=ctk.CTkFont(size=12),
            text_color="#4CC9F0"
        )
        points_label.pack(side="left", padx=(0, 15))

        # Дата создания
        created_label = ctk.CTkLabel(
            details_frame,
            text=f"📅 Создана: {created_date}",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        created_label.pack(side="left", padx=(0, 15))

        # Статистика выполнений
        completion_count = self.db.get_habit_completion_count(habit_id)
        stats_label = ctk.CTkLabel(
            details_frame,
            text=f"🎯 Выполнена: {completion_count} раз",
            font=ctk.CTkFont(size=12),
            text_color="#FFA500"
        )
        stats_label.pack(side="left")

        # Кнопка удаления
        delete_btn = ctk.CTkButton(
            details_frame,
            text="🗑️ Удалить",
            command=lambda hid=habit_id: self.delete_habit_confirmation(hid, card),
            fg_color="transparent",
            hover_color="#FF6B6B",
            border_width=1,
            border_color="#FF6B6B",
            text_color="#FF6B6B",
            width=80,
            height=30,
            font=ctk.CTkFont(size=11),
            corner_radius=8
        )
        delete_btn.pack(side="right")

        return card

    def delete_habit_confirmation(self, habit_id, habit_card):
        """Подтверждение удаления привычки"""

        def confirm_delete():
            success = self.db.delete_habit(habit_id)
            if success:
                habit_card.destroy()
                self.show_success_message("Привычка успешно удалена!")
                self.update_sidebar_stats()
                # Обновляем статистику в отчетах, если они открыты
                if hasattr(self, 'main_content'):
                    for widget in self.main_content.winfo_children():
                        if hasattr(widget, 'winfo_children'):
                            for child in widget.winfo_children():
                                if hasattr(child, 'winfo_name') and 'reports' in str(child.winfo_name()).lower():
                                    self.show_reports()
                                    break
            else:
                self.show_error_message("Ошибка при удалении привычки!")

        # Диалог подтверждения
        confirm_dialog = ctk.CTkToplevel(self.root)
        confirm_dialog.title("Подтверждение удаления")
        confirm_dialog.geometry("400x200")
        confirm_dialog.transient(self.root)
        confirm_dialog.grab_set()

        # Центрируем
        confirm_dialog.update_idletasks()
        x = (confirm_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (confirm_dialog.winfo_screenheight() // 2) - (200 // 2)
        confirm_dialog.geometry(f"400x200+{x}+{y}")

        main_frame = ctk.CTkFrame(confirm_dialog, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Сообщение
        message_label = ctk.CTkLabel(
            main_frame,
            text="Вы уверены, что хотите удалить эту привычку?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff",
            wraplength=350
        )
        message_label.pack(pady=20)

        warning_label = ctk.CTkLabel(
            main_frame,
            text="Это действие нельзя отменить!",
            font=ctk.CTkFont(size=12),
            text_color="#FF6B6B"
        )
        warning_label.pack(pady=5)

        # Кнопки
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=15)

        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Удалить",
            command=lambda: [confirm_delete(), confirm_dialog.destroy()],
            fg_color="#FF6B6B",
            hover_color="#e05555",
            width=100,
            height=35
        )
        delete_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Отмена",
            command=confirm_dialog.destroy,
            fg_color="#666666",
            hover_color="#555555",
            width=100,
            height=35
        )
        cancel_btn.pack(side="left", padx=10)

    def setup_reminders(self):
        """Настройка системы напоминаний"""
        self.check_reminders()

    def check_reminders(self):
        """Проверка напоминаний каждую минуту"""
        try:
            habits_with_reminders = self.db.get_habits_with_reminders()
            current_time = datetime.now().strftime("%H:%M")

            for habit in habits_with_reminders:
                habit_id, name, description, habit_type, points, reminder_time, created_date = habit
                if reminder_time and reminder_time == current_time:
                    self.show_reminder_notification(name, description)

        except Exception as e:
            print(f"Ошибка при проверке напоминаний: {e}")

        # Проверяем каждую минуту
        self.root.after(60000, self.check_reminders)

    def show_reminder_notification(self, habit_name, description):
        """Показать напоминание"""
        reminder_window = ctk.CTkToplevel(self.root)
        reminder_window.title("🔔 Напоминание о привычке")
        reminder_window.geometry("400x250")
        reminder_window.transient(self.root)
        reminder_window.grab_set()

        # Центрируем
        reminder_window.update_idletasks()
        x = (reminder_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (reminder_window.winfo_screenheight() // 2) - (250 // 2)
        reminder_window.geometry(f"400x250+{x}+{y}")

        main_frame = ctk.CTkFrame(reminder_window, fg_color="#FFA500", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Иконка и заголовок
        icon_label = ctk.CTkLabel(
            main_frame,
            text="🔔",
            font=ctk.CTkFont(size=40)
        )
        icon_label.pack(pady=10)

        title_label = ctk.CTkLabel(
            main_frame,
            text="Время для привычки!",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=5)

        habit_label = ctk.CTkLabel(
            main_frame,
            text=f"Привычка: {habit_name}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        habit_label.pack(pady=5)

        if description:
            desc_label = ctk.CTkLabel(
                main_frame,
                text=description,
                font=ctk.CTkFont(size=12),
                text_color="#ffffff",
                wraplength=350
            )
            desc_label.pack(pady=5)

        def mark_completed_and_close():
            """Отметить выполненной и закрыть"""
            today = date.today()
            # Находим ID привычки
            habits = self.db.get_all_habits()
            for habit in habits:
                if habit[1] == habit_name:
                    self.db.mark_habit_completed(habit[0], today)
                    self.show_success_message(f"Привычка '{habit_name}' отмечена как выполненная!")
                    break
            reminder_window.destroy()
            self.update_sidebar_stats()

        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=15)

        completed_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ Выполнено",
            command=mark_completed_and_close,
            fg_color="#2AA876",
            hover_color="#218c61",
            width=120
        )
        completed_btn.pack(side="left", padx=5)

        close_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Закрыть",
            command=reminder_window.destroy,
            fg_color="#FF6B6B",
            hover_color="#e05555",
            width=120
        )
        close_btn.pack(side="left", padx=5)

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernHabitTrackerApp()
    app.run()