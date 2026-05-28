# Паттерн «Команда» (Command) в Python

## 1. Что такое Command-паттерн?

Паттерн Command («Команда») — это способ превратить запрос или действие в полноценный объект. Вместо того чтобы напрямую вызывать метод, вы создаёте объект-команду, который хранит в себе все детали: какой метод вызвать, с какими параметрами, и даже как отменить это действие.

**Главная идея:** Отделить «кто просит» (отправитель) от «кто исполняет» (получатель), упаковав действие в объект.

**Где пригодится:**

- Кнопки в GUI (каждая кнопка — это команда)
- Очереди задач и планировщики
- Макросы и запись действий пользователя
- **Undo/Redo** (здесь Command бывает удобнее Memento)
- Транзакции в базах данных

---

## 2. Аналогия

Представьте себе ресторан.

**Клиент** хочет заказать пасту. Он не идёт на кухню и не говорит повару «свари мне пасту». Вместо этого клиент говорит **официанту** (отправитель) свой заказ.

Официант записывает заказ на **бумажку** — это и есть команда. На бумажке написано: «Паста карбонара, стол №3». Официант не знает, как варить пасту — его дело передать бумажку.

Официант может положить бумажку в **стек заказов** (очередь), а может сразу отнести её на кухню. На кухне **повар** (получатель) умеет читать бумажку и готовить именно то блюдо, которое написано.

**Отмены:** Если клиент передумал, официант может выбросить бумажку из очереди — команда не выполнится. А если паста уже готова? Тогда нужна «команда отмены» — например, выкинуть блюдо и списать ингредиенты.

| В ресторане | В паттерне |
|---|---|
| Клиент | Клиентский код |
| Официант | Invoker (вызыватель) |
| Бумажка с заказом | Command |
| Повар | Receiver (получатель) |

---

## 3. Три главных «героя» паттерна

| Роль | Обязанность | Пример в Python |
|---|---|---|
| **Command** | Интерфейс с методом `execute()` (и иногда `undo()`). Хранит ссылку на получателя и параметры. | Абстрактный класс с методом `execute()` |
| **Receiver** | Тот, кто реально выполняет работу. Знает, **как** делать действие. | Класс `Light`, `Stereo` |
| **Invoker** | Решает, **когда** выполнить команду. Не знает, что именно делает команда. | Кнопка в UI, горячая клавиша, планировщик |

---

## 4. Пример «Выключатель»

### 4.1 Без паттерна Command

```python
class Light:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        print("Свет включён")

    def turn_off(self):
        self.is_on = False
        print("Свет выключен")

class RemoteControl:
    def __init__(self, light):
        self.light = light

    def press_button1(self):
        self.light.turn_on()

    def press_button2(self):
        self.light.turn_off()

# Проблема: каждая новая кнопка — новый метод.
# Нельзя отменить действие, нельзя записать последовательность.
```

### 4.2 С паттерном Command

