# QAFlow

Тестовый фреймворк для web-приложения. Покрывает API, UI, E2E и мобильную эмуляцию.

Запускается локально через Makefile или удалённо через GitHub Actions — в том числе из Telegram-бота.

---

## Как это работает

```
workflow_dispatch (all / ui / api / e2e / mobile)
         |
    api_tests
         |
    ui_tests ──── mobile_tests
         |
    e2e_tests
         |
    allure_report → GitHub Pages
```

Каждый job независим. Если API упали — UI и E2E всё равно запустятся (`if: always()`).
Allure собирает результаты всех jobs и публикует единый отчёт.

---

## Структура

```
tests/
├── desktop/
│   ├── api/            # HTTP тесты через requests
│   │   ├── test_users.py
│   │   └── test_create.py
│   ├── ui/             # браузерные тесты через Playwright
│   │   ├── pages/      # Page Object Model
│   │   ├── test_login.py
│   │   └── test_basic_ui.py
│   └── e2e/            # сквозные сценарии
│       ├── pages/
│       └── test_flow.py
└── mobile/             # эмуляция Pixel 5 + iPhone 13
    ├── pages/
    ├── test_mobile_login.py
    ├── test_mobile_navigation.py
    └── test_mobile_ui.py
```

---

## Что тестируется

### API (`tests/desktop/api`)
Сайт: jsonplaceholder.typicode.com

- GET /users — статус 200, структура ответа, количество записей
- GET /users/{id} — валидация полей (id, email, name)
- GET /users/999 — 404 на несуществующий ресурс
- POST /posts — создание, проверка id и createdAt в ответе
- PUT /posts/1 — обновление, проверка изменённых полей
- DELETE /posts/1 — статус 200, пустое тело
- GET /posts?userId=1 — фильтрация, все записи принадлежат userId=1

Покрыты: positive, negative, фильтрация, граничные id.

---

### UI (`tests/desktop/ui`)
Сайт: saucedemo.com, the-internet.herokuapp.com

- логин с валидными credentials → редирект на /inventory
- логин с неверным паролем → сообщение об ошибке
- логин заблокированного пользователя → специфичная ошибка
- пустые поля → валидация формы
- checkbox: переключение состояния
- dropdown: выбор опций
- динамические элементы: добавление и удаление

Покрыты: positive, negative, граничные состояния UI.

---

### E2E (`tests/desktop/e2e`)
Сайт: saucedemo.com, httpbin.org

- полный flow: логин → добавить товар → корзина → checkout → подтверждение
- негативный login flow: несколько невалидных попыток подряд
- API консистентность: структура и поля всех пользователей
- httpbin delay: ответ приходит в пределах таймаута

---

### Mobile (`tests/mobile`)
Устройства: Pixel 5 (393px), iPhone 13 (390px)

Каждый тест прогоняется на обоих устройствах автоматически через `pytest_generate_tests`.

- логин: success, wrong password, пустые поля, locked user
- навигация: бургер-меню, переход в корзину, сортировка товаров
- адаптивный UI: ширина viewport, видимость элементов, title страницы

---

## Запуск

```bash
pip install -r requirements.txt
playwright install chromium

make test-api        # API
make test-ui         # UI
make test-e2e        # E2E
make test-mobile     # Mobile (Pixel 5 + iPhone 13)
make test-all        # всё сразу

make report          # открыть Allure в браузере
make clean           # удалить артефакты
```

---

## Design decisions

**Page Object Model везде** — локаторы и действия живут в page-классах. Тесты только вызывают методы. При смене селектора правишь одно место.

**Разделение desktop / mobile** — разные контексты браузера, разные фикстуры, разные конфигурации viewport. Смешивать не стоит.

**`pytest_generate_tests` для устройств** — не нужно дублировать `@pytest.mark.parametrize` в каждом тесте. Устройства подключаются на уровне conftest.

**`if: always()` в CI** — если API упали, UI и E2E всё равно запустятся. Полная картина за один прогон, а не остановка на первой ошибке.

**Скриншот при падении** — через `pytest_runtest_makereport` hook. Автоматически, без изменений в тестах. Для мобильных — имя файла содержит название устройства.

**Нет time.sleep** — везде `expect()` с встроенным retry от Playwright.

---

## Ограничения

- тестируются публичные демо-сайты, не реальный продукт
- нет параллельного запуска (pytest-xdist не подключён)
- мобильная эмуляция через Chromium — не реальный Safari на iPhone
- нет хранения истории прогонов, только последний Allure отчёт

---

## Пример отчета

Allure overview после прогона тестов:
<img width="1258" height="678" alt="Снимок экрана — 2026-04-18 в 21 49 36" src="https://github.com/user-attachments/assets/9bd39859-8970-45cc-b745-1b64893cee88" />

