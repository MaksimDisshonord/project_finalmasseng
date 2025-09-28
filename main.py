import customtkinter as ctk
import tkinter as tk
import random
import re
from datetime import datetime

# Заготовлені відповіді українською мовою
responses = {
    "привіт": "Привіт! Як твої справи?",
    "як справи": "У мене все чудово, дякую! 😊 А у тебе?",
    "що робиш": "Відповідаю на твої запитання 😎",
    "бувай": "Бувай! Гарного дня 👋",
    "до побачення": "До побачення! Було приємно спілкуватися 👋",
    "до зустрічі": "До зустрічі! Гарно провести час 👋",

    "як тебе звати": "Я чат-бот 🤖",
    "скільки тобі років": "Я ще молодий, всього кілька рядків коду 😁",
    "де ти живеш": "Я живу прямо тут, у твоєму комп'ютері 💻",
    "що ти вмієш": "Я вмію відповідати на запитання та підтримувати розмову 🗣️",
    "ти людина": "Ні, я бот, але можу спілкуватися майже як людина 😉",
    "яка погода": "Погода у мене завжди ясна — я ж у коді ☀️",
    "що їси": "Електрику ⚡ та трохи оперативної пам'яті 😅",
    "ти спиш": "Ні, я завжди на зв'язку 🔋",
    "як настрій": "Чудовий! Дякую, що запитав 😃 А у тебе?",
    "любиш музику": "Звичайно! Особливо електронну 🎶",
    "який сьогодні день": "Сьогодні чудовий день, щоб поспілкуватися зі мною 😉",

    # Запитання про комп'ютер
    "що таке комп'ютер": "Комп'ютер — це розумна машина для обробки інформації 💻",
    "хто придумав комп'ютер": "Перші ідеї комп'ютера запропонував Чарльз Беббідж у 19 столітті 👨‍🔬",
    "навіщо потрібен комп'ютер": "Комп'ютер потрібен для роботи, ігор, спілкування та багато чого іншого 🌍",
    "ти комп'ютер": "Я програма, яка працює на комп'ютері ⚡",

    # Додаткові відповіді
    "дякую": "Будь ласка! Завжди радий допомогти 😊",
    "спасибі": "Будь ласка! Завжди радий допомогти 😊",
    "допоможи": "Звичайно допоможу! Що тебе цікавить? 🤝",
    "нудно": "Давай поговоримо про щось цікаве! 💭",
    "що нового": "Завжди є що обговорити! Розкажи, що у тебе відбувається? 📰",
    "як дела": "У мене все супер! А у тебе як? 😊"
}

# Рекомендації для користувача українською
suggestions = [
    # Привітання та знайомство
    ["Привіт", "Як справи", "Як тебе звати"],
    ["Що робиш", "Як настрій", "Скільки тобі років"],

    # Запитання про бота
    ["Ти людина", "Що ти вмієш", "Де ти живеш"],
    ["Ти спиш", "Що їси", "Любиш музику"],

    # Комп'ютери та технології
    ["Що таке комп'ютер", "Хто придумав комп'ютер", "Ти комп'ютер"],

    # Спілкування
    ["Який сьогодні день", "Яка погода", "Час"],
    ["Дякую", "Допоможи", "Нудно"],

    # Особиста інформація (приклади)
    ["Мене звати Анна", "Мені 20 років", "Я люблю програмування"],

    # Прощання
    ["Бувай", "До побачення", "До зустрічі"]
]

# Шаблони для більш гнучких відповідей
patterns = [
    (r"мене звати (\w+)", "Приємно познайомитися, {}! 😊"),
    (r"мені (\d+) років", "Здорово! {} років - чудовий вік! 🎉"),
    (r"я люблю (\w+)", "Круто! {} - це чудово! ❤️"),
    (r"час|скільки часу", f"Зараз {datetime.now().strftime('%H:%M')} ⏰"),
]

