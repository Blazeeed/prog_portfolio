# Паттерн «Одиночка» для курсов валют ЦБ РФ

## Цель работы

Изучить применение шаблона проектирования «Одиночка» (Singleton) на языке Python.

В рамках работы необходимо:

* реализовать метакласс `SingletonMeta`, гарантирующий единственность экземпляра;
* реализовать класс `CurrenciesLst` для получения курсов валют из API ЦБ РФ;
* реализовать метод `fetch()` для загрузки курсов по идентификаторам;
* реализовать визуализацию курсов через `matplotlib`;
* разработать тесты с использованием `unittest.mock`.

---

## Постановка задачи

### Задание

1. Реализовать метакласс `SingletonMeta`:
   * обеспечить создание единственного экземпляра класса;
   * повторные вызовы конструктора должны возвращать тот же объект.

2. Реализовать класс `CurrenciesLst` (на основе `SingletonMeta`):
   * метод `fetch(currencies_ids_lst)` — загружает курсы из XML API ЦБ РФ;
   * для корректных ID возвращает `{CharCode: (Name, (int_part, frac_part))}`;
   * для некорректных ID возвращает `{id: None}`;
   * ограничение частоты запросов через `min_interval`.

3. Реализовать метод `visualize_currencies()`:
   * строит столбчатый график курсов через `matplotlib`;
   * сохраняет график в файл `.jpg`.

Источник данных:

```text
http://www.cbr.ru/scripts/XML_daily.asp
```

---

## Теоретические сведения

### Паттерн «Одиночка»

Паттерн «Одиночка» гарантирует, что класс имеет только один экземпляр, и предоставляет глобальную точку доступа к нему.

Реализация через метакласс — наиболее «питоновский» способ:

```python
class SingletonMeta(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
```

### Формат данных API ЦБ РФ (XML)

API возвращает XML-документ с узлами `<Valute>`:

```xml
<Valute ID="R01035">
    <CharCode>GBP</CharCode>
    <Name>Фунт стерлингов...</Name>
    <Nominal>1</Nominal>
    <Value>113,2069</Value>
</Valute>
```

Значение курса хранится с запятой как разделителем десятичных знаков. Функция `_split_value()` разбивает строку на целую и дробную части.

---

## Описание решения

### Вспомогательная функция `_split_value(value_str)`

Разбивает строку курса на кортеж `(целая_часть, дробная_часть)`:

| Входное значение | Результат |
|---|---|
| `'113,2069'` | `('113', '2069')` |
| `'90,0000'` | `('90', '0000')` |
| `'90'` (без запятой) | `('90', '0')` |

### Метод `fetch(currencies_ids_lst)`

```text
1. Ждёт min_interval с момента последнего запроса (throttle)
2. GET http://www.cbr.ru/scripts/XML_daily.asp
3. Парсит XML через ElementTree
4. Для каждого ID в списке:
   - Найден → добавляет {CharCode: (Name, (int_part, frac_part))}
   - Не найден → добавляет {id: None}
5. Обновляет cur_lst и возвращает результат
```

### Метод `visualize_currencies()`

Строит столбчатый график на основе `cur_lst` и сохраняет в `.jpg` файл.

---

## Листинг программы

### Файл `currencies.py`

