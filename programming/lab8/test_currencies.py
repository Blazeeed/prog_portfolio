"""Тесты для модуля currencies.py.

Покрывают:
    - паттерн «Одиночка» (SingletonMeta)
    - корректные идентификаторы валют (название, диапазон 0–999)
    - некорректные идентификаторы (возврат {id: None})
    - геттеры/сеттеры
    - rate limiting
    - вспомогательные функции
"""

import unittest
from unittest.mock import MagicMock, patch

from currencies import (
    CurrenciesLst,
    SingletonMeta,
    _split_value,
    get_currencies,
)

# ---------------------------------------------------------------------------
# XML, имитирующий ответ API ЦБ РФ
# ---------------------------------------------------------------------------

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
    """Создаёт мок HTTP-ответа с заданным XML-содержимым."""
    mock = MagicMock()
    mock.content = xml
    mock.raise_for_status = MagicMock()
    return mock


# ---------------------------------------------------------------------------
# Тесты вспомогательной функции _split_value
# ---------------------------------------------------------------------------


class TestSplitValue(unittest.TestCase):
    """Тесты функции разбивки значения курса на части."""

    def test_normal_value(self) -> None:
        """Корректная строка разбивается на две части."""
        self.assertEqual(_split_value("113,2069"), ("113", "2069"))

    def test_zero_fraction(self) -> None:
        """Строка без дробной части получает '0' как дробь."""
        self.assertEqual(_split_value("90"), ("90", "0"))

    def test_zero_value(self) -> None:
        """Нулевое значение разбивается корректно."""
        self.assertEqual(_split_value("0,0000"), ("0", "0000"))


# ---------------------------------------------------------------------------
# Тесты паттерна «Одиночка»
# ---------------------------------------------------------------------------


class TestSingletonMeta(unittest.TestCase):
    """Тесты метакласса SingletonMeta."""

    def test_same_instance(self) -> None:
        """Два вызова конструктора возвращают один и тот же объект."""
        a = CurrenciesLst()
        b = CurrenciesLst()
        self.assertIs(a, b)

    def test_singleton_uses_metaclass(self) -> None:
        """CurrenciesLst является экземпляром метакласса SingletonMeta."""
        self.assertIsInstance(CurrenciesLst, SingletonMeta)


# ---------------------------------------------------------------------------
# Тесты корректных идентификаторов валют
# ---------------------------------------------------------------------------


class TestValidCurrencies(unittest.TestCase):
    """Тесты получения корректных курсов валют."""

    @patch("currencies.requests.get")
    def test_gbp_name(self, mock_get: MagicMock) -> None:
        """Название GBP содержит 'Фунт'."""
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()

        result = CurrenciesLst().fetch(["R01035"])

        gbp_data = result[0].get("GBP")
        self.assertIsNotNone(gbp_data)
        self.assertIn("Фунт", gbp_data[0])

    @patch("currencies.requests.get")
    def test_gbp_value_in_range(self, mock_get: MagicMock) -> None:
        """Курс GBP находится в диапазоне 0–999."""
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()

        result = CurrenciesLst().fetch(["R01035"])

        gbp_data = result[0].get("GBP")
        int_part, frac_part = gbp_data[1]
        value = float(f"{int_part}.{frac_part}")
        self.assertGreater(value, 0)
        self.assertLess(value, 999)

    @patch("currencies.requests.get")
    def test_try_name(self, mock_get: MagicMock) -> None:
        """Название TRY содержит 'лир'."""
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()

        result = CurrenciesLst().fetch(["R01700J"])

        try_data = result[0].get("TRY")
        self.assertIsNotNone(try_data)
        self.assertIn("лир", try_data[0])

    @patch("currencies.requests.get")
    def test_try_value_in_range(self, mock_get: MagicMock) -> None:
        """Курс TRY находится в диапазоне 0–999."""
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()

        result = CurrenciesLst().fetch(["R01700J"])

        try_data = result[0].get("TRY")
        int_part, frac_part = try_data[1]
        value = float(f"{int_part}.{frac_part}")
        self.assertGreater(value, 0)
        self.assertLess(value, 999)


