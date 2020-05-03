# PyMessages

Проект WebServer + API, выполненный в рамках программы образовательного проекта 
"Яндекс.Лицей"

## Описание проекта

Проект представляет собой мессенджер с типичными для него возможностями:
- [X] Создавать аккаунт
- [X] Настраивать профиль
- [X] Добавлять пользователей в друзья, удалять их из друзей
- [ ] Отправлять и просматривать сообщения

Проект выполнен с использованием языка Python (и не только)

## Установка и запуск

Чтобы запустить приложение:
* Установите Python версии 3.8 и выше (https://www.python.org/downloads/);
* Установите все зависимости из requirements.txt. Лучше всего это делать в 
виртуальном окружении. Для создания виртуального окружения выполните в 
терминале или в командной строке команду `python -m venv venv && 
venv\Scripts\activate` (чтобы выйти из виртуального окружения после того, как 
закончите работать с приложением, выполните команду `venv\Scripts\deactivate`). 
Чтобы установить все зависимости, выполните команду 
`pip install -r requirements.txt`;
* Чтобы в приложении работала рассылка email (необходимая для регитсрации 
пользователей) откройте файл app/config.py и внесите данные SMTP сервера, 
который вы будете использовать ([бесплатные SMTP сервера](#полезные-ссылки));
* Запустите файл \_\_main\_\_.py либо выполните команду `python __main__.py` в 
терминале или в командной строке.

*Все команды в терминале или в командной строке нужно выполнять из директории, 
в которую вы поместили файлы репозитория*

Готово! Теперь приложение запущено по адресу https://localhost:5000. Приложение 
запущено в вашей локальной сети. Если вы хотите, чтобы к приложению можно было 
получить доступ через Интернет, вы можете воспользоваться, к примеру, сервисом 
[ngrok](https://ngrok.com/).

## Сборка

Проект готов к запуску "из коробки", но если вам вдруг необходимо изменить 
какие либо стиле на странице, придёться пересобирать проект вручную (так как 
они заданы в файле SASS по пути app/sass/style.scss). Для этого:

* Установите SASS ([руководство по установке](#полезные-ссылки));
* Скачайте и распакуйте в папку app содержимое исходников Bootstrap 
([скачать исходники](#полезные-ссылки)). Распакованную папку переименуйте в 
"bootstrap";
* Выполните в терминале команду `sass app/sass:app/static/css` для компиляции 
SASS файлов.

Готово! Стили скомпилированы.

## Конфигурация приложения

Конфигурация приложения происходит в зависимости от значения переменной среды 
APP_CONFIG. Если значением является путь к файлу, то конфигурация происходит 
через этот файл ([подробнее в документации Flask](
https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-files)). 

Иначе значение переменной расценивается как название Python класс и 
конфигурация происходит через данный класс ([подробнее в документации Flask](
https://flask.palletsprojects.com/en/1.1.x/config/#development-production)).

Все конфиги должны содержаться в файле app/config.py.

По умолчанию APP_CONFIG = app.config.DevelopmentConfig.

Чтобы сконфигурировать приложение через переменные среды, установите
значение APP_CONFIG = app.config.EnvConfig, в переменную среды APP_ENV_VARS
внесите через запятую названия всех значений конфигурации, которые вы хотите
установить через переменные среды, и соотвествующим переменным среды
присвойте нужные значения (учитите, что эти значения вычисляются как Python
выражения с помощью функции eval()). Например выполнив данные команды в 
командной строке Windows:

```cmd
set APP_CONFIG = app.config.EnvConfig
set APP_ENV_VARS = SECRET_KEY, DEBUG
set SECRET_KEY = 'SUPER_SECRET_KEY'
set DEBUG = True
```

Мы установим значениям конфигурации приложения SECRET_KEY и DEBUG значения 
`'SUPER_SECRET_KEY'` и `True` соответственно.

## Полезные ссылки

* Бесплатные SMTP сервера можно найти тут:  
https://bimailer.ru/help/smtp-list.php.  
К примеру, такие услуги предоставляет Google и Яндекс;
* [ngrok](https://ngrok.com/) - организация виртуального туннеля из Интернета 
на ваш локальный компьютер.
* [Установка SASS](https://sass-scss.ru/install/)
* [Исходники Bootstrap](
https://bootstrap-4.ru/docs/4.4/getting-started/download/)
