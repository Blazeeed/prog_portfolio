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


# ---------------------------------------------------------------------------
# Абстрактный интерфейс
# ---------------------------------------------------------------------------


class Component(ABC):
    """Базовый абстрактный интерфейс компонента.

    Определяет контракт, которому следуют как конкретный компонент,
    так и все его декораторы.
    """

    @abstractmethod
    def operation(self) -> Any:
        """Выполняет основную операцию компонента.

        Returns:
            Результат в формате, определённом конкретной реализацией.
        """


# ---------------------------------------------------------------------------
# Конкретный компонент — получение курсов валют из API ЦБ РФ
# ---------------------------------------------------------------------------


class ConcreteComponent(Component):
    """Получает актуальные курсы валют из API ЦБ РФ в формате dict.

    Использует публичный API https://www.cbr-xml-daily.ru/daily_json.js,
    который возвращает данные в формате JSON.

    Examples:
        >>> component = ConcreteComponent()
        >>> data = component.operation()
        >>> isinstance(data, dict)
        True
        >>> "Valute" in data
        True
    """

    URL: str = "https://www.cbr-xml-daily.ru/daily_json.js"

    def operation(self) -> dict[str, Any]:
        """Загружает курсы валют из API ЦБ РФ.

        Returns:
            Словарь с данными о курсах валют. Содержит ключ ``'Valute'``
            со словарями для каждой валюты (CharCode, Name, Nominal,
            Value, Previous и др.).

        Raises:
            requests.RequestException: При ошибке сетевого запроса.
        """
        response = requests.get(self.URL, timeout=10)
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# Абстрактный базовый декоратор
# ---------------------------------------------------------------------------


class Decorator(Component, ABC):
    """Абстрактный базовый декоратор.

    Хранит ссылку на обёрнутый компонент и делегирует ему вызовы.
    Обязывает конкретные декораторы реализовать методы ``operation``
    и ``save_to_file``.

    Args:
        component: Компонент или другой декоратор для обёртки.
    """

    def __init__(self, component: Component) -> None:
        """Инициализирует декоратор оборачиваемым компонентом.

        Args:
            component: Компонент или другой декоратор для обёртки.
        """
        self._component = component

    @property
    def component(self) -> Component:
        """Возвращает обёрнутый компонент."""
        return self._component

    def operation(self) -> Any:
        """Делегирует вызов обёрнутому компоненту.

        Returns:
            Результат операции обёрнутого компонента.
        """
        return self._component.operation()

    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        """Сохраняет результат операции в файл соответствующего формата.

        Args:
            filename: Путь к файлу для сохранения.
        """


# ---------------------------------------------------------------------------
# Конкретный декоратор — YAML
# ---------------------------------------------------------------------------


class YamlDecorator(Decorator):
    """Декоратор, преобразующий данные компонента в формат YAML.

    Конвертирует dict, возвращённый обёрнутым компонентом, в YAML-строку.
    Поддерживает сохранение результата в .yaml файл.

    Examples:
        >>> from unittest.mock import MagicMock
        >>> comp = MagicMock()
        >>> comp.operation.return_value = {"Valute": {"USD": {"Value": 90.0}}}
        >>> dec = YamlDecorator(comp)
        >>> isinstance(dec.operation(), str)
        True
        >>> "Valute" in dec.operation()
        True
    """

    def operation(self) -> str:
        """Преобразует данные компонента в строку формата YAML.

        Returns:
            Строка в формате YAML с курсами валют.
        """
        data = self._component.operation()
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)

    def save_to_file(self, filename: str = "rates.yaml") -> None:
        """Сохраняет курсы валют в файл формата YAML.

        Args:
            filename: Путь к файлу. По умолчанию ``'rates.yaml'``.
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.operation())


# ---------------------------------------------------------------------------
# Конкретный декоратор — CSV
# ---------------------------------------------------------------------------


class CsvDecorator(Decorator):
    """Декоратор, преобразующий данные компонента в формат CSV.

    Извлекает валюты из ключа ``'Valute'`` и формирует таблицу CSV,
    где каждая строка соответствует одной валюте.

    Столбцы: CharCode, Name, Nominal, Value, Previous.

    Examples:
        >>> from unittest.mock import MagicMock
        >>> comp = MagicMock()
        >>> comp.operation.return_value = {
        ...     "Valute": {
        ...         "USD": {"CharCode": "USD", "Name": "Доллар",
        ...                 "Nominal": 1, "Value": 90.0, "Previous": 89.0}
        ...     }
        ... }
        >>> dec = CsvDecorator(comp)
        >>> "USD" in dec.operation()
        True
        >>> "CharCode" in dec.operation()
        True
    """

    _FIELDS: list[str] = ["CharCode", "Name", "Nominal", "Value", "Previous"]

    def operation(self) -> str:
        """Преобразует данные компонента в строку формата CSV.

        Returns:
            Строка в формате CSV с заголовком и строками для каждой валюты.
        """
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
        """Сохраняет курсы валют в файл формата CSV.

        Args:
            filename: Путь к файлу. По умолчанию ``'rates.csv'``.
        """
        with open(filename, "w", encoding="utf-8", newline="") as f:
            f.write(self.operation())


# ---------------------------------------------------------------------------
# Клиентский код
# ---------------------------------------------------------------------------


def client_code(component: Component) -> None:
    """Демонстрирует работу с компонентом через общий интерфейс Component.

    Args:
        component: Любой компонент или декоратор, реализующий ``Component``.
    """
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
