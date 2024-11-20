import requests
import tkinter as tk
from tkinter import messagebox

# Налаштування інтерфейсу
display = tk.Tk()
display.title("Search")
display.configure(bg="gray")  # Сіра тема
display.resizable(True, False)  # Дозволено витягування по горизонталі

# Текст запиту
text = tk.Label(display, text="Ваш запит:", bg="gray", fg="white")
text.grid(row=0, column=0, padx=10, pady=5, sticky="w")
input_title = tk.Entry(display, width=40)
input_title.grid(row=0, column=1, padx=10, pady=5)

# Дата
date = tk.Label(display, text="Дата (YYYY-MM-DD):", bg="gray", fg="white")
date.grid(row=1, column=0, padx=10, pady=5, sticky="w")
input_date = tk.Entry(display, width=40)
input_date.grid(row=1, column=1, padx=10, pady=5)

# Кнопка пошуку
search_button = tk.Button(display, text="Шукати", command=lambda: search_news(), bg="lightgray")
search_button.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

# Список результатів
listbox = tk.Listbox(display, height=25, width=80, bg="white", fg="black")
listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# URL та API ключ
URL = "https://newsapi.org/v2/everything?"
API_KEY = "42a2cb2e64f54f41af55c05c50402992"

def search_news():
    query = input_title.get().lower()
    date_title = input_date.get()
    if query.strip():  # Перевірка на порожній запит
        params = {
            "q": query.strip(),
            "from": date_title,  # Дата початку (ISO формат: YYYY-MM-DD)
            "sortBy": "publishedAt",  # Сортування за датою
            "apiKey": API_KEY,  # Ваш API-ключ
        }

        response = requests.get(URL, params=params)  # HTTP-запит
        if response.status_code == 200:  # Успішна відповідь
            data = response.json().get("articles", [])
            listbox.delete(0, tk.END)  # Очистка списку
            if data:
                for article in data:
                    title = article.get("title", "No Title")
                    time = article.get("publishedAt", "No Date")
                    listbox.insert(tk.END, f"Title: {title}")
                    listbox.insert(tk.END, f"Published at: {time}")
                    listbox.insert(tk.END, "-" * 60)
            else:
                listbox.insert(tk.END, "Результатів не знайдено.")
        else:
            messagebox.showerror("Помилка", f"Помилка {response.status_code}: {response.json().get('message', 'Невідома помилка')}")
    else:
        messagebox.showwarning("Попередження", "Введіть запит для пошуку.")

# Налаштування адаптивності
display.columnconfigure(1, weight=1)

display.mainloop()
