import os

from dotenv import load_dotenv

load_dotenv()

HTTP_TIMEOUT = int(os.getenv('HTTP_TIMEOUT'))
SENTRY_DSN = os.getenv('SENTRY_DSN')

BACKOFFICE_SHIFT_URL = os.getenv('BACKOFFICE_SHIFT_URL')
FORM_DEFAULT_ERROR_MESSAGE = 'Оу! 😮 Что-то пошло не так! Обратитесь в службу поддержки 🔨: %0A%0Ahttps://t.me/easytap_support_bot'
