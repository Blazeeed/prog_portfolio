# Паттерн «Декоратор» для работы с курсами валют ЦБ РФ

## Цель работы

Изучить применение шаблона проектирования «Декоратор» на языке Python.

В рамках работы необходимо:

* реализовать базовый компонент для получения курсов валют через API Центробанка РФ;
* реализовать декораторы для преобразования данных в YAML и CSV форматы;
* использовать абстрактные классы и интерфейсы (`ABC`, `@abstractmethod`);
* реализовать сохранение данных в файлы;
* разработать тесты с использованием `unittest.mock`.

---

## Постановка задачи

На основе шаблона «Декоратор» реализовать:

1. Базовый компонент `ConcreteComponent`, который:
   * получает данные о курсах валют через API ЦБ РФ;
   * возвращает данные в формате словаря (`dict`).

2. Конкретные декораторы:
   * `YamlDecorator` — конвертирует словарь в YAML и сохраняет в файл;
   * `CsvDecorator` — конвертирует данные блока `Valute` в CSV и сохраняет в файл.

Каждый декоратор должен:

* переопределять метод `operation()`;
* реализовывать метод `save_to_file(filename)`.

Источник данных:

```text
https://www.cbr-xml-daily.ru/daily_json.js
```

---

## Теоретические сведения

### Паттерн «Декоратор»

Паттерн «Декоратор» позволяет динамически расширять функциональность объектов без изменения их исходного кода. Вместо наследования используется обёртка (wrapper), которая хранит ссылку на исходный компонент и добавляет новое поведение.

| Элемент | Класс | Назначение |
|---|---|---|
| Component | `Component` (ABC) | Абстрактный интерфейс |
| ConcreteComponent | `ConcreteComponent` | Получает JSON с API ЦБ РФ |
| Decorator | `Decorator` (ABC) | Базовый декоратор — делегирует вызов |
| ConcreteDecorator | `YamlDecorator` | Конвертирует dict → YAML |
| ConcreteDecorator | `CsvDecorator` | Конвертирует dict → CSV |

### Иерархия классов

```
Component (ABC)
    └── operation() → Any

ConcreteComponent → Component
    └── operation() → dict  (запрос к API ЦБ РФ)

Decorator (ABC) → Component
    ├── _component: Component
    ├── operation() → делегирует _component
    └── save_to_file(filename) — абстрактный

YamlDecorator → Decorator
    ├── operation() → str  (YAML)
    └── save_to_file(filename)

CsvDecorator → Decorator
    ├── operation() → str  (CSV)
    └── save_to_file(filename)
```

---

## Листинг программы

### Файл `main.py`

```python
"""
Паттерн «Декоратор» для получения и конвертации курсов валют ЦБ РФ.

Структура:
    Component          — абстрактный интерфейс (ABC)
    ConcreteComponent  — получает курсы валют из API ЦБ РФ в формате dict
    Decorator          — абстрактный базовый декоратор
    YamlDecorator      — конвертирует результат в YAML, сохраняет в .yaml файл
    CsvDecorator       — конвертирует результат в CSV, сохраняет в .csv файл

API ЦБ РФ: https://www.cbr-xml-daily.ru/daily_json.js
"""

from __future__ import annotations

import csv
import io
from abc import ABC, abstractmethod
from typing import Any

import requests
import yaml


class Component(ABC):
    @abstractmethod
    def operation(self) -> Any:
        """Выполняет основную операцию компонента."""


class ConcreteComponent(Component):
    URL: str = "https://www.cbr-xml-daily.ru/daily_json.js"

    def operation(self) -> dict[str, Any]:
        response = requests.get(self.URL, timeout=10)
        response.raise_for_status()
        return response.json()


class Decorator(Component, ABC):
    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        return self._component

    def operation(self) -> Any:
        return self._component.operation()

    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        """Сохраняет результат операции в файл."""


class YamlDecorator(Decorator):
    def operation(self) -> str:
        data = self._component.operation()
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)

    def save_to_file(self, filename: str = "rates.yaml") -> None:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.operation())


class CsvDecorator(Decorator):
    _FIELDS: list[str] = ["CharCode", "Name", "Nominal", "Value", "Previous"]

    def operation(self) -> str:
        data = self._component.operation()
        valute: dict[str, Any] = data.get("Valute", {})

        output = io.StringIO()
        writer = csv.DictWriter(
            output, fieldnames=self._FIELDS, extrasaction="ignore"
        )
        writer.writeheader()
        for currency in valute.values():
            writer.writerow(currency)

        return output.getvalue()

    def save_to_file(self, filename: str = "rates.csv") -> None:
        with open(filename, "w", encoding="utf-8", newline="") as f:
            f.write(self.operation())


def client_code(component: Component) -> None:
    result = component.operation()
    print(f"Type: {type(result).__name__}")
    output = str(result) if not isinstance(result, str) else result
    print(output[:400])


if __name__ == "__main__":
    base = ConcreteComponent()

    print("=== JSON (ConcreteComponent) ===")
    client_code(base)

    print("\n=== YAML (YamlDecorator) ===")
    yaml_dec = YamlDecorator(base)
    client_code(yaml_dec)
    yaml_dec.save_to_file("rates.yaml")
    print("Saved -> rates.yaml")

    print("\n=== CSV (CsvDecorator) ===")
    csv_dec = CsvDecorator(base)
    client_code(csv_dec)
    csv_dec.save_to_file("rates.csv")
    print("Saved -> rates.csv")
```