# Теми для чата
THEMES = {
    "light": {
        "bg_main": "#FAFAFA",
        "bg_chat": "white",
        "bg_header": "#2AABEE",
        "bg_input": "#F5F5F5",
        "bg_suggestions": "white",
        "bg_suggestions_header": "#E3F2FD",
        "text_header": "white",
        "text_suggestions_header": "#1976D2",
        "user_message": "#0084FF",
        "bot_message": "#F0F0F0",
        "user_text": "white",
        "bot_text": "black",
        "border_color": "#E0E0E0"
    },
    "dark": {
        "bg_main": "#1A1A1A",
        "bg_chat": "#2D2D2D",
        "bg_header": "#1E3A8A",
        "bg_input": "#404040",
        "bg_suggestions": "#2D2D2D",
        "bg_suggestions_header": "#374151",
        "text_header": "white",
        "text_suggestions_header": "#60A5FA",
        "user_message": "#3B82F6",
        "bot_message": "#4B5563",
        "user_text": "white",
        "bot_text": "white",
        "border_color": "#4B5563"
    }
}


class TelegramMessage(ctk.CTkFrame):
    def __init__(self, parent, sender, text, timestamp, is_user=False, theme="light"):
        super().__init__(parent, fg_color="transparent")

        self.is_user = is_user
        self.theme = theme
        current_theme = THEMES[theme]

        message_frame = ctk.CTkFrame(
            self,
            fg_color=current_theme["user_message"] if is_user else current_theme["bot_message"],
            corner_radius=18
        )

        if is_user:
            message_frame.pack(fill="x", padx=(50, 10), pady=2, anchor="e")
        else:
            message_frame.pack(fill="x", padx=(10, 50), pady=2, anchor="w")

        message_label = ctk.CTkLabel(
            message_frame,
            text=text,
            font=ctk.CTkFont(size=14),
            text_color=current_theme["user_text"] if is_user else current_theme["bot_text"],
            wraplength=300,
            justify="left"
        )
        message_label.pack(padx=12, pady=8, anchor="w")

        info_text = f"{sender} • {timestamp}"
        info_label = ctk.CTkLabel(
            message_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color=current_theme["user_text"] if is_user else "gray",
        )
        info_label.pack(padx=12, pady=(0, 8), anchor="e" if is_user else "w")


class ChatBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_theme = "light"

        self.title("Telegram Style ChatBot - Українська версія")
        self.geometry("900x700")
        self.minsize(600, 500)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.create_interface()
        self.message_widgets = []
        self.suggestion_buttons = []
        self.update_suggestions()

        self.add_message("Чат-Бот", "Привіт! Я готовий до спілкування! 😊", False)

    def create_interface(self):
        """Створює інтерфейс з поточною темою"""
        theme = THEMES[self.current_theme]

        # Заголовок з кнопкою налаштувань
        self.header_frame = ctk.CTkFrame(self, height=60, fg_color=theme["bg_header"], corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)

        # Кнопка налаштувань
        self.settings_button = ctk.CTkButton(
            self.header_frame,
            text="⚙️",
            width=40,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            hover_color="#1E88E5",
            text_color="white",
            command=self.toggle_settings
        )
        self.settings_button.pack(side="right", padx=15, pady=10)

        self.avatar_frame = ctk.CTkFrame(self.header_frame, width=40, height=40, fg_color="#1E88E5", corner_radius=20)
        self.avatar_frame.pack(side="left", padx=15, pady=10)
        self.avatar_frame.pack_propagate(False)

        avatar_label = ctk.CTkLabel(
            self.avatar_frame,
            text="🤖",
            font=ctk.CTkFont(size=20)
        )
        avatar_label.place(relx=0.5, rely=0.5, anchor="center")

        info_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=10)

        self.bot_name = ctk.CTkLabel(
            info_frame,
            text="Чат-Бот",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=theme["text_header"]
        )
        self.bot_name.pack(anchor="w")

        self.bot_status = ctk.CTkLabel(
            info_frame,
            text="в мережі",
            font=ctk.CTkFont(size=12),
            text_color=theme["text_header"]
        )
        self.bot_status.pack(anchor="w")

        # Панель налаштувань (спочатку прихована)
        self.settings_panel = ctk.CTkFrame(self, height=80, fg_color=theme["bg_suggestions_header"])
        self.settings_visible = False

        settings_label = ctk.CTkLabel(
            self.settings_panel,
            text="Налаштування теми:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme["text_suggestions_header"]
        )
        settings_label.pack(side="left", padx=20, pady=25)

        self.theme_var = tk.StringVar(value=self.current_theme)

        light_radio = ctk.CTkRadioButton(
            self.settings_panel,
            text="☀️ Світла",
            variable=self.theme_var,
            value="light",
            font=ctk.CTkFont(size=12),
            text_color=theme["text_suggestions_header"],
            command=self.change_theme
        )
        light_radio.pack(side="left", padx=10, pady=25)

        dark_radio = ctk.CTkRadioButton(
            self.settings_panel,
            text="🌙 Темна",
            variable=self.theme_var,
            value="dark",
            font=ctk.CTkFont(size=12),
            text_color=theme["text_suggestions_header"],
            command=self.change_theme
        )
        dark_radio.pack(side="left", padx=10, pady=25)

        self.main_frame = ctk.CTkFrame(self, fg_color=theme["bg_main"])
        self.main_frame.pack(fill="both", expand=True)

        self.chat_frame = ctk.CTkFrame(self.main_frame, fg_color=theme["bg_chat"])
        self.chat_frame.pack(side="left", fill="both", expand=True, padx=(0, 1))

        self.messages_frame = ctk.CTkScrollableFrame(
            self.chat_frame,
            fg_color=theme["bg_chat"]
        )
        self.messages_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.suggestions_frame = ctk.CTkFrame(self.main_frame, width=250, fg_color=theme["bg_suggestions"])
        self.suggestions_frame.pack(side="right", fill="y")
        self.suggestions_frame.pack_propagate(False)

        suggestions_header = ctk.CTkFrame(self.suggestions_frame, height=50, fg_color=theme["bg_suggestions_header"],
                                          corner_radius=0)
        suggestions_header.pack(fill="x")
        suggestions_header.pack_propagate(False)

        self.suggestions_label = ctk.CTkLabel(
            suggestions_header,
            text="💬 Швидкі відповіді",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme["text_suggestions_header"]
        )
        self.suggestions_label.pack(pady=15)

        self.suggestions_scroll = ctk.CTkScrollableFrame(
            self.suggestions_frame,
            fg_color=theme["bg_suggestions"]
        )
        self.suggestions_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.input_frame = ctk.CTkFrame(self.chat_frame, height=70, fg_color=theme["bg_input"], corner_radius=0)
        self.input_frame.pack(fill="x", side="bottom")
        self.input_frame.pack_propagate(False)

        input_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        input_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.entry = ctk.CTkEntry(
            input_container,
            placeholder_text="Напишіть повідомлення...",
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=20,
            border_width=1,
            border_color=theme["border_color"]
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(10, 5))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(
            input_container,
            text="➤",
            width=40,
            height=40,
            font=ctk.CTkFont(size=16),
            corner_radius=20,
            fg_color="#2AABEE",
            hover_color="#1E88E5",
            command=self.send_message
        )
        self.send_button.pack(side="right", padx=(5, 0))

    def toggle_settings(self):
        """Показує/приховує панель налаштувань"""
        if self.settings_visible:
            self.settings_panel.pack_forget()
            self.settings_visible = False
        else:
            self.settings_panel.pack(fill="x", after=self.header_frame)
            self.settings_visible = True

    def change_theme(self):
        """Змінює тему чата"""
        new_theme = self.theme_var.get()
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            ctk.set_appearance_mode("dark" if new_theme == "dark" else "light")
            self.refresh_interface()

    def refresh_interface(self):
        """Оновлює інтерфейс з новою темою"""
        # Зберігаємо повідомлення
        messages_data = []
        for widget in self.message_widgets:
            # Тут ми б зберегли дані повідомлень, але для простоти просто очистимо
            pass

        # Очищуємо всі віджети
        for widget in self.winfo_children():
            widget.destroy()

        # Пересоздаємо інтерфейс
        self.create_interface()
        self.message_widgets = []
        self.suggestion_buttons = []
        self.update_suggestions()

        # Додаємо початкове повідомлення
        self.add_message("Чат-Бот", "Привіт! Я готовий до спілкування! 😊", False)

    def update_suggestions(self):
        """Оновлює рекомендації в стилі Telegram"""
        theme = THEMES[self.current_theme]

        for button in self.suggestion_buttons:
            button.destroy()
        self.suggestion_buttons = []

        selected_groups = random.sample(suggestions, min(4, len(suggestions)))
        current_suggestions = []

        for group in selected_groups:
            current_suggestions.extend(group)

        random.shuffle(current_suggestions)
        display_suggestions = current_suggestions[:12]

        for suggestion in display_suggestions:
            btn = ctk.CTkButton(
                self.suggestions_scroll,
                text=suggestion,
                height=35,
                font=ctk.CTkFont(size=12),
                corner_radius=18,
                fg_color="#E3F2FD" if self.current_theme == "light" else "#374151",
                hover_color="#BBDEFB" if self.current_theme == "light" else "#4B5563",
                text_color="#1976D2" if self.current_theme == "light" else "#60A5FA",
                border_width=1,
                border_color="#2196F3" if self.current_theme == "light" else "#6B7280",
                command=lambda s=suggestion: self.use_suggestion(s)
            )
            btn.pack(fill="x", pady=3)
            self.suggestion_buttons.append(btn)

        separator = ctk.CTkFrame(self.suggestions_scroll, height=1, fg_color=theme["border_color"])
        separator.pack(fill="x", pady=10)

        refresh_btn = ctk.CTkButton(
            self.suggestions_scroll,
            text="🔄 Оновити пропозиції",
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=20,
            fg_color="#4CAF50",
            hover_color="#45A049",
            command=self.update_suggestions
        )
        refresh_btn.pack(fill="x", pady=5)
        self.suggestion_buttons.append(refresh_btn)

    def use_suggestion(self, suggestion):
        """Використовує рекомендацію"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, suggestion)
        self.send_message()

    def find_pattern_response(self, message):
        """Шукає збіги з шаблонами"""
        for pattern, response_template in patterns:
            match = re.search(pattern, message.lower())
            if match:
                if '{}' in response_template:
                    return response_template.format(match.group(1))
                else:
                    return response_template
        return None

    def get_fuzzy_match(self, message):
        """Простий пошук за ключовими словами"""
        words = message.lower().split()
        for word in words:
            for key in responses.keys():
                if word in key or key in word:
                    return responses[key]
        return None

    def send_message(self, event=None):
        user_msg = self.entry.get().strip()
        if not user_msg:
            return

        self.entry.delete(0, tk.END)

        self.add_message("Ви", user_msg, True)

        bot_msg = None

        bot_msg = responses.get(user_msg.lower())

        if not bot_msg:
            bot_msg = self.find_pattern_response(user_msg)

        if not bot_msg:
            bot_msg = self.get_fuzzy_match(user_msg)

        # Стандартна відповідь
        if not bot_msg:
            default_responses = [
                "Цікаво! Розкажи більше 🤔",
                "Я поки не знаю, що відповісти 😅",
                "Хм, це нове для мене 🧐",
                "Можеш переформулювати? 🤖",
                "Не зовсім розумію, спробуй інакше 🤷‍♂️"
            ]
            bot_msg = random.choice(default_responses)

        self.after(500, lambda: self.add_message("Чат-Бот", bot_msg, False))

        if random.randint(1, 5) == 1:
            self.update_suggestions()

    def add_message(self, sender, text, is_user=False):
        """Додає повідомлення в стилі Telegram"""
        timestamp = datetime.now().strftime("%H:%M")

        message_widget = TelegramMessage(
            self.messages_frame,
            sender,
            text,
            timestamp,
            is_user,
            self.current_theme
        )
        message_widget.pack(fill="x", pady=2)
        self.message_widgets.append(message_widget)

        self.after(100, lambda: self.messages_frame._parent_canvas.yview_moveto(1.0))


if __name__ == "__main__":
    app = ChatBotApp()
    app.mainloop()