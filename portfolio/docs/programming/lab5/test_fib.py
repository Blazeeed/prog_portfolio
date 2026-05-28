"""Тесты для модуля fib.py.

Покрывают:
    - вспомогательные функции _is_fibonacci и _fib_list
    - корутину my_genn (задание 1)
    - класс-итератор FibonacchiLst (задание 2)
"""

import unittest
from fib import _is_fibonacci, _fib_list, my_genn, FibonacchiLst


class TestIsFibonacci(unittest.TestCase):
    """Тесты вспомогательной функции _is_fibonacci."""

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
    """Тесты вспомогательной функции _fib_list."""

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
    """Тесты корутины my_genn (задание 1)."""

    def setUp(self):
        """Создаёт и инициализирует корутину перед каждым тестом."""
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
        """Несколько последовательных вызовов send."""
        self.assertEqual(self.gen.send(3), [0, 1, 1])
        self.assertEqual(self.gen.send(5), [0, 1, 1, 2, 3])
        self.assertEqual(self.gen.send(1), [0])

    def test_is_generator(self):
        import types
        self.assertIsInstance(self.gen, types.GeneratorType)


class TestFibonacchiLst(unittest.TestCase):
    """Тесты класса-итератора FibonacchiLst (задание 2)."""

    def test_main_example(self):
        """Пример из задания."""
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
        """FibonacchiLst поддерживает протокол итератора."""
        fib_iter = FibonacchiLst([1, 2, 3])
        self.assertIs(iter(fib_iter), fib_iter)

    def test_stop_iteration(self):
        """StopIteration вызывается по завершении."""
        fib_iter = FibonacchiLst([1])
        next(fib_iter)
        with self.assertRaises(StopIteration):
            next(fib_iter)

    def test_for_loop(self):
        """Работа в цикле for."""
        result = []
        for x in FibonacchiLst([0, 4, 1, 6, 2, 9]):
            result.append(x)
        self.assertEqual(result, [0, 1, 2])

    def test_large_numbers(self):
        """Большие числа Фибоначчи."""
        self.assertEqual(list(FibonacchiLst([144, 100, 233])), [144, 233])

    def test_negative_numbers_excluded(self):
        """Отрицательные числа не являются числами Фибоначчи."""
        self.assertEqual(list(FibonacchiLst([-1, 0, -2, 1])), [0, 1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