```python
"""
Курсы валют ЦБ РФ с паттерном «Одиночка» (Singleton).

Реализует:
    SingletonMeta  — метакласс для паттерна «Одиночка»
    CurrenciesLst  — класс-одиночка для работы с курсами валют
    get_currencies — вспомогательная функция (совместимость с шаблоном)

API ЦБ РФ: http://www.cbr.ru/scripts/XML_daily.asp
"""

from __future__ import annotations

import time
from typing import Any, Optional
from xml.etree import ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import requests


def _split_value(value_str: str) -> tuple[str, str]:
    parts = value_str.split(",")
    if len(parts) == 2:
        return (parts[0], parts[1])
    return (parts[0], "0")


def _parse_valute(node: ET.Element, ids: list[str]) -> Optional[dict[str, Any]]:
    valute_id = node.get("ID", "")
    if valute_id not in ids:
        return None

    charcode: str = node.find("CharCode").text
    name: str = node.find("Name").text
    value_str: str = node.find("Value").text
    nominal_str: str = node.find("Nominal").text

    int_part, frac_part = _split_value(value_str)

    if nominal_str != "1":
        return {charcode: (name, (int_part, frac_part), nominal_str)}
    return {charcode: (name, (int_part, frac_part))}


class SingletonMeta(type):
    _instances: dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class CurrenciesLst(metaclass=SingletonMeta):
    def __init__(self, min_interval: float = 1.0) -> None:
        self.__cur_lst: list[dict[str, Any]] = []
        self.__min_interval: float = min_interval
        self.__last_request_time: float = 0.0

    def __del__(self) -> None:
        self.__cur_lst.clear()

    @property
    def cur_lst(self) -> list[dict[str, Any]]:
        return self.__cur_lst

    @cur_lst.setter
    def cur_lst(self, value: list[dict[str, Any]]) -> None:
        if not isinstance(value, list):
            raise TypeError("cur_lst должен быть списком")
        self.__cur_lst = value

    @property
    def min_interval(self) -> float:
        return self.__min_interval

    @min_interval.setter
    def min_interval(self, value: float) -> None:
        if value < 0:
            raise ValueError("min_interval не может быть отрицательным")
        self.__min_interval = value

    def fetch(self, currencies_ids_lst: list[str]) -> list[dict[str, Any]]:
        self._throttle()

        response = requests.get(
            "http://www.cbr.ru/scripts/XML_daily.asp", timeout=10
        )
        response.raise_for_status()

        root = ET.fromstring(response.content)
        result: list[dict[str, Any]] = []
        found_ids: set[str] = set()

        for node in root.findall("Valute"):
            entry = _parse_valute(node, currencies_ids_lst)
            if entry is not None:
                found_ids.add(node.get("ID", ""))
                result.append(entry)

        for cid in currencies_ids_lst:
            if cid not in found_ids:
                result.append({cid: None})

        self.__cur_lst = result
        return result

    def _throttle(self) -> None:
        elapsed = time.time() - self.__last_request_time
        if elapsed < self.__min_interval:
            time.sleep(self.__min_interval - elapsed)
        self.__last_request_time = time.time()

    def visualize_currencies(self, output_path: str = "currencies.jpg") -> None:
        labels: list[str] = []
        values: list[float] = []

        for entry in self.__cur_lst:
            for code, data in entry.items():
                if data is None:
                    continue
                int_part, frac_part = data[1]
                value = float(f"{int_part}.{frac_part}")
                labels.append(code)
                values.append(value)

        if not labels:
            print("Нет данных для построения графика.")
            return

        fig, ax = plt.subplots(figsize=(max(6, len(labels) * 1.2), 5))
        bars = ax.bar(labels, values, color="steelblue", edgecolor="white")
        ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=9)
        ax.set_ylabel("Курс (руб.)")
        ax.set_title("Курсы валют ЦБ РФ")
        ax.set_ylim(0, max(values) * 1.15)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close(fig)
        print(f"График сохранён: {output_path}")


def get_currencies(currencies_ids_lst: list[str]) -> list[dict[str, Any]]:
    return CurrenciesLst().fetch(currencies_ids_lst)


if __name__ == "__main__":
    ids = ["R01035", "R01335", "R01700J"]
    cl = CurrenciesLst(min_interval=1.0)
    result = cl.fetch(ids)
    for entry in result:
        print(entry)
    cl.visualize_currencies("currencies.jpg")
```

---

### Файл `test_currencies.py`

