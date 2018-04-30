# Quick start guide
1. Create the .env configuration file in `/src/rrsm/.env`. Example test server configuration:
    ```
    SECRET_KEY='#ps1ib&=v%zsgzi5q*qp-ei*b1bg19dxv&861m@4@x+2ww6nx^'
    DEBUG=True
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=sqlite:///db.sqlite3
    DATABASE_ENGINE = "sqlite3"
    DATABASE_NAME = "/var/db/rrsm.db"
    DATABASE_USER='admin'
    DATABASE_PASS='passwd'
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
    ```
    SECRET_KEY should be a 50-characters long string of random characters from the following set: `abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)`
1. Create the virtual environment:
    ```
    [usr@host src]$ python3 -m venv env
    ```
1. Activate the virtual environment:
    ```
    [usr@host src]$ source env/bin/activate
    ```
1. Install the dependencies:
    ```
    (env) [usr@host src]$ pip install -r requirements.txt
    ```
1. Go to the root directory:
    ```
    (env) [usr@host src]$ cd rrsm/
    ```
1. Run the test server:
    ```
    (env) [usr@host rrsm]$ python3 manage.py runserver 0.0.0.0:8080
    ```