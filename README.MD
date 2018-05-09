# Quick start guide
1. Create the .env configuration file in `/src/rrsm/.env`. Example test server configuration:
    ```
    SECRET_KEY='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    DEBUG=False
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=sqlite:///db.sqlite3
    DATABASE_ENGINE = "sqlite3"
    DATABASE_NAME = "rrsm.db"
    DATABASE_USER='admin'
    DATABASE_PASS='passwd'
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    CACHE_BACKEND=django.core.cache.backends.filebased.FileBasedCache
    CACHE_LOCATION='rrsm_cache'
    CACHE_TIME_SHORT=0
    CACHE_TIME_MEDIUM=0
    CACHE_TIME_LONG=0
    ```
    * SECRET_KEY should be a 50-characters long string of random characters from the following set: `abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)`
    * Only `SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` settigns are meaningful. Rest of them can be left unchanged, they are here just to satisfy the Django Framework
    * `CACHE_BACKEND` can be set to:
        * `django.core.cache.backends.memcached.MemcachedCache` with location `127.0.0.1:11211` (default for python-memcached) 
        * `django.core.cache.backends.filebased.FileBasedCache` with location e.g. `/data/rrsm_cache/`
        * `django.core.cache.backends.db.DatabaseCache` with location e.g. `rrsm_cache_table`
        * `django.core.cache.backends.dummy.DummyCache` can be used during development 
    * `CACHE_TIME_SHORT`, `CACHE_TIME_MEDIUM` and `CACHE_TIME_LONG` are timers (in seconds) used for cache validation assigned to pages depending on how often their content changes
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
    (env) [usr@host rrsm]$ python3 manage.py runserver 0.0.0.0:8000
    ```
# Docker
1. Make sure ports are set up correctly
    * `/rrsm/src/docker-compose.yml`
    * `/rrsm/src/nginx/sites-enabled/django`
1. Build and run the images
    ```
    (env) [usr@host src]$ docker-compose -p 'rrsm' up -d
    ```
1. Connecting to a running container can be done using:
    ```
    [usr@host ~]$ docker exec -it <CONTAINER ID> sh
    ```
# Logs
Tail can be used to follow the app logs:
```
[usr@host rrsm]$ tail -f logs/rrsm.log
```
# Remarks
* The WebService response times in some cases can get long resulting in `504 Gateway Timeout`. This can be prevented by modifying the `/etc/ninx/nginx.conf` on the Nginx container and adding following lines to the basic config:
    ```
    proxy_read_timeout 300;
    ```