```python
"""Тесты для модуля currencies.py."""

import unittest
from unittest.mock import MagicMock, patch

from currencies import (
    CurrenciesLst,
    SingletonMeta,
    _split_value,
    get_currencies,
)

SAMPLE_XML: bytes = """<?xml version="1.0" encoding="utf-8"?>
<ValCurs Date="15.01.2024" name="Foreign Currency Market">
  <Valute ID="R01035">
    <NumCode>826</NumCode>
    <CharCode>GBP</CharCode>
    <Nominal>1</Nominal>
    <Name>Фунт стерлингов Соединенного королевства</Name>
    <Value>113,2069</Value>
    <VunitRate>113,2069</VunitRate>
  </Valute>
  <Valute ID="R01335">
    <NumCode>398</NumCode>
    <CharCode>KZT</CharCode>
    <Nominal>100</Nominal>
    <Name>Казахстанских тенге</Name>
    <Value>19,8264</Value>
    <VunitRate>0,198264</VunitRate>
  </Valute>
  <Valute ID="R01700J">
    <NumCode>949</NumCode>
    <CharCode>TRY</CharCode>
    <Nominal>1</Nominal>
    <Name>Турецких лир</Name>
    <Value>2,7100</Value>
    <VunitRate>2,7100</VunitRate>
  </Valute>
</ValCurs>""".encode("utf-8")


def _make_mock_response(xml: bytes = SAMPLE_XML) -> MagicMock:
    mock = MagicMock()
    mock.content = xml
    mock.raise_for_status = MagicMock()
    return mock


class TestSplitValue(unittest.TestCase):

    def test_normal_value(self) -> None:
        self.assertEqual(_split_value("113,2069"), ("113", "2069"))

    def test_zero_fraction(self) -> None:
        self.assertEqual(_split_value("90"), ("90", "0"))

    def test_zero_value(self) -> None:
        self.assertEqual(_split_value("0,0000"), ("0", "0000"))


class TestSingletonMeta(unittest.TestCase):

    def test_same_instance(self) -> None:
        a = CurrenciesLst()
        b = CurrenciesLst()
        self.assertIs(a, b)

    def test_singleton_uses_metaclass(self) -> None:
        self.assertIsInstance(CurrenciesLst, SingletonMeta)


class TestValidCurrencies(unittest.TestCase):

    @patch("currencies.requests.get")
    def test_gbp_name(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()
        result = CurrenciesLst().fetch(["R01035"])
        gbp_data = result[0].get("GBP")
        self.assertIn("Фунт", gbp_data[0])

    @patch("currencies.requests.get")
    def test_gbp_value_in_range(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()
        result = CurrenciesLst().fetch(["R01035"])
        int_part, frac_part = result[0]["GBP"][1]
        value = float(f"{int_part}.{frac_part}")
        self.assertGreater(value, 0)
        self.assertLess(value, 999)

    @patch("currencies.requests.get")
    def test_try_name(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()
        result = CurrenciesLst().fetch(["R01700J"])
        self.assertIn("лир", result[0]["TRY"][0])

    @patch("currencies.requests.get")
    def test_try_value_in_range(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()
        result = CurrenciesLst().fetch(["R01700J"])
        int_part, frac_part = result[0]["TRY"][1]
        value = float(f"{int_part}.{frac_part}")
        self.assertGreater(value, 0)
        self.assertLess(value, 999)


class TestInvalidCurrencies(unittest.TestCase):

    @patch("currencies.requests.get")
    def test_invalid_id_returns_none(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()
        result = CurrenciesLst().fetch(["R9999"])
        self.assertEqual(result, [{"R9999": None}])

    @patch("currencies.requests.get")
    def test_mixed_ids(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()
        result = CurrenciesLst().fetch(["R01035", "R9999"])
        codes = {}
        for entry in result:
            codes.update(entry)
        self.assertIn("GBP", codes)
        self.assertIsNone(codes["R9999"])


class TestNominal(unittest.TestCase):

    @patch("currencies.requests.get")
    def test_kzt_stores_nominal(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()
        result = CurrenciesLst().fetch(["R01335"])
        kzt_data = result[0].get("KZT")
        self.assertEqual(len(kzt_data), 3)
        self.assertEqual(kzt_data[2], "100")


class TestGettersSetters(unittest.TestCase):

    def setUp(self) -> None:
        SingletonMeta._instances.clear()
        self.cl = CurrenciesLst()

    def test_cur_lst_getter(self) -> None:
        self.assertIsInstance(self.cl.cur_lst, list)

    def test_cur_lst_setter(self) -> None:
        data = [{"USD": ("Доллар", ("90", "0000"))}]
        self.cl.cur_lst = data
        self.assertEqual(self.cl.cur_lst, data)

    def test_cur_lst_setter_type_error(self) -> None:
        with self.assertRaises(TypeError):
            self.cl.cur_lst = "не список"

    def test_min_interval_setter(self) -> None:
        self.cl.min_interval = 2.0
        self.assertEqual(self.cl.min_interval, 2.0)

    def test_min_interval_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.cl.min_interval = -1.0


class TestGetCurrenciesWrapper(unittest.TestCase):

    @patch("currencies.requests.get")
    def test_wrapper_returns_list(self, mock_get: MagicMock) -> None:
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()
        result = get_currencies(["R01035"])
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

---

## Результаты тестирования

| № | Тест | Класс | Проверка | Результат |
|---|------|-------|----------|-----------|
| 1 | `test_normal_value` | `TestSplitValue` | `'113,2069'` → `('113', '2069')` | ✅ OK |
| 2 | `test_zero_fraction` | `TestSplitValue` | Строка без запятой → `('90', '0')` | ✅ OK |
| 3 | `test_zero_value` | `TestSplitValue` | `'0,0000'` → `('0', '0000')` | ✅ OK |
| 4 | `test_same_instance` | `TestSingletonMeta` | Два вызова конструктора → один объект | ✅ OK |
| 5 | `test_singleton_uses_metaclass` | `TestSingletonMeta` | Используется метакласс `SingletonMeta` | ✅ OK |
| 6 | `test_gbp_name` | `TestValidCurrencies` | Название GBP содержит «Фунт» | ✅ OK |
| 7 | `test_gbp_value_in_range` | `TestValidCurrencies` | Курс GBP в диапазоне 0–999 | ✅ OK |
| 8 | `test_try_name` | `TestValidCurrencies` | Название TRY содержит «лир» | ✅ OK |
| 9 | `test_try_value_in_range` | `TestValidCurrencies` | Курс TRY в диапазоне 0–999 | ✅ OK |
| 10 | `test_invalid_id_returns_none` | `TestInvalidCurrencies` | Несуществующий ID → `{id: None}` | ✅ OK |
| 11 | `test_mixed_ids` | `TestInvalidCurrencies` | Корректный + некорректный ID | ✅ OK |
| 12 | `test_kzt_stores_nominal` | `TestNominal` | KZT (номинал=100) хранит номинал | ✅ OK |
| 13 | `test_cur_lst_getter` | `TestGettersSetters` | `cur_lst` возвращает список | ✅ OK |
| 14 | `test_cur_lst_setter` | `TestGettersSetters` | Установка нового списка | ✅ OK |
| 15 | `test_cur_lst_setter_type_error` | `TestGettersSetters` | Не-список → `TypeError` | ✅ OK |
| 16 | `test_min_interval_setter` | `TestGettersSetters` | Установка нового `min_interval` | ✅ OK |
| 17 | `test_min_interval_negative_raises` | `TestGettersSetters` | Отрицательное значение → `ValueError` | ✅ OK |
| 18 | `test_wrapper_returns_list` | `TestGetCurrenciesWrapper` | `get_currencies()` возвращает список | ✅ OK |

```
Ran 18 tests in 0.010s

