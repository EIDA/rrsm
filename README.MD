# RSSM

This repository is deployed at [orfeus-eu.org/rrsm](https://orfeus-eu.org/rrsm/).

## Quickstart

1. Create the .env configuration file from `/src/rrsm/.env.sample` and adjust its values. Example test server configuration:

   ```bash
   cp src/rrsm/.env.sample src/rrsm/.env
   ```

   - SECRET*KEY should be a 50-characters long string of random characters from the following set: `abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&\*(-*=+)`
   - Only `SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` settigns are meaningful. Rest of them can be left unchanged, they are here just to satisfy the Django Framework
   - `CACHE_BACKEND` can be set to:
     - `django.core.cache.backends.memcached.MemcachedCache` with location `127.0.0.1:11211` (default for python-memcached)
     - `django.core.cache.backends.filebased.FileBasedCache` with location e.g. `/data/rrsm_cache/`
     - `django.core.cache.backends.db.DatabaseCache` with location e.g. `rrsm_cache_table`
     - `django.core.cache.backends.dummy.DummyCache` can be used during development
   - `CACHE_TIME_SHORT`, `CACHE_TIME_MEDIUM` and `CACHE_TIME_LONG` are timers (in seconds) used for cache validation assigned to pages depending on how often their content changes
   - `RRSM_URL_BASE` allows adding a URL prefix to all RRSM URLs

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
   - `/src/docker-compose.yml`
   - `/src/nginx/sites-enabled/django`
1. Build and run the images:

   ```bash
   cd src/
   docker-compose -p 'rrsm' up -d
   ```

1. Connecting to a running container can be done using:

   ```bash
   docker exec -it <CONTAINER ID> sh
   ```

## Tests

Tests can be executed using following command:

```bash
python3 src/rrsm/manage.py test rrsmi
```

## Logs

Tail can be used to follow the app logs:

```bash
tail -f src/rrsm/logs/rrsm.log
```

## Remarks

- The WebService response times in some cases can get long resulting in `504 Gateway Timeout`. This can be prevented by modifying the `/etc/ninx/nginx.conf` on the Nginx container and adding following lines to the basic config:

  ```bash
  proxy_read_timeout 300;
  ```
