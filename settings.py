import os

from dotenv import load_dotenv

load_dotenv()

HTTP_TIMEOUT = int(os.getenv('HTTP_TIMEOUT'))
SENTRY_DSN = os.getenv('SENTRY_DSN')

BACKOFFICE_SHIFT_URL = os.getenv('BACKOFFICE_SHIFT_URL')
BACKOFFICE_CONTRACT_URL = os.getenv('BACKOFFICE_CONTRACT_URL')

FORM_DEFAULT_ERROR_MESSAGE = 'Оу! 😮 Что-то пошло не так! Обратитесь в службу поддержки 🔨: %0A%0Ahttps://t.me/easytap_support_bot'

DID_CLIENT_ID = os.getenv('DID_CLIENT_ID')
DID_CLIENT_SECRET = os.getenv('DID_CLIENT_SECRET')
DID_STATE = os.getenv('DID_STATE')
DID_REDIRECT_URI = os.getenv('DID_REDIRECT_URI')
DID_SIGN_URL = os.getenv('DID_SIGN_URL')
DID_UPLOAD_DOCUMENT_URL = os.getenv('DID_UPLOAD_DOCUMENT_URL')
DID_OBTAIN_ACCESS_TOKEN_URL = os.getenv('DID_OBTAIN_ACCESS_TOKEN_URL')
DID_OBTAIN_DOCUMENT_SIGNATURE_URL = os.getenv('DID_OBTAIN_DOCUMENT_SIGNATURE_URL')

WAITING_FOR_GENERATING_CONTRACT_FILE = os.getenv('WAITING_FOR_GENERATING_CONTRACT_FILE')

DB_NAME = 'front-office.db'
API_KEY = os.getenv('API_KEY')
HOSTNAME = os.getenv('HOSTNAME')
