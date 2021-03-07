import logging
import os
import base64
from urllib import parse
from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

log = logging.getLogger(__name__)


def get_env_tags(tag_list: List[str]) -> dict:
    """Create dictionary of environment tags"""
    tags = {}
    for t in tag_list:
        tag_key, env_key = t.split(":")
        env_value = os.environ.get(env_key)
        if env_value:
            tags.update({tag_key: env_value})
    return tags


config = Config(".env")

SECRET_PROVIDER = config("SECRET_PROVIDER", default=None)

if SECRET_PROVIDER == None:
    from starlette.datastructures import Secret

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)

ENV = config("ENV", default="local")
ENV_TAG_LIST = config("ENV_TAGS", cast=CommaSeparatedStrings, default="")
ENV_TAGS = get_env_tags(ENV_TAG_LIST)

APP_NAME = "app"
APP_UI_URL = config("APP_UI_URL", default="http://localhost")
