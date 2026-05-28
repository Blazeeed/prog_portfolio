# Числа Фибоначчи: корутина и класс-итератор

## Цель работы

Изучить работу с итераторами, генераторами и сопрограммами (корутинами) на языке Python.

В рамках работы необходимо:

* реализовать корутину `my_genn()`, принимающую число через `send()` и возвращающую список первых n чисел Фибоначчи;
* реализовать класс-итератор `FibonacchiLst`, который из переданного списка извлекает только числа Фибоначчи;
* реализовать вспомогательные функции для проверки принадлежности числа к ряду Фибоначчи;
* разработать модульные тесты с использованием `unittest`.

---

## Постановка задачи

### Задание 1 — корутина `my_genn()`

Реализовать корутину, которая:

* принимает число `n` через метод `send()`;
* возвращает список первых `n` чисел последовательности Фибоначчи (начиная с 0);
* работает в бесконечном цикле до явного завершения.

#### Пример использования

```python
gen = my_genn()
next(gen)          # инициализация корутины
gen.send(3)        # → [0, 1, 1]
gen.send(5)        # → [0, 1, 1, 2, 3]
gen.send(8)        # → [0, 1, 1, 2, 3, 5, 8, 13]
```

### Задание 2 — класс-итератор `FibonacchiLst`

Реализовать класс-итератор, который:

* принимает список целых чисел;
* при итерации возвращает только те элементы, которые принадлежат ряду Фибоначчи;
* реализует методы `__iter__` и `__next__`.

#### Пример использования

```python
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
list(FibonacchiLst(lst))  # → [0, 1, 2, 3, 5, 8, 1]
```

---

## Теоретические сведения

### Сопрограммы (корутины)

Корутина — это специальный тип генератора, который может не только отдавать значения через `yield`, но и принимать значения через `send()`.

```python
def coroutine():
    value = yield          # ожидает значение через send()
    while True:
        value = yield process(value)
```

Перед первым вызовом `send()` необходимо инициализировать корутину вызовом `next()`.

### Итераторы

Итератор — это объект, реализующий методы `__iter__` и `__next__`. Метод `__next__` возвращает следующий элемент или вызывает `StopIteration`, когда элементы исчерпаны.

### Числа Фибоначчи

Число `n` является числом Фибоначчи тогда и только тогда, когда одно из выражений `(5n² + 4)` или `(5n² − 4)` является точным квадратом:

```python
def is_perfect_square(x):
    s = int(x ** 0.5)
    return s * s == x

is_fib = is_perfect_square(5*n*n + 4) or is_perfect_square(5*n*n - 4)
```

---

## Описание алгоритмов

### `_is_fibonacci(n)` — проверка числа

Проверяет, является ли неотрицательное целое число числом Фибоначчи, используя свойство идеального квадрата.

| Входное значение | Результат |
|---|---|
| 0, 1, 2, 3, 5, 8, 13, 21, ... | `True` |
| 4, 6, 7, 9, 10, ... | `False` |
| Отрицательные числа | `False` |

### `_fib_list(n)` — генерация списка

Строит список первых `n` чисел Фибоначчи итеративно:

| n | Результат |
|---|---|
| 0 | `[]` |
| 1 | `[0]` |
| 2 | `[0, 1]` |
| 3 | `[0, 1, 1]` |
| 8 | `[0, 1, 1, 2, 3, 5, 8, 13]` |

### Корутина `my_genn()`

```text
1. yield None          ← инициализация (next(gen))
2. Ожидает n через send(n)
3. Вычисляет _fib_list(n)
4. yield результат
5. Переходит к шагу 2
```

### Класс-итератор `FibonacchiLst`

```text
1. Хранит исходный список и текущий индекс
2. __next__(): проходит по элементам с текущей позиции
3. Возвращает первый элемент, являющийся числом Фибоначчи
4. StopIteration — когда список исчерпан
```

---

## Листинг программы

### Файл `fib.py`