---

### Файл `test_main.py`

```python
"""Тесты для модуля main.py (паттерн «Декоратор», курсы валют ЦБ РФ)."""

import csv
import io
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import yaml

from main import (
    Component,
    ConcreteComponent,
    CsvDecorator,
    Decorator,
    YamlDecorator,
)

SAMPLE_DATA: dict = {
    "Date": "2024-01-15T11:30:00+03:00",
    "Valute": {
        "USD": {
            "ID": "R01235",
            "NumCode": "840",
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 90.0,
            "Previous": 89.5,
        },
        "EUR": {
            "ID": "R01239",
            "NumCode": "978",
            "CharCode": "EUR",
            "Nominal": 1,
            "Name": "Евро",
            "Value": 98.0,
            "Previous": 97.5,
        },
    },
}


class TestConcreteComponent(unittest.TestCase):

    @patch("main.requests.get")
    def test_operation_returns_dict(self, mock_get: MagicMock) -> None:
        mock_get.return_value.json.return_value = SAMPLE_DATA
        mock_get.return_value.raise_for_status = MagicMock()
        result = ConcreteComponent().operation()
        self.assertIsInstance(result, dict)

    @patch("main.requests.get")
    def test_operation_contains_valute_key(self, mock_get: MagicMock) -> None:
        mock_get.return_value.json.return_value = SAMPLE_DATA
        mock_get.return_value.raise_for_status = MagicMock()
        result = ConcreteComponent().operation()
        self.assertIn("Valute", result)


class TestYamlDecorator(unittest.TestCase):

    def setUp(self) -> None:
        mock_component = MagicMock(spec=Component)
        mock_component.operation.return_value = SAMPLE_DATA
        self.decorator = YamlDecorator(mock_component)

    def test_operation_returns_valid_yaml(self) -> None:
        result = self.decorator.operation()
        self.assertIsInstance(result, str)
        parsed = yaml.safe_load(result)
        self.assertIsInstance(parsed, dict)
        self.assertIn("Valute", parsed)

    def test_operation_preserves_currency_values(self) -> None:
        result = self.decorator.operation()
        parsed = yaml.safe_load(result)
        self.assertAlmostEqual(parsed["Valute"]["USD"]["Value"], 90.0)
        self.assertAlmostEqual(parsed["Valute"]["EUR"]["Value"], 98.0)

    def test_save_to_file_creates_valid_yaml_file(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
            tmp_path = f.name
        try:
            self.decorator.save_to_file(tmp_path)
            with open(tmp_path, encoding="utf-8") as f:
                parsed = yaml.safe_load(f)
            self.assertIn("Valute", parsed)
        finally:
            os.unlink(tmp_path)


class TestCsvDecorator(unittest.TestCase):

    def setUp(self) -> None:
        mock_component = MagicMock(spec=Component)
        mock_component.operation.return_value = SAMPLE_DATA
        self.decorator = CsvDecorator(mock_component)

    def test_operation_returns_csv_with_correct_header(self) -> None:
        result = self.decorator.operation()
        reader = csv.DictReader(io.StringIO(result))
        self.assertEqual(
            reader.fieldnames,
            ["CharCode", "Name", "Nominal", "Value", "Previous"],
        )

    def test_operation_contains_all_currencies(self) -> None:
        result = self.decorator.operation()
        reader = csv.DictReader(io.StringIO(result))
        codes = [row["CharCode"] for row in reader]
        self.assertIn("USD", codes)
        self.assertIn("EUR", codes)

    def test_save_to_file_creates_valid_csv_file(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            tmp_path = f.name
        try:
            self.decorator.save_to_file(tmp_path)
            with open(tmp_path, encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertGreater(len(rows), 0)
            self.assertIn("CharCode", rows[0])
        finally:
            os.unlink(tmp_path)


class TestDecoratorPattern(unittest.TestCase):

    def test_concrete_component_is_subclass_of_component(self) -> None:
        self.assertTrue(issubclass(ConcreteComponent, Component))

    def test_yaml_decorator_is_subclass_of_decorator(self) -> None:
        self.assertTrue(issubclass(YamlDecorator, Decorator))

    def test_csv_decorator_is_subclass_of_decorator(self) -> None:
        self.assertTrue(issubclass(CsvDecorator, Decorator))

    def test_decorator_cannot_be_instantiated(self) -> None:
        with self.assertRaises(TypeError):
            Decorator(MagicMock())


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

---

## Результаты тестирования

| № | Тест | Класс | Проверка | Результат |
|---|------|-------|----------|-----------|
| 1 | `test_operation_returns_dict` | `TestConcreteComponent` | `operation()` возвращает `dict` | ✅ OK |
| 2 | `test_operation_contains_valute_key` | `TestConcreteComponent` | Результат содержит ключ `'Valute'` | ✅ OK |
| 3 | `test_operation_returns_valid_yaml` | `TestYamlDecorator` | `operation()` возвращает валидный YAML | ✅ OK |
| 4 | `test_operation_preserves_currency_values` | `TestYamlDecorator` | YAML содержит верные курсы валют | ✅ OK |
| 5 | `test_save_to_file_creates_valid_yaml_file` | `TestYamlDecorator` | Файл YAML создаётся с корректным содержимым | ✅ OK |
| 6 | `test_operation_returns_csv_with_correct_header` | `TestCsvDecorator` | CSV содержит правильный заголовок | ✅ OK |
| 7 | `test_operation_contains_all_currencies` | `TestCsvDecorator` | CSV содержит строки для USD и EUR | ✅ OK |
| 8 | `test_save_to_file_creates_valid_csv_file` | `TestCsvDecorator` | Файл CSV создаётся с корректным содержимым | ✅ OK |
| 9 | `test_concrete_component_is_subclass_of_component` | `TestDecoratorPattern` | `ConcreteComponent` наследует `Component` | ✅ OK |
| 10 | `test_yaml_decorator_is_subclass_of_decorator` | `TestDecoratorPattern` | `YamlDecorator` наследует `Decorator` | ✅ OK |
| 11 | `test_csv_decorator_is_subclass_of_decorator` | `TestDecoratorPattern` | `CsvDecorator` наследует `Decorator` | ✅ OK |
| 12 | `test_decorator_cannot_be_instantiated` | `TestDecoratorPattern` | `Decorator` нельзя создать напрямую | ✅ OK |

```
Ran 12 tests in 0.003s

