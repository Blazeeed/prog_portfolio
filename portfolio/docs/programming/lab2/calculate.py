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