```python
"""
Числа Фибоначчи: корутина и класс-итератор.

Задание 1 — корутина my_genn():
    Принимает число n через send() и возвращает список первых n чисел
    последовательности Фибоначчи.

Задание 2 — класс FibonacchiLst:
    Из переданного списка извлекает только элементы, принадлежащие
    последовательности Фибоначчи.
"""

from typing import Generator, Iterator


def _is_fibonacci(n: int) -> bool:
    if n < 0:
        return False

    def is_perfect_square(x: int) -> bool:
        s = int(x ** 0.5)
        return s * s == x

    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)


def _fib_list(n: int) -> list[int]:
    if n <= 0:
        return []
    result = [0, 1]
    while len(result) < n:
        result.append(result[-1] + result[-2])
    return result[:n]


def my_genn() -> Generator[list[int], int, None]:
    n = yield
    while True:
        n = yield _fib_list(n)


class FibonacchiLst:
    def __init__(self, lst: list[int]) -> None:
        self._lst = lst
        self._index = 0

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        while self._index < len(self._lst):
            value = self._lst[self._index]
            self._index += 1
            if _is_fibonacci(value):
                return value
        raise StopIteration


if __name__ == "__main__":
    print("=== Задание 1: корутина my_genn() ===")
    gen = my_genn()
    next(gen)
    print(f"send(3) -> {gen.send(3)}")
    print(f"send(5) -> {gen.send(5)}")
    print(f"send(8) -> {gen.send(8)}")

    print("\n=== Задание 2: FibonacchiLst ===")
    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    print(f"Исходный список : {lst}")
    print(f"Числа Фибоначчи : {list(FibonacchiLst(lst))}")
```

---

### Файл `test_fib.py`