OK
```

> Тесты используют `unittest.mock.patch` и `MagicMock` — реальные HTTP-запросы не выполняются.

---

## Используемые библиотеки

| Библиотека | Назначение |
|---|---|
| `abc` | Абстрактные классы и методы |
| `requests` | HTTP-запросы к API ЦБ РФ |
| `yaml` | Сериализация в формат YAML |
| `csv` | Формирование CSV через `DictWriter` |
| `io` | Строковый буфер для CSV |
| `unittest.mock` | Mock-объекты для тестирования без сети |

---

## Структура файлов

```
├── main.py          # Component, ConcreteComponent, декораторы
└── test_main.py     # Модульные тесты с mock
```

---

## Вывод

В ходе выполнения работы реализован паттерн «Декоратор» для обработки курсов валют ЦБ РФ.

Реализованы:

* абстрактный интерфейс `Component` через `ABC` и `@abstractmethod`;
* базовый компонент `ConcreteComponent`, получающий курсы в формате JSON через `requests`;
* абстрактный декоратор `Decorator` с делегированием вызовов компоненту;
* `YamlDecorator` — конвертирует данные в YAML и сохраняет в файл;
* `CsvDecorator` — конвертирует блок `Valute` в CSV через `csv.DictWriter`;
* 12 тестов с `unittest.mock` — без реальных HTTP-запросов.

---

## 📁 Файлы проекта

| Файл | Описание |
|---|---|
| [main.py](lab7/main.py) | Component, ConcreteComponent и декораторы |
| [test_main.py](lab7/test_main.py) | Модульные тесты с mock |
