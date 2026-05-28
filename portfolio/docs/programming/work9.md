# Создание сайта-портфолио с помощью MkDocs

## Цель работы

Создать статический сайт-портфолио для публикации лабораторных работ по дисциплине «Программирование» с использованием генератора документации **MkDocs** и темы **Material for MkDocs**.

---

## Используемые технологии

| Инструмент | Назначение |
|---|---|
| [MkDocs](https://www.mkdocs.org/) | Генератор статических сайтов из Markdown-файлов |
| [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) | Тема оформления с поддержкой светлой/тёмной темы |
| [GitHub Pages](https://pages.github.com/) | Бесплатный хостинг статических сайтов |
| Markdown | Язык разметки для написания страниц |

---

## 1. Установка зависимостей

Для работы необходим Python 3.8+. Установка производится через `pip`:

```bash
pip install mkdocs-material
```

Эта команда автоматически устанавливает сам MkDocs и тему Material со всеми зависимостями.

Проверка установки:

```bash
mkdocs --version
```

---

## 2. Структура проекта

Итоговая структура папки портфолио:

```
решения/
├── mkdocs.yml                  ← конфигурация сайта
├── requirements.txt            ← зависимости (mkdocs-material)
└── docs/
    ├── index.md                ← главная страница
    ├── about.md                ← страница «Обо мне»
    ├── contacts.md             ← страница «Контакты»
    └── programming/
        ├── work0.md            ← Работа с Git
        ├── work1.md            ← Two Sum
        ├── work2.md            ← Вычисление деления
        ├── work3.md            ← Бинарное дерево
        ├── work5.md            ← Итераторы и генераторы
        ├── work6.md            ← Паттерн «Команда»
        ├── work7.md            ← Паттерн «Декоратор»
        ├── work8.md            ← Паттерн «Одиночка»
        ├── work9.md            ← Портфолио на MkDocs
        ├── lab1/               ← исходный код
        ├── lab2/
        ├── lab3/
        ├── lab5/
        ├── lab7/
        └── lab8/
```

---

## 3. Конфигурационный файл `mkdocs.yml`

Главный файл настройки сайта:

```yaml
site_name: Портфолио по программированию
site_description: Решения лабораторных работ по дисциплине «Программирование»
site_author: Махов Владислав Анатольевич

theme:
  name: material
  language: ru

  palette:
    # Светлая тема
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: Темная тема
    # Тёмная тема
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: Светлая тема

  features:
    - navigation.tabs        # вкладки верхнего уровня
    - navigation.sections    # группировка разделов
    - navigation.expand      # раскрытые секции
    - navigation.top         # кнопка «наверх»
    - search.highlight       # подсветка результатов поиска
    - content.code.copy      # кнопка копирования кода

plugins:
  - search                   # встроенный поиск по сайту

markdown_extensions:
  - admonition               # блоки-предупреждения (note, warning...)
  - tables                   # таблицы
  - toc:
      permalink: true        # якорные ссылки у заголовков
  - pymdownx.highlight       # подсветка синтаксиса
  - pymdownx.superfences     # вложенные блоки кода
  - md_in_html               # Markdown внутри HTML

nav:
  - Главная: index.md
  - Обо мне: about.md
  - Программирование:
      - Общее. Работа с Git: programming/work0.md
      - Тема 1. Two Sum: programming/work1.md
      - Тема 2. Вычисление деления: programming/work2.md
      - Тема 3. Бинарное дерево. Рекурсия: programming/work3.md
      - Тема 5. Итераторы, генераторы, сопрограммы: programming/work5.md
      - Тема 6. Паттерн «Команда»: programming/work6.md
      - Тема 7. Паттерны проектирования (Декоратор): programming/work7.md
      - Тема 8. Паттерн «Одиночка»: programming/work8.md
      - Тема 9. Создание сайта-портфолио: programming/work9.md
  - Контакты: contacts.md
```

---

## 4. Написание страниц (Markdown)

Каждая страница — это обычный `.md` файл. Пример структуры страницы лабораторной работы:

```markdown
# Заголовок работы

## Цель работы
...

## Постановка задачи
...

## Листинг программы

    ```python
    def my_func():
        pass
    ```

## Результаты тестирования

| № | Тест | Результат |
|---|------|-----------|
| 1 | test_example | ✅ OK |

## Вывод
...
```

---

## 5. Локальный запуск

Для предпросмотра сайта в браузере с автоматическим обновлением:

```bash
cd решения
mkdocs serve
```

Сайт будет доступен по адресу: **http://127.0.0.1:8000**

При каждом изменении `.md` файлов или `mkdocs.yml` страница в браузере обновляется автоматически.

---

## 6. Сборка статического сайта

Команда генерирует папку `site/` с готовыми HTML-файлами:

```bash
mkdocs build
```

Содержимое папки `site/` можно разместить на любом веб-хостинге.

---

## 7. Публикация на GitHub Pages

MkDocs умеет публиковать сайт на GitHub Pages одной командой:

```bash
mkdocs gh-deploy
```

Что происходит под капотом:

1. Выполняется `mkdocs build` — генерируются HTML-файлы.
2. Содержимое папки `site/` помещается в ветку `gh-pages` репозитория.
3. GitHub Pages автоматически публикует сайт по адресу:  
   `https://<username>.github.io/<repository>/`

### Шаги для первой публикации

```bash
# 1. Инициализируем репозиторий (если ещё нет)
git init
git remote add origin https://github.com/Blazeeed/portfolio-prog

# 2. Публикуем сайт
mkdocs gh-deploy

# 3. В настройках репозитория на GitHub:
#    Settings → Pages → Source → Branch: gh-pages
```

---

## 8. Основные команды MkDocs

| Команда | Что делает |
|---|---|
| `mkdocs new .` | Создаёт новый проект в текущей папке |
| `mkdocs serve` | Запускает локальный сервер с hot-reload |
| `mkdocs build` | Собирает статический сайт в папку `site/` |
| `mkdocs gh-deploy` | Публикует сайт на GitHub Pages |
| `mkdocs --version` | Показывает версию MkDocs |

---

## Вывод

В ходе работы создан статический сайт-портфолио с использованием **MkDocs** и темы **Material for MkDocs**.

Реализованы:

* конфигурация сайта через `mkdocs.yml` с темой Material, поддержкой светлой/тёмной темы и встроенным поиском;
* структура документации из Markdown-файлов для каждой лабораторной работы;
* навигация по разделам с вкладками и группировкой;
* публикация на GitHub Pages командой `mkdocs gh-deploy`.

MkDocs + Material — удобный инструмент для создания технической документации и учебных портфолио: минимум настройки, красивый результат, полная поддержка Markdown.

---

## 📁 Файлы проекта

| Файл | Описание |
|---|---|
| [mkdocs.yml](../../mkdocs.yml) | Конфигурация сайта |
| [requirements.txt](../../requirements.txt) | Зависимости (`mkdocs-material`) |
