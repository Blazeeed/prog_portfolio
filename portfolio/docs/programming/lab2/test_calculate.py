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
        config_file.write_text("[DEFAULT]\nepsilon = 0.5\n", encoding="utf-8")  # > 10**-1
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