# ---------------------------------------------------------------------------
# Тесты некорректных идентификаторов
# ---------------------------------------------------------------------------


class TestInvalidCurrencies(unittest.TestCase):
    """Тесты поведения при некорректных идентификаторах."""

    @patch("currencies.requests.get")
    def test_invalid_id_returns_none(self, mock_get: MagicMock) -> None:
        """Несуществующий идентификатор возвращает {id: None}."""
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()

        result = CurrenciesLst().fetch(["R9999"])

        self.assertEqual(result, [{"R9999": None}])

    @patch("currencies.requests.get")
    def test_mixed_ids(self, mock_get: MagicMock) -> None:
        """Смесь корректных и некорректных ID: некорректный → None."""
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()

        result = CurrenciesLst().fetch(["R01035", "R9999"])

        codes = {}
        for entry in result:
            codes.update(entry)

        self.assertIn("GBP", codes)
        self.assertIsNotNone(codes["GBP"])
        self.assertIn("R9999", codes)
        self.assertIsNone(codes["R9999"])


# ---------------------------------------------------------------------------
# Тесты номинала
# ---------------------------------------------------------------------------


class TestNominal(unittest.TestCase):
    """Тесты хранения номинала для валют с номиналом != 1."""

    @patch("currencies.requests.get")
    def test_kzt_stores_nominal(self, mock_get: MagicMock) -> None:
        """KZT (номинал 100) сохраняет номинал в кортеже."""
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()

        result = CurrenciesLst().fetch(["R01335"])

        kzt_data = result[0].get("KZT")
        self.assertIsNotNone(kzt_data)
        self.assertEqual(len(kzt_data), 3)
        self.assertEqual(kzt_data[2], "100")


# ---------------------------------------------------------------------------
# Тесты геттеров и сеттеров
# ---------------------------------------------------------------------------


class TestGettersSetters(unittest.TestCase):
    """Тесты свойств класса CurrenciesLst."""

    def setUp(self) -> None:
        SingletonMeta._instances.clear()
        self.cl = CurrenciesLst()

    def test_cur_lst_getter(self) -> None:
        """cur_lst возвращает список."""
        self.assertIsInstance(self.cl.cur_lst, list)

    def test_cur_lst_setter(self) -> None:
        """cur_lst.setter устанавливает переданный список."""
        data = [{"USD": ("Доллар", ("90", "0000"))}]
        self.cl.cur_lst = data
        self.assertEqual(self.cl.cur_lst, data)

    def test_cur_lst_setter_type_error(self) -> None:
        """cur_lst.setter выбрасывает TypeError при неверном типе."""
        with self.assertRaises(TypeError):
            self.cl.cur_lst = "не список"  # type: ignore[assignment]

    def test_min_interval_setter(self) -> None:
        """min_interval.setter принимает корректное значение."""
        self.cl.min_interval = 2.0
        self.assertEqual(self.cl.min_interval, 2.0)

    def test_min_interval_negative_raises(self) -> None:
        """min_interval.setter выбрасывает ValueError при отрицательном значении."""
        with self.assertRaises(ValueError):
            self.cl.min_interval = -1.0


# ---------------------------------------------------------------------------
# Тест функции-обёртки get_currencies
# ---------------------------------------------------------------------------


class TestGetCurrenciesWrapper(unittest.TestCase):
    """Тест совместимости функции get_currencies из шаблона."""

    @patch("currencies.requests.get")
    def test_wrapper_returns_list(self, mock_get: MagicMock) -> None:
        """get_currencies возвращает список."""
        mock_get.return_value = _make_mock_response()
        SingletonMeta._instances.clear()

        result = get_currencies(["R01035"])

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
