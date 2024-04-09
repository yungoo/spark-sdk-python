# -*- coding: utf-8 -*-
import os

import pytest

from sparkproxy import config as qn_config
from sparkproxy import Auth


@pytest.fixture(scope='session')
def access_key():
    yield os.getenv('QINIU_ACCESS_KEY')


@pytest.fixture(scope='session')
def secret_key():
    yield os.getenv('QINIU_SECRET_KEY')


@pytest.fixture(scope='session')
def qn_auth(access_key, secret_key):
    yield Auth(access_key, secret_key)


@pytest.fixture(scope='session')
def is_travis():
    """
    migrate from old test cases.
    seems useless.
    """
    yield os.getenv('TEST_ENV') == 'travis'


@pytest.fixture(scope='function')
def set_conf_default(request):
    if hasattr(request, 'param'):
        qn_config.set_default(**request.param)
    yield
    qn_config._config = {
        'default_api_host': qn_config.API_HOST,
        'default_backup_hosts_retry_times': 2,
        'connection_timeout': 30,  # 链接超时为时间为30s
        'connection_retries': 3,  # 链接重试次数为3次
        'connection_pool': 10  # 链接池个数为10
    }

    _is_customized_default = {
        'default_api_host': False,
        'connection_timeout': False,
        'connection_retries': False,
        'connection_pool': False
    }
