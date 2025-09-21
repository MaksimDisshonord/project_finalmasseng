import customtkinter as ctk
import tkinter as tk
from tkinter import PhotoImage
import re
from datetime import datetime
import random

# Заготовленные ответы
responses = {
    "привет": "Привет! Как твои дела?",
    "как дела": "У меня всё отлично, спасибо! 😊 А у тебя?",
    "что делаешь": "Отвечаю на твои вопросы 😎",
    "пока": "Пока! Хорошего дня 👋",
    "до свидания": "До свидания! Было приятно пообщаться 👋",

    "как тебя зовут": "Я чат-бот 👁️",
    "сколько тебе лет": "Я ещё молодой, всего несколько строчек кода 😁",
    "где ты живешь": "Я живу прямо тут, в твоём компьютере 💻",
    "что ты умеешь": "Я умею отвечать на вопросы и поддерживать беседу 🗣️",
    "ты человек": "Нет, я бот, но могу общаться почти как человек 😉",
    "какая погода": "Погода у меня всегда ясная — я ведь в коде ☀️",
    "что кушаешь": "Электричество ⚡ и немного оперативной памяти 😅",
    "ты спишь": "Нет, я всегда на связи 🔋",
    "как настроение": "Отличное! Спасибо, что спросил 😃 А у тебя?",
    "любишь музыку": "Конечно! Особенно электронную 🎶",
    "какой сегодня день": "Сегодня прекрасный день, чтобы пообщаться со мной 😉",

    # Вопросы про компьютер
    "что такое компьютер": "Компьютер — это умная машина для обработки информации 💻",
    "кто придумал компьютер": "Первые идеи компьютера предложил Чарльз Бэббидж в 19 веке 👨‍🔬",
    "для чего нужен компьютер": "Компьютер нужен для работы, игр, общения и многого другого 🌍",
    "ты компьютер": "Я программа, которая работает на компьютере ⚡",

    # Дополнительные ответы
    "спасибо": "Пожалуйста! Всегда рад помочь 😊",
    "помоги": "Конечно помогу! Что тебя интересует? 🤝",
    "скучно": "Давай поговорим о чём-нибудь интересном! 💭",
    "что нового": "Всегда есть что обсудить! Расскажи, что у тебя происходит? 📰"
}

# Рекомендации для пользователя
suggestions = [
    # Приветствие и знакомство
    ["Привет", "Как дела", "Как тебя зовут"],
    ["Что делаешь", "Как настроение", "Сколько тебе лет"],

    # Вопросы о боте
    ["Ты человек", "Что ты умеешь", "Где ты живешь"],
    ["Ты спишь", "Что кушаешь", "Любишь музыку"],

    # Компьютеры и технологии
    ["Что такое компьютер", "Кто придумал компьютер", "Ты компьютер"],

    # Общение
    ["Какой сегодня день", "Какая погода", "Время"],
    ["Спасибо", "Помоги", "Скучно"],

    # Личная информация (примеры)
    ["Меня зовут Анна", "Мне 20 лет", "Я люблю программирование"],

    # Прощание
    ["Пока", "До свидания"]
]

# Шаблоны для более гибких ответов
patterns = [
    (r"меня зовут (\w+)", "Приятно познакомиться, {}! 😊"),
    (r"мне (\d+) лет", "Здорово! {} лет - отличный возраст! 🎉"),
    (r"я люблю (\w+)", "Круто! {} - это замечательно! ❤️"),
    (r"время|сколько времени", f"Сейчас {datetime.now().strftime('%H:%M')} ⏰"),
]


class TelegramMessage(ctk.CTkFrame):
    def __init__(self, parent, sender, text, timestamp, is_user=False):
        super().__init__(parent, fg_color="transparent")

        self.is_user = is_user

        message_frame = ctk.CTkFrame(
            self,
            fg_color="#0084FF" if is_user else "#F0F0F0",
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
            text_color="white" if is_user else "black",
            wraplength=300,
            justify="left"
        )
        message_label.pack(padx=12, pady=8, anchor="w")

        info_text = f"{sender} • {timestamp}"
        info_label = ctk.CTkLabel(
            message_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color="white" if is_user else "gray",
        )
        info_label.pack(padx=12, pady=(0, 8), anchor="e" if is_user else "w")


class ChatBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Telegram Style ChatBot")
        self.geometry("900x700")
        self.minsize(600, 500)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.header_frame = ctk.CTkFrame(self, height=60, fg_color="#2AABEE", corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)

        self.avatar_frame = ctk.CTkFrame(self.header_frame, width=40, height=40, fg_color="#1E88E5", corner_radius=20)
        self.avatar_frame.pack(side="left", padx=15, pady=10)
        self.avatar_frame.pack_propagate(False)

        avatar_label = ctk.CTkLabel(
            self.avatar_frame,
            text="👁️",
            font=ctk.CTkFont(size=20)
        )
        avatar_label.place(relx=0.5, rely=0.5, anchor="center")

        info_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=10)

        self.bot_name = ctk.CTkLabel(
            info_frame,
            text="ChatBot",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        self.bot_name.pack(anchor="w")

        self.bot_status = ctk.CTkLabel(
            info_frame,
            text="в сети",
            font=ctk.CTkFont(size=12),
            text_color="white"
        )
        self.bot_status.pack(anchor="w")

        self.main_frame = ctk.CTkFrame(self, fg_color="#FAFAFA")
        self.main_frame.pack(fill="both", expand=True)

        self.chat_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.chat_frame.pack(side="left", fill="both", expand=True, padx=(0, 1))

        self.messages_frame = ctk.CTkScrollableFrame(
            self.chat_frame,
            fg_color="white"
        )
        self.messages_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.suggestions_frame = ctk.CTkFrame(self.main_frame, width=250, fg_color="white")
        self.suggestions_frame.pack(side="right", fill="y")
        self.suggestions_frame.pack_propagate(False)

        suggestions_header = ctk.CTkFrame(self.suggestions_frame, height=50, fg_color="#E3F2FD", corner_radius=0)
        suggestions_header.pack(fill="x")
        suggestions_header.pack_propagate(False)

        self.suggestions_label = ctk.CTkLabel(
            suggestions_header,
            text="💬 Быстрые ответы",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1976D2"
        )
        self.suggestions_label.pack(pady=15)

        self.suggestions_scroll = ctk.CTkScrollableFrame(
            self.suggestions_frame,
            fg_color="white"
        )
        self.suggestions_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.input_frame = ctk.CTkFrame(self.chat_frame, height=70, fg_color="#F5F5F5", corner_radius=0)
        self.input_frame.pack(fill="x", side="bottom")
        self.input_frame.pack_propagate(False)

        input_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        input_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.attach_button = ctk.CTkButton(
            input_container,
            text="📎",
            width=40,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            hover_color="#E0E0E0",
            text_color="#757575"
        )
        self.attach_button.pack(side="left", padx=(0, 5))

        self.entry = ctk.CTkEntry(
            input_container,
            placeholder_text="Напишите сообщение...",
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=20,
            border_width=1,
            border_color="#E0E0E0"
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
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

        self.message_widgets = []
        self.suggestion_buttons = []
        self.update_suggestions()

        self.add_message("ChatBot", "Привет! Я готов к общению! 😊", False)

    def update_suggestions(self):
        """Обновляет рекомендации в стиле Telegram"""
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
                fg_color="#E3F2FD",
                hover_color="#BBDEFB",
                text_color="#1976D2",
                border_width=1,
                border_color="#2196F3",
                command=lambda s=suggestion: self.use_suggestion(s)
            )
            btn.pack(fill="x", pady=3)
            self.suggestion_buttons.append(btn)

        separator = ctk.CTkFrame(self.suggestions_scroll, height=1, fg_color="#E0E0E0")
        separator.pack(fill="x", pady=10)

        refresh_btn = ctk.CTkButton(
            self.suggestions_scroll,
            text="🔄 Обновить предложения",
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
        """Использует рекомендацию"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, suggestion)
        self.send_message()

    def find_pattern_response(self, message):
        """Ищет совпадения с шаблонами"""
        for pattern, response_template in patterns:
            match = re.search(pattern, message.lower())
            if match:
                if '{}' in response_template:
                    return response_template.format(match.group(1))
                else:
                    return response_template
        return None

    def get_fuzzy_match(self, message):
        """Простой поиск по ключевым словам"""
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

        self.add_message("Вы", user_msg, True)

        bot_msg = None

        bot_msg = responses.get(user_msg.lower())

        if not bot_msg:
            bot_msg = self.find_pattern_response(user_msg)

        if not bot_msg:
            bot_msg = self.get_fuzzy_match(user_msg)

        # 4. Стандартный ответ
        if not bot_msg:
            default_responses = [
                "Интересно! Расскажи больше 🤔",
                "Я пока не знаю, что ответить 😅",
                "Хм, это новое для меня 🧐",
                "Можешь переформулировать? 🤖"
            ]
            bot_msg = random.choice(default_responses)

        self.after(500, lambda: self.add_message("ChatBot", bot_msg, False))

        if random.randint(1, 5) == 1:
            self.update_suggestions()

    def add_message(self, sender, text, is_user=False):
        """Добавляет сообщение в стиле Telegram"""
        timestamp = datetime.now().strftime("%H:%M")

        message_widget = TelegramMessage(
            self.messages_frame,
            sender,
            text,
            timestamp,
            is_user
        )
        message_widget.pack(fill="x", pady=2)
        self.message_widgets.append(message_widget)

        self.after(100, lambda: self.messages_frame._parent_canvas.yview_moveto(1.0))


if __name__ == "__main__":
    app = ChatBotApp()
    app.mainloop()