OK
```

> Тесты используют `unittest.mock.patch` — реальные HTTP-запросы к ЦБ РФ не выполняются.

---

## Используемые библиотеки

| Библиотека | Назначение |
|---|---|
| `xml.etree.ElementTree` | Парсинг XML-ответа от API ЦБ РФ |
| `requests` | HTTP-запросы к API |
| `matplotlib` | Построение столбчатого графика |
| `time` | Управление интервалами между запросами |
| `unittest.mock` | Mock-объекты для тестирования без сети |

---

## Структура файлов

```
├── currencies.py      # SingletonMeta, CurrenciesLst, get_currencies
└── test_currencies.py # Модульные тесты с mock
```

---

## Вывод

В ходе выполнения работы реализован паттерн «Одиночка» для получения курсов валют ЦБ РФ.

В программе реализованы:

* метакласс `SingletonMeta`, гарантирующий единственность экземпляра через `_instances`;
* класс-одиночка `CurrenciesLst` с ограничением частоты запросов (`min_interval`);
* парсинг XML-ответа от API ЦБ РФ через `ElementTree`;
* поддержка валют с номиналом, отличным от 1 (например, KZT с номиналом 100);
* визуализация курсов через `matplotlib` с сохранением в `.jpg`;
* 18 тестов с `unittest.mock`, покрывающих все компоненты.

---

## 📁 Файлы проекта

| Файл | Описание |
|---|---|
| [currencies.py](lab8/currencies.py) | `SingletonMeta`, `CurrenciesLst`, `get_currencies` |
| [test_currencies.py](lab8/test_currencies.py) | Модульные тесты с mock |
