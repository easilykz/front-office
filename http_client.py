import requests
from sentry_sdk import capture_exception

import settings


class FrontOfficeHttpError(Exception):
    pass


class HttpClient:
    @classmethod
    def post(cls, *args, **kwargs):
        kwargs.update({'timeout': settings.HTTP_TIMEOUT})

        try:
            got = requests.post(*args, **kwargs)
            return got
        except requests.exceptions.Timeout:
            capture_exception(f'Timeout POST: {args} {kwargs}')
            raise FrontOfficeHttpError()

    @classmethod
    def get(cls, *args, **kwargs):
        kwargs.update({'timeout': settings.HTTP_TIMEOUT})

        try:
            got = requests.get(*args, **kwargs)
            return got
        except requests.exceptions.Timeout:
            capture_exception(f'Timeout GET: {args} {kwargs}')
            raise FrontOfficeHttpError()
