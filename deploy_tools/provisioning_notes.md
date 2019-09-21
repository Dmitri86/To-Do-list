Обеспечение работы нового сайта
===============================
## Необходимые пакеты:
* nginx
* Python 3.6
* virtualenv + pip
* Git

например, в Ubuntu:
	sudo add-apt-repository ppa:fkrull/deadsnakes
	sudo apt-get install nginx git python36 python3..6-venv

## Конфигурация виртуального узла Nginx
* см. nginx.template.conf
* заменить SITENAME, например, на my.test-to-do.tk

## Служба Systemd

* см. gunicrorn-systemd.template.service
* заменить SITENAME, например, на my.test-to-do.tk 

## Структура папок:
Если допустить, что есть учетная запись в /home/username

/home/username
└── sites
    ├── SITENAME
        ├── database
        ├── source
        ├── static
        ├── virtualenv


