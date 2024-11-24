import json
from typing import List, Dict
import os

DATA_FILE = os.path.abspath("../logs/library_data.json")


class Book:

    """Класс для представления книги"""

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:

        """Возвращает данные книги в виде словаря"""

        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict):

        """Возвращает экземпляр книги из словаря"""

        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class Library:

    """Класс для управления библиотекой"""

    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):

        """Загружает книги из файла"""

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self):

        """Сохраняет книги в файл"""

        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):

        """Добавляет книгу в библиотеку"""

        book_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга добавлена: {new_book.to_dict()}")

    def delete_book(self, book_id: int):

        """Удаляет книгу по ID"""

        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, query: str, field: str):

        """Ищет книги по указанному полю"""

        valid_fields = {"title", "author", "year"}
        if field not in valid_fields:
            print("Ошибка: поле для поиска должно быть 'title', 'author' или 'year'.")
            return
        results = [book for book in self.books if query.lower() in str(getattr(book, field)).lower()]
        if results:
            for book in results:
                print(book.to_dict())
        else:
            print("Книги не найдены.")

    def display_books(self):

        """Выводит список всех книг"""

        if self.books:
            for book in self.books:
                print(book.to_dict())
        else:
            print("Библиотека пуста.")

    def update_status(self, book_id: int, new_status: str):

        """Изменяет статус книги"""

        valid_statuses = {"в наличии", "выдана"}
        if new_status not in valid_statuses:
            print(f"Ошибка: статус должен быть одним из {valid_statuses}.")
            return
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                print(f"Статус книги с ID {book_id} обновлен на '{new_status}'.")
                return
        print(f"Книга с ID {book_id} не найдена.")


def get_valid_int(prompt: str) -> int:

    """Получает валидное целое число от пользователя"""

    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                raise ValueError("Число должно быть неотрицательным.")
            return value
        except ValueError as e:
            print(f"Ошибка ввода: {e}. Попробуйте снова.")


def get_valid_string(prompt: str, allow_empty: bool = False) -> str:

    """Получает валидную строку от пользователя"""

    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Ошибка ввода: строка не может быть пустой. Попробуйте снова.")


def main():
    library = Library()
    print("Добро пожаловать в систему управления библиотекой!")
    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            title = get_valid_string("Введите название книги: ")
            author = get_valid_string("Введите автора книги: ")
            year = get_valid_int("Введите год издания (например, 2022): ")
            library.add_book(title, author, year)
        elif choice == "2":
            book_id = get_valid_int("Введите ID книги: ")
            library.delete_book(book_id)
        elif choice == "3":
            field = get_valid_string("Введите поле для поиска (title, author, year): ")
            query = get_valid_string("Введите запрос: ")
            library.search_books(query, field)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = get_valid_int("Введите ID книги: ")
            new_status = get_valid_string("Введите новый статус ('в наличии' или 'выдана'): ")
            library.update_status(book_id, new_status)
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