```python
import unittest
from fib import _is_fibonacci, _fib_list, my_genn, FibonacchiLst


class TestIsFibonacci(unittest.TestCase):

    def test_zero_is_fib(self):
        self.assertTrue(_is_fibonacci(0))

    def test_one_is_fib(self):
        self.assertTrue(_is_fibonacci(1))

    def test_two_is_fib(self):
        self.assertTrue(_is_fibonacci(2))

    def test_three_is_fib(self):
        self.assertTrue(_is_fibonacci(3))

    def test_five_is_fib(self):
        self.assertTrue(_is_fibonacci(5))

    def test_eight_is_fib(self):
        self.assertTrue(_is_fibonacci(8))

    def test_four_is_not_fib(self):
        self.assertFalse(_is_fibonacci(4))

    def test_six_is_not_fib(self):
        self.assertFalse(_is_fibonacci(6))

    def test_negative_is_not_fib(self):
        self.assertFalse(_is_fibonacci(-1))

    def test_large_fib(self):
        self.assertTrue(_is_fibonacci(144))

    def test_large_non_fib(self):
        self.assertFalse(_is_fibonacci(100))


class TestFibList(unittest.TestCase):

    def test_zero_elements(self):
        self.assertEqual(_fib_list(0), [])

    def test_negative_elements(self):
        self.assertEqual(_fib_list(-5), [])

    def test_one_element(self):
        self.assertEqual(_fib_list(1), [0])

    def test_two_elements(self):
        self.assertEqual(_fib_list(2), [0, 1])

    def test_three_elements(self):
        self.assertEqual(_fib_list(3), [0, 1, 1])

    def test_five_elements(self):
        self.assertEqual(_fib_list(5), [0, 1, 1, 2, 3])

    def test_eight_elements(self):
        self.assertEqual(_fib_list(8), [0, 1, 1, 2, 3, 5, 8, 13])

    def test_length_matches(self):
        for n in range(10):
            with self.subTest(n=n):
                self.assertEqual(len(_fib_list(n)), max(n, 0))


class TestMyGenn(unittest.TestCase):

    def setUp(self):
        self.gen = my_genn()
        next(self.gen)

    def test_send_3(self):
        self.assertEqual(self.gen.send(3), [0, 1, 1])

    def test_send_5(self):
        self.assertEqual(self.gen.send(5), [0, 1, 1, 2, 3])

    def test_send_8(self):
        self.assertEqual(self.gen.send(8), [0, 1, 1, 2, 3, 5, 8, 13])

    def test_send_1(self):
        self.assertEqual(self.gen.send(1), [0])

    def test_send_2(self):
        self.assertEqual(self.gen.send(2), [0, 1])

    def test_send_0_returns_empty(self):
        self.assertEqual(self.gen.send(0), [])

    def test_multiple_sends(self):
        self.assertEqual(self.gen.send(3), [0, 1, 1])
        self.assertEqual(self.gen.send(5), [0, 1, 1, 2, 3])
        self.assertEqual(self.gen.send(1), [0])

    def test_is_generator(self):
        import types
        self.assertIsInstance(self.gen, types.GeneratorType)


class TestFibonacchiLst(unittest.TestCase):

    def test_main_example(self):
        lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
        self.assertEqual(list(FibonacchiLst(lst)), [0, 1, 2, 3, 5, 8, 1])

    def test_empty_list(self):
        self.assertEqual(list(FibonacchiLst([])), [])

    def test_single_zero(self):
        self.assertEqual(list(FibonacchiLst([0])), [0])

    def test_two_elements(self):
        self.assertEqual(list(FibonacchiLst([0, 1])), [0, 1])

    def test_repeated_ones(self):
        self.assertEqual(list(FibonacchiLst([1, 1])), [1, 1])

    def test_no_fibonacci_numbers(self):
        self.assertEqual(list(FibonacchiLst([4, 6, 7, 9])), [])

    def test_all_fibonacci_numbers(self):
        self.assertEqual(list(FibonacchiLst([0, 1, 1, 2, 3, 5])), [0, 1, 1, 2, 3, 5])

    def test_is_iterable(self):
        fib_iter = FibonacchiLst([1, 2, 3])
        self.assertIs(iter(fib_iter), fib_iter)

    def test_stop_iteration(self):
        fib_iter = FibonacchiLst([1])
        next(fib_iter)
        with self.assertRaises(StopIteration):
            next(fib_iter)

    def test_for_loop(self):
        result = []
        for x in FibonacchiLst([0, 4, 1, 6, 2, 9]):
            result.append(x)
        self.assertEqual(result, [0, 1, 2])

    def test_large_numbers(self):
        self.assertEqual(list(FibonacchiLst([144, 100, 233])), [144, 233])

    def test_negative_numbers_excluded(self):
        self.assertEqual(list(FibonacchiLst([-1, 0, -2, 1])), [0, 1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

---

## Результаты тестирования

### TestIsFibonacci (11 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_zero_is_fib` | 0 является числом Фибоначчи | ✅ OK |
| 2 | `test_one_is_fib` | 1 является числом Фибоначчи | ✅ OK |
| 3 | `test_two_is_fib` | 2 является числом Фибоначчи | ✅ OK |
| 4 | `test_three_is_fib` | 3 является числом Фибоначчи | ✅ OK |
| 5 | `test_five_is_fib` | 5 является числом Фибоначчи | ✅ OK |
| 6 | `test_eight_is_fib` | 8 является числом Фибоначчи | ✅ OK |
| 7 | `test_four_is_not_fib` | 4 не является числом Фибоначчи | ✅ OK |
| 8 | `test_six_is_not_fib` | 6 не является числом Фибоначчи | ✅ OK |
| 9 | `test_negative_is_not_fib` | -1 не является числом Фибоначчи | ✅ OK |
| 10 | `test_large_fib` | 144 является числом Фибоначчи | ✅ OK |
| 11 | `test_large_non_fib` | 100 не является числом Фибоначчи | ✅ OK |

