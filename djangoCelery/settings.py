"""
Django settings for djangoCelery project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9t%x^^-x_*c(kjc5y#56&v+uyr3*&wh$oq^1q2^$06o@8u%cb^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',
    'django_celery_results',
    'django_celery_beat'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoCelery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoCelery.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangoCelery',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'POST': 3306,

    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 最重要的配置，设置消息broker,格式为：db://user:password@host:port/dbname
# 如果redis安装在本机，使用localhost
# 如果docker部署的redis，使用redis://redis:6379
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"

# celery时区设置，建议与Django settings中TIME_ZONE同样时区，防止时差
# Django设置时区需同时设置USE_TZ=True和TIME_ZONE = 'Asia/Shanghai'
CELERY_TIMEZONE = TIME_ZONE

# 为django_celery_results存储Celery任务执行结果设置后台
# 格式为：db+scheme://user:password@host:port/dbname
# 支持数据库django-db和缓存django-cache存储任务状态及结果
CELERY_RESULT_BACKEND = "django-db"
# celery内容等消息的格式设置，默认json
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# 为任务设置超时时间，单位秒。超时即中止，执行下个任务。
CELERY_TASK_TIME_LIMIT = 5

# 为存储结果设置过期日期，默认1天过期。如果beat开启，Celery每天会自动清除。
# 设为0，存储结果永不过期
CELERY_RESULT_EXPIRES = 1

# 任务限流
CELERY_TASK_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}

# Worker并发数量，一般默认CPU核数，可以不设置
CELERY_WORKER_CONCURRENCY = 2

# 每个worker执行了多少任务就会死掉，默认是无限的
CELERY_WORKER_MAX_TASKS_PER_CHILD = 200


# 参考：https://blog.csdn.net/weixin_42134789/article/details/116311095?utm_term=celery%E5%A4%9A%E4%B8%AA%E9%A1%B9%E7%9B%AE&utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~sobaiduweb~default-1-116311095&spm=3001.4430
from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    "add-every-30s": {
        "task": "app.tasks.add",
        'schedule': 30.0,  # 每30秒执行1次
        'args': (3, 8),  # 传递参数
        'options': {'queue': 'default'}
    },
    "add-every-day": {
        "task": "app.tasks.add",
        'schedule': timedelta(hours=1),  # 每小时执行1次
        'args': (3, 6)  # 传递参数
    },
}

# 如果每次添加或修改周期性任务都要修改配置文件非常不方便，一个更好的方式是使用任务调度器。先在settings.py中将任务调度器设为DatabaseScheduler
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# 配置多队列
from kombu import Queue, Exchange

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('heavy_tasks', Exchange('heavy_tasks'), routing_key='heavy_tasks'),
)
CELERY_TASK_ROUTES = {
    'app.tasks.heave_tasks': 'heavy_tasks'
}

# # 路由（哪个任务放入哪个队列）
# CELERY_ROUTES = {   # app.tasks.add这个任务进去add队列并routeing_key为xue.add
#     'app.tasks.add': {
#         'queue': 'default',
#         'routing_key': 'default',
#     }
# }
