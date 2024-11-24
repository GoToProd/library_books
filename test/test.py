import os
import unittest
from source.main import Library
import logging


file = os.path.abspath("../logs/test_library_data.json")
log_file_path = os.path.abspath("../logs/library_tests.log")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()


class TestLibrary(unittest.TestCase):
    def setUp(self):

        """Подготовка тестового окружения"""

        logger.info("Подготовка тестового окружения")
        self.library = Library(data_file=file)
        self.library.books = []

    def test_add_book(self):

        """Тест добавления книги"""

        logger.info("Начало теста: добавление книги")
        self.library.add_book("Test Title", "Test Author", 2022)
        self.library.add_book("Test Title2", "Test Author2", 2023)
        self.assertEqual(len(self.library.books), 2)
        self.assertEqual(self.library.books[0].title, "Test Title")
        self.assertEqual(self.library.books[1].title, "Test Title2")
        logger.info("Тест успешно завершен: добавление книги\n")

    def test_delete_book(self):

        """Тест удаления книги"""

        logger.info("Начало теста: удаление книги")
        self.library.add_book("Test Title", "Test Author", 2022)
        self.library.delete_book(1)
        self.assertEqual(len(self.library.books), 0)
        logger.info("Тест успешно завершен: удаление книги\n")

    def test_search_books(self):

        """Тест поиска книги"""

        logger.info("Начало теста: поиск книги")
        self.library.add_book("Test Title", "Test Author", 2022)
        results = [book.title for book in self.library.books if "Test" in book.title]
        self.assertIn("Test Title", results)
        logger.info("Тест успешно завершен: поиск книги\n")

    def test_update_status(self):

        """Тест изменения статуса книги"""

        logger.info("Начало теста: изменение статуса книги")
        self.library.add_book("Test Title", "Test Author", 2022)
        self.library.update_status(1, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")
        logger.info("Тест успешно завершен: изменение статуса книги\n")


if __name__ == "__main__":
    logger.info("Запуск тестов")
    unittest.main()
    logger.info("Все тесты завершены")
