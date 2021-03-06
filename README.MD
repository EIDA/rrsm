# RSSM
This repository is deployed at [orfeus-eu.org/rrsm](https://orfeus-eu.org/rrsm/).

## Quickstart

1. Create the .env configuration file in `/src/rrsm/.env`. Example test server configuration:

    ```bash
    SECRET_KEY='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    DEBUG=True
    ALLOWED_HOSTS=.localhost,127.0.0.1
    # Database configuration
    DATABASE_URL=sqlite:///db.sqlite3
    DATABASE_ENGINE=django.db.backends.sqlite3
    DATABASE_NAME='rrsm.db'
    DATABASE_USER='admin'
    DATABASE_PASS='passwd'
    # Email configuration
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    # Cache configuration
    CACHE_BACKEND=django.core.cache.backends.filebased.FileBasedCache
    CACHE_LOCATION='rrsm_cache'
    CACHE_TIME_SHORT=0
    CACHE_TIME_MEDIUM=0
    CACHE_TIME_LONG=0
    # URL base
    RRSM_URL_BASE=''
    # Configuration for outliers filtering
    OUTLIER_FILTERING_ENABLED=True
    PGA_MIN=0.00001
    PGA_MAX=9.806
    PGV_MIN=0.000001
    PGV_MAX=1
    PGV_BROADBAND_MIN=0.000001
    PGV_BROADBAND_MAX=0.013
    ```

    * SECRET_KEY should be a 50-characters long string of random characters from the following set: `abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)`
    * Only `SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` settigns are meaningful. Rest of them can be left unchanged, they are here just to satisfy the Django Framework
    * `CACHE_BACKEND` can be set to:
        * `django.core.cache.backends.memcached.MemcachedCache` with location `127.0.0.1:11211` (default for python-memcached)
        * `django.core.cache.backends.filebased.FileBasedCache` with location e.g. `/data/rrsm_cache/`
        * `django.core.cache.backends.db.DatabaseCache` with location e.g. `rrsm_cache_table`
        * `django.core.cache.backends.dummy.DummyCache` can be used during development 
    * `CACHE_TIME_SHORT`, `CACHE_TIME_MEDIUM` and `CACHE_TIME_LONG` are timers (in seconds) used for cache validation assigned to pages depending on how often their content changes
    * `RRSM_URL_BASE` allows adding a URL prefix to all RRSM URLs
1. Create the virtual environment:

    ```bash
    python3 -m venv env
    ```

1. Activate the virtual environment:

    ```bash
    source env/bin/activate
    ```

1. Let's upgrade pip and install the dependencies:

    ```bash
    pip install --upgrade pip
    pip install -r src/rrsm/requirements.txt
    ```

1. Run the test server:

    ```bash
    python3 src/rrsm/manage.py runserver 0.0.0.0:8000
    ```

## Docker

1. Make sure ports are set up correctly
    * `/src/docker-compose.yml`
    * `/src/nginx/sites-enabled/django`
1. Build and run the images:

    ```bash
    cd src/
    docker-compose -p 'rrsm' up -d
    ```

1. Connecting to a running container can be done using:

    ```bash
    docker exec -it <CONTAINER ID> sh
    ```

## Logs

Tail can be used to follow the app logs:

```bash
    tail -f src/rrsm/logs/rrsm.log
```

## Remarks

* The WebService response times in some cases can get long resulting in `504 Gateway Timeout`. This can be prevented by modifying the `/etc/ninx/nginx.conf` on the Nginx container and adding following lines to the basic config:

    ```bash
    proxy_read_timeout 300;
    ```
