import time
import json
import string
import sqlite3 as sl

from flask import Flask, request, render_template, render_template_string
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

import settings
from http_client import HttpClient, FrontOfficeHttpError

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
app = Flask(__name__)


class DB:
    def __init__(self):
        self.conn = sl.connect(settings.DB_NAME)

    def init_schema(self):
        schema_sql = '''
            CREATE TABLE IF NOT EXISTS DYNAMIC_FORM (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                title TEXT,
                jotform_url TEXT
            );
        '''
        self.execute_sql(schema_sql)

    def execute_sql(self, sql):
        with self.conn:
            return list(self.conn.execute(sql))


db_client = DB()
db_client.init_schema()


@app.route('/new', methods=['GET'])
def new_worker():
    return render_template('new_worker.html')


@app.route('/new/thnx', methods=['GET', 'POST'])
def new_worker_confirmation():
    return render_template('new_worker_confirmation.html')


@app.route('/apply', methods=['GET'])
def apply_to_shift():
    code = request.args.get('code')
    description = settings.FORM_DEFAULT_ERROR_MESSAGE
    shift_id = None

    if code:
        try:
            form = HttpClient.get(f'{settings.BACKOFFICE_SHIFT_URL}={code}').json()

            description = form['text'].strip('"')
            shift_id = form['shift_id']
        except FrontOfficeHttpError:
            pass

    return render_template('apply.html', description=description, shift_id=shift_id)


@app.route('/contract', methods=['GET'])
def apply_for_job():
    return render_template('apply_for_job.html')


@app.route('/contract-remote', methods=['GET'])
def remote_apply_for_job():
    return render_template('remote_apply_for_job.html')


@app.route('/confirm', methods=['POST'])
def confirm_for_job_application():
    code = request.args.get('code')

    try:
        got = HttpClient.get(f'{settings.BACKOFFICE_WORKER_STATUS_URL}?code={code}').json()
    except FrontOfficeHttpError:
        return render_template('error.html')

    if not got.get('success') or not got.get('html_status_text'):
        return render_template('error.html')

    return render_template('job_confirmation.html', code=code, status_text=got.get('html_status_text'))


@app.route('/contract-sign', methods=['GET'])
def contract_sign():
    user_code = request.args.get('user')
    document_type = request.args.get('document') or 'work_contract'  # по умолчанию

    if not user_code:
        return render_template('error.html')

    try:
        form = HttpClient.get(f'{settings.BACKOFFICE_DOCUMENT_SIGN_DETAILS_URL}?user={user_code}&document={document_type}').json()
        if not form['success']:
            return render_template('error.html')

        contract_url = form['contract_url']
        sign_url = form['sign_url']
    except FrontOfficeHttpError:
        return render_template('error.html')

    return render_template('contract_sign.html', contract_url=contract_url, sign_url=sign_url)


@app.route('/contract-upload', methods=['POST', 'GET'])
def contract_upload():
    code = request.args.get('code')
    return render_template('contract_upload.html', code=code)


@app.route('/integrations/did/')
def sign_finish():
    try:
        code = request.args['code']
        document_id = request.args['scope'].split('sign.')[1].split('+')[0]

        got = HttpClient.post(settings.BACKOFFICE_UPLOAD_DOCUMENT_SIGNATURE_URL, data={'code': code, 'document_id': document_id})

        if not got.json().get('success'):
            sentry_sdk.capture_message(f'#front-office-fail: {got.json()}')

    except Exception as e:
        sentry_sdk.capture_exception(e)

    return render_template('sign_finish.html')


@app.route('/business')
def business_form():
    return render_template('business.html')


@app.route('/partners-mobile/')
def partners_mobile_form():
    return render_template('partners_mobile.html')


@app.route('/partners-mobile/finish/')
def partners_mobile_finish_form():
    return render_template('partners_mobile_finish.html')


@app.route('/dynamic-form-upload/', methods=['GET'])
def dynamic_form_upload():
    name = request.args.get('name')
    title = request.args.get('title')
    jotform_url = request.args.get('jotform_url')
    key = request.args.get('key')

    if not name or not title or not jotform_url:
        return render_template_string('не все параметры переданы')

    if key != settings.API_KEY:
        return render_template_string('неправильный ключ')

    db_client.execute_sql(f'INSERT INTO DYNAMIC_FORM(name, title, jotform_url) values("{name}", "{title}", "{jotform_url}");')
    url = f'https://{settings.HOSTNAME}/form/{name}'

    return render_template_string(f'успех! проверьте вашу форму: {url}')


@app.route('/form/<name>', methods=['GET'])
def dynamic_form(name):
    # простая защита от sql-инъекции
    allowed_symbols = set(list(string.ascii_letters) + ['-'])
    if not set(name).issubset(allowed_symbols):
        return render_template('error.html')

    got = db_client.execute_sql(f'SELECT title, jotform_url FROM DYNAMIC_FORM WHERE name = "{name}";')

    if not got:
        return render_template('error.html')

    return render_template('dynamic_form.html', title=got[-1][0], jotform_url=got[-1][1])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
