# Решение задачи деления с использованием конфигурационного файла

## Цель работы

Разработать программу на языке Python, которая:

1. Выполняет деление двух чисел с заданной точностью.
2. Загружает значение точности из конфигурационного файла.
3. Выполняет обработку ошибок через исключения.
4. Использует модульное тестирование для проверки корректности работы.

---

## Постановка задачи

### Задание

1. Написать функцию `calculate`, которая:

   * принимает два операнда и параметр точности `epsilon`;
   * выполняет деление первого операнда на второй;
   * бросает `ZeroDivisionError` при делении на ноль;
   * бросает `ValueError` если `epsilon` вне допустимого диапазона.

   Допустимый диапазон значений:

   ```text
   10^-9 ≤ epsilon ≤ 10^-1
   ```

2. Написать функцию `load_params`, которая:

   * считывает значение `epsilon` из файла `settings.ini`;
   * бросает `FileNotFoundError` если файл не найден;
   * бросает `ValueError` если значение epsilon не является числом или вне диапазона.

3. Реализовать тестирование с использованием `pytest`:

   Для функции `calculate`:

   * деление 1/2 и 1/1000;
   * деление на ноль;
   * epsilon вне допустимого диапазона;
   * дробные операнды, отрицательные числа.

   Для функции `load_params`:

   * успешное чтение из файла;
   * отсутствие файла;
   * неверный формат числа;
   * epsilon вне диапазона.

---

## Описание решения

Программа состоит из следующих частей:

1. Функция `calculate` — выполняет деление с проверкой входных данных.
2. Функция `load_params` — загружает параметры из конфигурационного файла.
3. Конфигурационный файл `settings.ini` — хранит значение `epsilon`.
4. Набор тестов `test_calculate.py` с использованием `pytest`.

### Алгоритм вычисления

Количество знаков после запятой определяется из `epsilon` через логарифм:

```python
decimal_places = round(-math.log10(epsilon))
return round(a / b, decimal_places)
```

| epsilon | decimal_places | Пример |
|---------|----------------|--------|
| 0.1 | 1 | `1/2` → `0.5` |
| 0.01 | 2 | `1/3` → `0.33` |
| 0.001 | 3 | `1/1000` → `0.001` |
| 0.0001 | 4 | (по умолчанию) |

---

## Листинг программы

### Файл `calculate.py`

```python
import math
import configparser


def calculate(a, b, *, epsilon=0.0001):
    """Делит a на b, результат округляется до точности epsilon.
    epsilon должен быть в диапазоне (10**-9, 10**-1).
    """
    if not (1e-9 <= epsilon <= 1e-1):
        raise ValueError(
            f"epsilon={epsilon} вне допустимого диапазона (10**-9, 10**-1)"
        )
    if b == 0:
        raise ZeroDivisionError("Деление на ноль недопустимо")

    decimal_places = round(-math.log10(epsilon))
    return round(a / b, decimal_places)


def load_params(config_path="settings.ini"):
    """Считывает epsilon из конфигурационного файла и возвращает его."""
    config = configparser.ConfigParser()
    files_read = config.read(config_path, encoding="utf-8")
    if not files_read:
        raise FileNotFoundError(f"Файл конфигурации '{config_path}' не найден")

    try:
        epsilon = float(config["DEFAULT"]["epsilon"])
    except (KeyError, ValueError) as e:
        raise ValueError(f"Некорректный формат epsilon в файле конфигурации: {e}")

    if not (1e-9 <= epsilon <= 1e-1):
        raise ValueError(
            f"epsilon={epsilon} из конфигурации вне допустимого диапазона (10**-9, 10**-1)"
        )

    return epsilon
```

---

### Конфигурационный файл `settings.ini`

```ini
[DEFAULT]
epsilon = 0.0001
```

---

### Файл `test_calculate.py`

