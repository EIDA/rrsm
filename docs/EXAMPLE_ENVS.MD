# /git/rrsm/src/.env
    DB_NAME=stationbook
    DB_USER=admin
    DB_PASS=passwd
    DB_SERVICE=postgres
    DB_PORT=5432

# /git/rrsm/src/rrsm/.env
    SECRET_KEY='#ps1ib&=v%zsgzi5q*qp-ei*b1bg19dxv&861m@4@x+2ww6nx^'
    DEBUG=True
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=sqlite:///db.sqlite3
    DATABASE_ENGINE = "django.db.backends.sqlite3"
    DATABASE_NAME = ".rrsm.db"
    DATABASE_USER='admin'
    DATABASE_PASS='passwd'
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    CACHE_BACKEND=django.core.cache.backends.db.DatabaseCache
    # CACHE_BACKENDS
    # django.core.cache.backends.dummy.DummyCache (dev)
    # django.core.cache.backends.db.DatabaseCache
    # django.core.cache.backends.memcached.MemcachedCache
    CACHE_TIME_SHORT=1800
    CACHE_TIME_MEDIUM=3600
    CACHE_TIME_LONG=43200