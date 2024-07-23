import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # Параметризованный тест для метода add_new_book, который будет запущен трижды с разными
    # значениями book_name и соответствующими ожидаемыми результатами expected.
    # "Клуб неисправимых оптимистов", True: проверка с валидным именем книги.
    # "", False: проверка с пустым именем книги.
    # "bla-" * 11, False: проверка с именем книги, превышающим допустимую длину (40 символов).
    @pytest.mark.parametrize("book_name, expected", [
        ("Клуб неисправимых оптимистов", True),
        ("", False),
        ("bla-" * 11, False),
    ])
    def test_add_new_book_check_valid_name(self, book_name, expected):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert (book_name in collector.get_books_genre()) == expected

    # Тест на добавление существующей книги
    def test_add_existing_book(self):
        collector = BooksCollector()
        collector.add_new_book("Клуб неисправимых оптимистов")
        collector.add_new_book("Клуб неисправимых оптимистов")
        assert len(collector.get_books_genre()) == 1

    # Параметризированный тест для установки жанра книге, включая несуществующий жанр
    @pytest.mark.parametrize("book, genre, expected_genre", [
        ("Дом, в котором...", "Фантастика", "Фантастика"),
        ("Дом, в котором...", "Несуществующий жанр", ""),
    ])
    def test_set_book_genre(self, book, genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        assert collector.get_book_genre(book) == expected_genre

    # Тест для получения жанра книги
    @pytest.mark.parametrize("book, genre", [
        ("451 по Фаренгейту", "Фантастика"),
        ("Поминки по Финнегану", ""),
    ])
    def test_get_book_genre(self, book, genre):
        collector = BooksCollector()
        collector.add_new_book(book)
        if genre:
            collector.set_book_genre(book, genre)
        assert collector.get_book_genre(book) == genre

    # Тест для получения списка книг с определённым жанром
    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book("451 по Фаренгейту")
        collector.set_book_genre("451 по Фаренгейту", "Фантастика")
        collector.add_new_book("Пикник на обочине")
        collector.set_book_genre("Пикник на обочине", "Фантастика")
        assert collector.get_books_with_specific_genre("Фантастика") == ["451 по Фаренгейту", "Пикник на обочине"]

    # Тест для получения словаря books_genre
    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book("451 по Фаренгейту")
        collector.set_book_genre("451 по Фаренгейту", "Фантастика")
        assert collector.get_books_genre() == {"451 по Фаренгейту": "Фантастика"}

    # Тест для получения списка книг для детей
    def test_get_books_for_children(self):
        collector = BooksCollector()
        collector.add_new_book("Ходячий замок")
        collector.set_book_genre("Ходячий замок", "Фантастика")
        collector.add_new_book("Молчание ягнят")
        collector.set_book_genre("Молчание ягнят", "Ужасы")
        assert collector.get_books_for_children() == ["Ходячий замок"]

    # Параметризация тестов для добавления книг в избранное и удаления их из избранного
    @pytest.mark.parametrize("book, add_to_favorites, expected", [
        ("Записки примата", True, ["Записки примата"]),
        ("Уроки химии", True, ["Записки примата", "Уроки химии"]),
        ("Записки примата", False, []),
    ])
    def test_manage_favorites(self, book, add_to_favorites, expected):
        collector = BooksCollector()
        collector.add_new_book("Записки примата")
        collector.add_new_book("Уроки химии")
        if add_to_favorites:
            collector.add_book_in_favorites("Записки примата")
            collector.add_book_in_favorites(book)
        else:
            collector.add_book_in_favorites("Записки примата")
            collector.delete_book_from_favorites("Записки примата")
        assert collector.get_list_of_favorites_books() == expected

    # Тест для получения списка избранных книг
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book("Записки примата")
        collector.add_new_book("Уроки химии")
        collector.add_book_in_favorites("Записки примата")
        collector.add_book_in_favorites("Уроки химии")
        assert collector.get_list_of_favorites_books() == ["Записки примата", "Уроки химии"]