### TestFibList (8 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_zero_elements` | `_fib_list(0)` → `[]` | ✅ OK |
| 2 | `test_negative_elements` | `_fib_list(-5)` → `[]` | ✅ OK |
| 3 | `test_one_element` | `_fib_list(1)` → `[0]` | ✅ OK |
| 4 | `test_two_elements` | `_fib_list(2)` → `[0, 1]` | ✅ OK |
| 5 | `test_three_elements` | `_fib_list(3)` → `[0, 1, 1]` | ✅ OK |
| 6 | `test_five_elements` | `_fib_list(5)` → `[0, 1, 1, 2, 3]` | ✅ OK |
| 7 | `test_eight_elements` | `_fib_list(8)` → `[0, 1, 1, 2, 3, 5, 8, 13]` | ✅ OK |
| 8 | `test_length_matches` | Длина списка совпадает с n | ✅ OK |

### TestMyGenn (8 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_send_3` | `send(3)` → `[0, 1, 1]` | ✅ OK |
| 2 | `test_send_5` | `send(5)` → `[0, 1, 1, 2, 3]` | ✅ OK |
| 3 | `test_send_8` | `send(8)` → `[0, 1, 1, 2, 3, 5, 8, 13]` | ✅ OK |
| 4 | `test_send_1` | `send(1)` → `[0]` | ✅ OK |
| 5 | `test_send_2` | `send(2)` → `[0, 1]` | ✅ OK |
| 6 | `test_send_0_returns_empty` | `send(0)` → `[]` | ✅ OK |
| 7 | `test_multiple_sends` | Несколько последовательных вызовов `send()` | ✅ OK |
| 8 | `test_is_generator` | Объект является генератором (`GeneratorType`) | ✅ OK |

### TestFibonacchiLst (12 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_main_example` | `[0,1,2,3,4,5,6,7,8,9,1]` → `[0,1,2,3,5,8,1]` | ✅ OK |
| 2 | `test_empty_list` | Пустой список → `[]` | ✅ OK |
| 3 | `test_single_zero` | `[0]` → `[0]` | ✅ OK |
| 4 | `test_two_elements` | `[0, 1]` → `[0, 1]` | ✅ OK |
| 5 | `test_repeated_ones` | `[1, 1]` → `[1, 1]` | ✅ OK |
| 6 | `test_no_fibonacci_numbers` | `[4, 6, 7, 9]` → `[]` | ✅ OK |
| 7 | `test_all_fibonacci_numbers` | Все числа Фибоначчи → без изменений | ✅ OK |
| 8 | `test_is_iterable` | `iter(obj) is obj` | ✅ OK |
| 9 | `test_stop_iteration` | `StopIteration` после исчерпания | ✅ OK |
| 10 | `test_for_loop` | Работа в цикле `for` | ✅ OK |
| 11 | `test_large_numbers` | `[144, 100, 233]` → `[144, 233]` | ✅ OK |
| 12 | `test_negative_numbers_excluded` | `[-1, 0, -2, 1]` → `[0, 1]` | ✅ OK |

```
Ran 39 tests in 0.002s

OK
```

---

## Используемые библиотеки

| Библиотека | Назначение |
|---|---|
| `typing` | Аннотации типов (`Generator`, `Iterator`) |
| `unittest` | Модульное тестирование |

---

## Структура файлов

```
├── fib.py          # Корутина my_genn() и итератор FibonacchiLst
└── test_fib.py     # Модульные тесты (unittest)
```

---

## Вывод

В ходе выполнения работы реализованы два инструмента для работы с числами Фибоначчи:

* корутина `my_genn()`, принимающая число `n` через `send()` и возвращающая список первых `n` чисел Фибоначчи;
* класс-итератор `FibonacchiLst`, фильтрующий числа Фибоначчи из произвольного списка.

Для проверки принадлежности числа к ряду Фибоначчи используется свойство идеального квадрата: O(1) по времени и памяти. Генерация списка выполняется итеративно за O(n).

Разработаны 39 модульных тестов (unittest), охватывающих граничные и нестандартные случаи.

---

## 📁 Файлы проекта

| Файл | Описание |
|---|---|
| [fib.py](lab5/fib.py) | Корутина `my_genn()` и итератор `FibonacchiLst` |
| [test_fib.py](lab5/test_fib.py) | Модульные тесты |
