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


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------


def _split_value(value_str: str) -> tuple[str, str]:
    """Разбивает строку курса валюты на целую и дробную части.

    ЦБ РФ возвращает числа с запятой в качестве разделителя (например,
    ``'113,2069'``). Функция разделяет строку по запятой.

    Args:
        value_str: Строка значения курса, например ``'113,2069'``.

    Returns:
        Кортеж ``(целая_часть, дробная_часть)``, например ``('113', '2069')``.

    Examples:
        >>> _split_value('113,2069')
        ('113', '2069')
        >>> _split_value('90,0000')
        ('90', '0000')
    """
    parts = value_str.split(",")
    if len(parts) == 2:
        return (parts[0], parts[1])
    return (parts[0], "0")


def _parse_valute(
    node: ET.Element, ids: list[str]
) -> Optional[dict[str, Any]]:
    """Разбирает XML-узел валюты и возвращает словарь или None.

    Args:
        node: XML-элемент ``<Valute>``.
        ids: Список запрошенных идентификаторов.

    Returns:
        Словарь вида ``{CharCode: (Name, (int_part, frac_part))}``
        (с номиналом, если он не равен 1), или ``None``, если ID не
        входит в запрошенный список.
    """
    valute_id = node.get("ID", "")
    if valute_id not in ids:
        return None

    charcode: str = node.find("CharCode").text  # type: ignore[union-attr]
    name: str = node.find("Name").text  # type: ignore[union-attr]
    value_str: str = node.find("Value").text  # type: ignore[union-attr]
    nominal_str: str = node.find("Nominal").text  # type: ignore[union-attr]

    int_part, frac_part = _split_value(value_str)

    if nominal_str != "1":
        return {charcode: (name, (int_part, frac_part), nominal_str)}
    return {charcode: (name, (int_part, frac_part))}


# ---------------------------------------------------------------------------
# Метакласс для паттерна «Одиночка»
# ---------------------------------------------------------------------------


class SingletonMeta(type):
    """Метакласс, реализующий паттерн «Одиночка» (Singleton).

    Гарантирует, что для класса, использующего этот метакласс,
    существует ровно один экземпляр за всё время работы программы.
    Повторные вызовы конструктора возвращают тот же объект.

    Examples:
        >>> class MyClass(metaclass=SingletonMeta):
        ...     pass
        >>> a = MyClass()
        >>> b = MyClass()
        >>> a is b
        True
    """

    _instances: dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Возвращает существующий экземпляр или создаёт новый.

        Args:
            *args: Позиционные аргументы для конструктора класса.
            **kwargs: Именованные аргументы для конструктора класса.

        Returns:
            Единственный экземпляр класса.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# ---------------------------------------------------------------------------
# Основной класс
# ---------------------------------------------------------------------------


class CurrenciesLst(metaclass=SingletonMeta):
    """Класс-одиночка для получения и хранения курсов валют ЦБ РФ.

    Реализует паттерн «Одиночка» через метакласс ``SingletonMeta``.
    Ограничивает частоту запросов к API (не чаще одного раза в секунду
    по умолчанию). Хранит значения курсов в виде кортежей
    ``(целая_часть, дробная_часть)``.

    Args:
        min_interval: Минимальный интервал между запросами (в секундах).
                      По умолчанию ``1.0``.

    Examples:
        >>> a = CurrenciesLst()
        >>> b = CurrenciesLst()
        >>> a is b
        True
    """

    def __init__(self, min_interval: float = 1.0) -> None:
        """Инициализирует хранилище курсов валют.

        Args:
            min_interval: Минимальный интервал между HTTP-запросами
                          к API ЦБ РФ (в секундах).
        """
        self.__cur_lst: list[dict[str, Any]] = []
        self.__min_interval: float = min_interval
        self.__last_request_time: float = 0.0

    def __del__(self) -> None:
        """Деструктор: очищает список курсов при удалении объекта."""
        self.__cur_lst.clear()

    # --- Геттеры и сеттеры ---

    @property
    def cur_lst(self) -> list[dict[str, Any]]:
        """Список загруженных курсов валют."""
        return self.__cur_lst

    @cur_lst.setter
    def cur_lst(self, value: list[dict[str, Any]]) -> None:
        """Устанавливает список курсов валют.

        Args:
            value: Новый список курсов.

        Raises:
            TypeError: Если переданное значение не является списком.
        """
        if not isinstance(value, list):
            raise TypeError("cur_lst должен быть списком")
        self.__cur_lst = value

    @property
    def min_interval(self) -> float:
        """Минимальный интервал между запросами в секундах."""
        return self.__min_interval

    @min_interval.setter
    def min_interval(self, value: float) -> None:
        """Устанавливает минимальный интервал между запросами.

        Args:
            value: Интервал в секундах (должен быть >= 0).

        Raises:
            ValueError: Если значение отрицательное.
        """
        if value < 0:
            raise ValueError("min_interval не может быть отрицательным")
        self.__min_interval = value

    # --- Основные методы ---

    def fetch(self, currencies_ids_lst: list[str]) -> list[dict[str, Any]]:
        """Загружает курсы валют из API ЦБ РФ по списку идентификаторов.

        Соблюдает ограничение частоты запросов (не чаще ``min_interval``
        секунд). Для некорректных идентификаторов добавляет ``{id: None}``.

        Args:
            currencies_ids_lst: Список идентификаторов валют ЦБ РФ,
                                 например ``['R01035', 'R01335']``.

        Returns:
            Список словарей вида::

                [{'GBP': ('Фунт стерлингов...', ('113', '2069'))},
                 {'R9999': None}]

        Raises:
            requests.RequestException: При ошибке сетевого запроса.
        """
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
        """Ждёт, если с последнего запроса прошло меньше ``min_interval`` секунд."""
        elapsed = time.time() - self.__last_request_time
        if elapsed < self.__min_interval:
            time.sleep(self.__min_interval - elapsed)
        self.__last_request_time = time.time()

    def visualize_currencies(self, output_path: str = "currencies.jpg") -> None:
        """Строит столбчатый график курсов валют и сохраняет в файл.

        Использует данные из ``cur_lst``. Валюты с некорректными ID
        (значение ``None``) пропускаются.

        Args:
            output_path: Путь для сохранения графика.
                         По умолчанию ``'currencies.jpg'``.
        """
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


# ---------------------------------------------------------------------------
# Вспомогательная функция из шаблона (совместимость)
# ---------------------------------------------------------------------------


def get_currencies(currencies_ids_lst: list[str]) -> list[dict[str, Any]]:
    """Получает курсы валют из API ЦБ РФ (функциональный интерфейс).

    Обёртка над ``CurrenciesLst.fetch`` для обратной совместимости
    с кодом из шаблона лабораторной работы.

    Args:
        currencies_ids_lst: Список идентификаторов валют ЦБ РФ.

    Returns:
        Список словарей с курсами валют или ``{id: None}`` для
        некорректных идентификаторов.
    """
    return CurrenciesLst().fetch(currencies_ids_lst)


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # GBP, KZT, TRY — идентификаторы из шаблона
    ids = ["R01035", "R01335", "R01700J"]

    print("Загрузка курсов валют...")
    cl = CurrenciesLst(min_interval=1.0)
    result = cl.fetch(ids)

    print("\nРезультат:")
    for entry in result:
        print(entry)

    print("\nПроверка Singleton:")
    cl2 = CurrenciesLst()
    print(f"cl is cl2: {cl is cl2}")

    print("\nПостроение графика...")
    cl.visualize_currencies("currencies.jpg")