```python
from abc import ABC, abstractmethod
from typing import List


# 1. Command — интерфейс всех команд
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# 2. Receiver — кто умеет делать реальную работу
class Light:
    def __init__(self, location: str = "комната"):
        self.location = location
        self._is_on = False

    def turn_on(self):
        self._is_on = True
        print(f"  {self.location}: свет включён")

    def turn_off(self):
        self._is_on = False
        print(f"  {self.location}: свет выключен")


class Stereo:
    def __init__(self, location: str = "гостиная"):
        self.location = location
        self._volume = 10

    def on(self):
        print(f"  {self.location}: музыка включена")

    def off(self):
        print(f"  {self.location}: музыка выключена")

    def set_volume(self, volume: int):
        self._volume = volume
        print(f"  {self.location}: громкость = {volume}")


# 3. Конкретные команды
class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_off()

    def undo(self):
        self.light.turn_on()


class StereoOnWithVolumeCommand(Command):
    def __init__(self, stereo: Stereo, volume: int):
        self.stereo = stereo
        self.volume = volume
        self._previous_volume = None

    def execute(self):
        self._previous_volume = self.stereo._volume
        self.stereo.on()
        self.stereo.set_volume(self.volume)

    def undo(self):
        self.stereo.off()
        if self._previous_volume is not None:
            self.stereo.set_volume(self._previous_volume)


class NoCommand(Command):
    """Пустая команда для незанятых слотов."""
    def execute(self):
        pass
    def undo(self):
        pass


# 4. Invoker — пульт с поддержкой отмены
class RemoteControl:
    def __init__(self, slots: int = 7):
        self._commands = [NoCommand() for _ in range(slots)]
        self._undo_command = NoCommand()

    def set_command(self, slot: int, command: Command):
        self._commands[slot] = command

    def press_button(self, slot: int):
        print(f"\n  Нажата кнопка {slot}")
        self._commands[slot].execute()
        self._undo_command = self._commands[slot]

    def press_undo(self):
        print("\n  Отмена последнего действия")
        self._undo_command.undo()


# Использование
if __name__ == "__main__":
    living_room_light = Light("гостиная")
    kitchen_light     = Light("кухня")
    stereo            = Stereo("гостиная")

    living_light_on  = LightOnCommand(living_room_light)
    living_light_off = LightOffCommand(living_room_light)
    kitchen_light_on = LightOnCommand(kitchen_light)
    stereo_on        = StereoOnWithVolumeCommand(stereo, 15)

    remote = RemoteControl()
    remote.set_command(0, living_light_on)
    remote.set_command(1, living_light_off)
    remote.set_command(2, kitchen_light_on)
    remote.set_command(4, stereo_on)

    remote.press_button(0)   # свет в гостиной включился
    remote.press_button(2)   # свет на кухне включился
    remote.press_button(4)   # музыка включилась

    remote.press_undo()      # отмена: музыка выключилась
    remote.press_button(1)   # свет в гостиной выключился
    remote.press_undo()      # отмена: свет в гостиной включился обратно
```

---

## 5. Макросы — несколько команд за раз

Особая сила Command — объединять команды в макросы:

```python
class MacroCommand(Command):
    def __init__(self, commands: List[Command]):
        self.commands = commands

    def execute(self):
        for command in self.commands:
            command.execute()

    def undo(self):
        # Отменяем в обратном порядке
        for command in reversed(self.commands):
            command.undo()


# Макрос «Вечеринка»
party_macro = MacroCommand([
    LightOnCommand(living_room_light),
    StereoOnWithVolumeCommand(stereo, 20),
])

remote.set_command(6, party_macro)
remote.press_button(6)   # Одна кнопка — целый сценарий!
remote.press_undo()      # Отмена всего сценария в обратном порядке
```

---

## 6. Command vs Memento: что выбрать для Undo?

Оба паттерна умеют отменять действия, но по-разному:

| Критерий | **Memento (Хранитель)** | **Command (Команда)** |
|---|---|---|
| Что сохраняется | Всё состояние объекта | Только одно действие |
| Память | Много (полный снимок) | Мало (разница + параметры) |
| Сложность | Просто сохранить, сложно с большими объектами | Нужно писать `undo()` для каждой команды |
| Для чего лучше | Простые объекты, «сохранение игры» | GUI, текстовые редакторы, транзакции |

**Итого:**

- **Memento** → когда объект простой, а цепочка изменений длинная (сохранения в играх)
- **Command** → когда действий много, объект сложный, и каждое изменение нужно отменять (текстовый редактор)

---

## 7. Когда использовать Command

**Хорошо подходит:**

- GUI с кнопками, пунктами меню, горячими клавишами
- Нужна очередь задач (например, пул потоков)
- Макросы и запись последовательности действий
- Поддержка Undo/Redo в редакторах
- Транзакции (всё или ничего)

**Не стоит использовать:**

- Всего 1-2 действия, которые никогда не изменятся
- Когда не нужна отмена
- Простая программа без UI

---

## 8. Итог

Паттерн Command — это превращение действия в объект:

| Элемент | Роль |
|---|---|
| **Command** | Интерфейс с `execute()` и `undo()` |
| **Receiver** | Кто реально выполняет работу |
| **Invoker** | Кто решает, когда выполнять |

**Преимущества:**

* Отделяем «что сделать» от «кто делает»
* Легко добавлять новые команды без изменения существующих
* Undo/Redo из коробки
* Макросы и очереди задач

В Python команды часто делают через замыкания или декораторы, но классический классовый подход даёт больше контроля и поддержку `undo`.

> Когда вы нажимаете Ctrl+Z в текстовом редакторе, там живёт стек команд с `undo()`, а не снимки всего документа.

---

## 📁 Источник

Материал подготовлен на основе конспекта: [Command.md](https://gist.github.com/Blazeeed/dfd12e5a2f9a7bb8dd03257d9d28e5c2)