```python
import pytest
import os
import configparser
from calculate import calculate, load_params


# ---------- Тесты для calculate ----------

class TestCalculate:

    def test_half(self):
        """1/2 с epsilon=0.1 должен вернуть 0.5"""
        assert calculate(1, 2, epsilon=0.1) == 0.5

    def test_one_thousandth(self):
        """1/1000 с epsilon=0.001 должен вернуть 0.001"""
        assert calculate(1, 1000, epsilon=0.001) == 0.001

    def test_division_by_zero(self):
        """Деление на ноль должно выбрасывать ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            calculate(1, 0)

    def test_default_epsilon(self):
        """Деление с epsilon по умолчанию (0.0001)"""
        assert calculate(1, 3) == round(1 / 3, 4)

    def test_float_operands(self):
        """Дробные операнды"""
        assert calculate(2.5, 0.5, epsilon=0.01) == 5.0

    def test_epsilon_too_large(self):
        """epsilon > 10**-1 должен выбрасывать ValueError"""
        with pytest.raises(ValueError):
            calculate(1, 2, epsilon=0.2)

    def test_epsilon_too_small(self):
        """epsilon < 10**-9 должен выбрасывать ValueError"""
        with pytest.raises(ValueError):
            calculate(1, 2, epsilon=1e-10)

    def test_epsilon_valid_boundary(self):
        """epsilon на границе диапазона (0.1) не должен вызывать ошибку"""
        result = calculate(1, 2, epsilon=0.1)
        assert result == 0.5

    def test_negative_operands(self):
        """Отрицательные операнды"""
        assert calculate(-1, 2, epsilon=0.01) == -0.5


# ---------- Тесты для load_params ----------

class TestLoadParams:

    def test_file_opens_for_reading(self, tmp_path):
        """Файл конфигурации успешно открывается"""
        config_file = tmp_path / "settings.ini"
        config_file.write_text("[DEFAULT]\nepsilon = 0.001\n", encoding="utf-8")
        epsilon = load_params(str(config_file))
        assert epsilon == 0.001

    def test_epsilon_in_valid_range(self, tmp_path):
        """epsilon из конфига входит в допустимый диапазон"""
        config_file = tmp_path / "settings.ini"
        config_file.write_text("[DEFAULT]\nepsilon = 0.00001\n", encoding="utf-8")
        epsilon = load_params(str(config_file))
        assert 1e-9 < epsilon < 1e-1

    def test_epsilon_out_of_range(self, tmp_path):
        """epsilon вне диапазона выбрасывает ValueError"""
        config_file = tmp_path / "settings.ini"
        config_file.write_text("[DEFAULT]\nepsilon = 0.5\n", encoding="utf-8")
        with pytest.raises(ValueError):
            load_params(str(config_file))

    def test_invalid_number_format(self, tmp_path):
        """Некорректный формат числа в конфиге выбрасывает ValueError"""
        config_file = tmp_path / "settings.ini"
        config_file.write_text("[DEFAULT]\nepsilon = abc\n", encoding="utf-8")
        with pytest.raises(ValueError):
            load_params(str(config_file))

    def test_file_not_found(self):
        """Отсутствующий файл выбрасывает FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            load_params("nonexistent_settings.ini")

    def test_load_and_use_in_calculate(self, tmp_path):
        """epsilon из конфига передаётся в calculate и работает корректно"""
        config_file = tmp_path / "settings.ini"
        config_file.write_text("[DEFAULT]\nepsilon = 0.01\n", encoding="utf-8")
        epsilon = load_params(str(config_file))
        assert calculate(1, 2, epsilon=epsilon) == 0.5


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
```

---

## Результаты тестирования

### TestCalculate (9 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_half` | 1/2 с epsilon=0.1 → 0.5 | ✅ PASSED |
| 2 | `test_one_thousandth` | 1/1000 с epsilon=0.001 → 0.001 | ✅ PASSED |
| 3 | `test_division_by_zero` | Деление на ноль → `ZeroDivisionError` | ✅ PASSED |
| 4 | `test_default_epsilon` | Деление с epsilon=0.0001 по умолчанию | ✅ PASSED |
| 5 | `test_float_operands` | 2.5/0.5 с epsilon=0.01 → 5.0 | ✅ PASSED |
| 6 | `test_epsilon_too_large` | epsilon=0.2 → `ValueError` | ✅ PASSED |
| 7 | `test_epsilon_too_small` | epsilon=1e-10 → `ValueError` | ✅ PASSED |
| 8 | `test_epsilon_valid_boundary` | epsilon=0.1 (граница) → без ошибки | ✅ PASSED |
| 9 | `test_negative_operands` | -1/2 → -0.5 | ✅ PASSED |

### TestLoadParams (6 тестов)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_file_opens_for_reading` | Файл открывается, epsilon читается | ✅ PASSED |
| 2 | `test_epsilon_in_valid_range` | epsilon входит в диапазон | ✅ PASSED |
| 3 | `test_epsilon_out_of_range` | epsilon=0.5 → `ValueError` | ✅ PASSED |
| 4 | `test_invalid_number_format` | epsilon='abc' → `ValueError` | ✅ PASSED |
| 5 | `test_file_not_found` | Файл не найден → `FileNotFoundError` | ✅ PASSED |
| 6 | `test_load_and_use_in_calculate` | epsilon из конфига → calculate работает | ✅ PASSED |

```
15 passed in 0.05s
```

---

## Используемые библиотеки

| Библиотека | Назначение |
|---|---|
| `math` | Вычисление количества знаков через `math.log10` |
| `configparser` | Работа с `.ini`-файлами |
| `pytest` | Модульное тестирование |

---

## Структура файлов

```
├── calculate.py       # Функции calculate и load_params
├── settings.ini       # Конфигурационный файл с epsilon
└── test_calculate.py  # Модульные тесты (pytest)
```

---

## Вывод

В ходе выполнения работы была разработана программа для деления чисел с параметром точности `epsilon`, загружаемым из конфигурационного файла `settings.ini`.

В программе реализованы:

* деление с проверкой входных данных и округлением по `epsilon` через `math.log10`;
* корректная обработка ошибок через исключения (`ValueError`, `ZeroDivisionError`, `FileNotFoundError`);
* загрузка параметров из `.ini`-файла через `configparser`;
* 15 тестов с использованием `pytest`, покрывающих основные и граничные случаи.

Программа успешно выполняет поставленные задачи и корректно обрабатывает исключительные ситуации.

---

## 📁 Файлы проекта

| Файл | Описание |
|---|---|
| [calculate.py](lab2/calculate.py) | Функции `calculate` и `load_params` |
| [settings.ini](lab2/settings.ini) | Конфигурационный файл с epsilon |
| [test_calculate.py](lab2/test_calculate.py) | Модульные тесты (pytest) |
