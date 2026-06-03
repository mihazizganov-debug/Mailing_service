# Mailing Service

Сервис управления рассылками на Django. Позволяет создавать, управлять и отправлять email-рассылки клиентам.

## Функционал

### Основной
- ✅ Управление клиентами (CRUD)
- ✅ Управление сообщениями (CRUD)
- ✅ Управление рассылками (CRUD)
- ✅ Отправка писем по требованию
- ✅ Логирование попыток отправки
- ✅ Статистика на главной странице

### Аутентификация и безопасность
- ✅ Регистрация с подтверждением email
- ✅ Вход / Выход
- ✅ Восстановление пароля
- ✅ Смена пароля
- ✅ Ограничение доступа (только свои объекты)

### Производительность
- ✅ Кеширование страниц (15 минут)
- ✅ Низкоуровневое кеширование списков

## Технологии

- Python 3.13
- Django 6.0.5
- SQLite / PostgreSQL
- Bootstrap 5
- django-allauth
- Redis (опционально)

## Структура проекта
mailing_service/ # Корень проекта
│
├── mailing/                                                   # Основное приложение сервиса рассылок
│ ├── migrations/                                              # Миграции базы данных
│ ├── static/                                                  # Статические файлы
│ │ └── images/                                                # Фоновые изображения
│ │  └── background.jpg                                        # Фоновый рисунок сайта
│ │
│ ├── templates/mailing/                                       # Шаблоны приложения
│ │ ├── base.html                                              # Базовый шаблон (меню, подвал)
│ │ ├── home.html                                              # Главная страница со статистикой
│ │ ├── client_list.html                                       # Список клиентов (таблица)
│ │ ├── client_form.html                                       # Форма создания/редактирования клиента
│ │ ├── client_detail.html                                     # Детальный просмотр клиента
│ │ ├── client_confirm_delete.html                             # Подтверждение удаления клиента
│ │ ├── message_list.html                                      # Список сообщений
│ │ ├── message_form.html                                      # Форма создания/редактирования сообщения
│ │ ├── message_detail.html                                    # Детальный просмотр сообщения
│ │ ├── message_confirm_delete.html                            # Подтверждение удаления сообщения
│ │ ├── mailing_list.html                                      # Список рассылок
│ │ ├── mailing_form.html                                      # Форма создания/редактирования рассылки
│ │ ├── mailing_detail.html                                    # Детальный просмотр рассылки
│ │ └── mailing_confirm_delete.html                            # Подтверждение удаления рассылки
│ ├── admin.py                                                 # Регистрация моделей в админ-панели
│ ├── models.py                                                # Модели: Client, Message, Mailing, Attempt
│ ├── views.py                                                 # Контроллеры (CBV) с кешированием
│ ├── urls.py                                                  # Маршруты приложения (/clients/, /messages/, /mailings/)
│ └── apps.py                                                  # Конфигурация приложения
│
├── users/                                                     # Приложение пользователей и аутентификации
│ ├── migrations/                                              # Миграции пользователей
│ ├── management/                                              # Кастомные команды
│ │ └── commands/                                              # Команды для управления
│ │  └── create_manager_group.py                               # Создание группы "Менеджер"
│ ├── templates/account/                                       # Шаблоны аутентификации (allauth)
│ │ ├── login.html                                             # Страница входа
│ │ ├── signup.html                                            # Страница регистрации
│ │ ├── logout.html                                            # Страница выхода
│ │ ├── password_change.html                                   # Смена пароля
│ │ ├── password_change_done.html                              # Успешная смена пароля
│ │ ├── password_reset.html                                    # Восстановление пароля (запрос email)
│ │ ├── password_reset_done.html                               # Письмо отправлено
│ │ ├── password_reset_from_key.html                           # Форма нового пароля
│ │ ├── password_reset_from_key_done.html                      # Пароль изменён
│ │ ├── email_confirm.html                                     # Подтверждение email
│ │ └── verification_sent.html                                 # Письмо с подтверждением отправлено
│ ├── models.py                                                # Кастомная модель User (email как логин)
│ ├── forms.py                                                 # Формы регистрации и входа
│ ├── views.py                                                 # Контроллеры для allauth
│ ├── urls.py                                                  # Маршруты пользователей (/users/)
│ └── admin.py                                                 # Регистрация модели User в админке
│
├── config/                                                    # Настройки проекта
│ ├── settings.py                                              # Конфигурация Django, allauth, кеширование
│ ├── urls.py                                                  # Главные маршруты (админка, приложения)
│ ├── asgi.py                                                  # ASGI конфигурация
│ └── wsgi.py                                                  # WSGI конфигурация
│
│
├── media/                                                     # Загруженные изображения (аватары)
├── manage.py                                                  # Управляющий скрипт Django
├── requirements.txt                                           # Зависимости проекта
├── .env                                                       # Переменные окружения (не в git)
├── .env.example                                               # Шаблон переменных окружения
├── .gitignore                                                 # Игнорируемые файлы
├── LICENSE                                                    # Лицензия MIT
└── README.md                                                  # Описание проекта


```markdown
## Установка и запуск

### Клонируйте репозиторий

```bash
git clone https://github.com/mihazizganov-debug/Mailing_service
cd Mailing_service

Создайте и активируйте виртуальное окружение
bash
python -m venv venv
venv\Scripts\activate

Установите зависимости
bash
pip install -r requirements.txt

Примените миграции
bash
python manage.py migrate

Создайте суперпользователя
bash
python manage.py createsuperuser

Создайте группу "Менеджер"
bash
python manage.py create_manager_group

Запустите сервер
bash
python manage.py runserver

Открыть в браузере
Главная	http://127.0.0.1:8000/

Админ-панель	http://127.0.0.1:8000/admin/

Регистрация	http://127.0.0.1:8000/accounts/signup/

Вход	http://127.0.0.1:8000/accounts/login/

Клиенты	http://127.0.0.1:8000/clients/

Сообщения	http://127.0.0.1:8000/messages/

Рассылки	http://127.0.0.1:8000/mailings/

Кеширование
Страницы кешируются на 15 минут

Списки клиентов и рассылок кешируются для каждого пользователя

Поддерживается Redis (опционально)

Лицензия
MIT License

Автор
Михаил Зизганов