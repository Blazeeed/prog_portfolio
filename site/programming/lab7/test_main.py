"""Тесты для модуля main.py (паттерн «Декоратор», курсы валют ЦБ РФ).

Минимум 2 теста для каждого из трёх компонентов:
    - ConcreteComponent (базовая функциональность)
    - YamlDecorator
    - CsvDecorator
"""

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

# ---------------------------------------------------------------------------
# Тестовые данные, имитирующие ответ API ЦБ РФ
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Тесты ConcreteComponent
# ---------------------------------------------------------------------------


class TestConcreteComponent(unittest.TestCase):
    """Тесты базового компонента, получающего данные из API ЦБ РФ."""

    @patch("main.requests.get")
    def test_operation_returns_dict(self, mock_get: MagicMock) -> None:
        """operation() возвращает словарь."""
        mock_get.return_value.json.return_value = SAMPLE_DATA
        mock_get.return_value.raise_for_status = MagicMock()

        result = ConcreteComponent().operation()

        self.assertIsInstance(result, dict)

    @patch("main.requests.get")
    def test_operation_contains_valute_key(self, mock_get: MagicMock) -> None:
        """Результат operation() содержит ключ 'Valute'."""
        mock_get.return_value.json.return_value = SAMPLE_DATA
        mock_get.return_value.raise_for_status = MagicMock()

        result = ConcreteComponent().operation()

        self.assertIn("Valute", result)


# ---------------------------------------------------------------------------
# Тесты YamlDecorator
# ---------------------------------------------------------------------------


class TestYamlDecorator(unittest.TestCase):
    """Тесты декоратора YamlDecorator."""

    def setUp(self) -> None:
        """Создаёт мок компонента и декоратор перед каждым тестом."""
        mock_component = MagicMock(spec=Component)
        mock_component.operation.return_value = SAMPLE_DATA
        self.decorator = YamlDecorator(mock_component)

    def test_operation_returns_valid_yaml(self) -> None:
        """operation() возвращает валидную YAML-строку."""
        result = self.decorator.operation()

        self.assertIsInstance(result, str)
        parsed = yaml.safe_load(result)
        self.assertIsInstance(parsed, dict)
        self.assertIn("Valute", parsed)

    def test_operation_preserves_currency_values(self) -> None:
        """YAML содержит корректные значения курсов валют."""
        result = self.decorator.operation()
        parsed = yaml.safe_load(result)

        self.assertAlmostEqual(parsed["Valute"]["USD"]["Value"], 90.0)
        self.assertAlmostEqual(parsed["Valute"]["EUR"]["Value"], 98.0)

    def test_save_to_file_creates_valid_yaml_file(self) -> None:
        """save_to_file() создаёт файл с валидным YAML-содержимым."""
        with tempfile.NamedTemporaryFile(
            suffix=".yaml", delete=False, mode="w"
        ) as f:
            tmp_path = f.name
        try:
            self.decorator.save_to_file(tmp_path)

            with open(tmp_path, encoding="utf-8") as f:
                parsed = yaml.safe_load(f)

            self.assertIn("Valute", parsed)
        finally:
            os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Тесты CsvDecorator
# ---------------------------------------------------------------------------


class TestCsvDecorator(unittest.TestCase):
    """Тесты декоратора CsvDecorator."""

    def setUp(self) -> None:
        """Создаёт мок компонента и декоратор перед каждым тестом."""
        mock_component = MagicMock(spec=Component)
        mock_component.operation.return_value = SAMPLE_DATA
        self.decorator = CsvDecorator(mock_component)

    def test_operation_returns_csv_with_correct_header(self) -> None:
        """operation() возвращает CSV с корректным заголовком."""
        result = self.decorator.operation()
        reader = csv.DictReader(io.StringIO(result))

        self.assertEqual(
            reader.fieldnames,
            ["CharCode", "Name", "Nominal", "Value", "Previous"],
        )

    def test_operation_contains_all_currencies(self) -> None:
        """CSV содержит строки для всех валют из тестовых данных."""
        result = self.decorator.operation()
        reader = csv.DictReader(io.StringIO(result))
        codes = [row["CharCode"] for row in reader]

        self.assertIn("USD", codes)
        self.assertIn("EUR", codes)

    def test_save_to_file_creates_valid_csv_file(self) -> None:
        """save_to_file() создаёт файл с валидным CSV-содержимым."""
        with tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False, mode="w"
        ) as f:
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


# ---------------------------------------------------------------------------
# Тесты архитектуры паттерна
# ---------------------------------------------------------------------------


class TestDecoratorPattern(unittest.TestCase):
    """Тесты корректности реализации паттерна «Декоратор»."""

    def test_concrete_component_is_subclass_of_component(self) -> None:
        """ConcreteComponent наследует Component."""
        self.assertTrue(issubclass(ConcreteComponent, Component))

    def test_yaml_decorator_is_subclass_of_decorator(self) -> None:
        """YamlDecorator наследует Decorator."""
        self.assertTrue(issubclass(YamlDecorator, Decorator))

    def test_csv_decorator_is_subclass_of_decorator(self) -> None:
        """CsvDecorator наследует Decorator."""
        self.assertTrue(issubclass(CsvDecorator, Decorator))

    def test_decorator_cannot_be_instantiated(self) -> None:
        """Абстрактный Decorator нельзя создать напрямую."""
        with self.assertRaises(TypeError):
            Decorator(MagicMock())  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main(verbosity=2)
