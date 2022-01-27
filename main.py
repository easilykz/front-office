import time
import json

from flask import Flask, request, render_template
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


@app.route('/new', methods=['GET'])
def new_worker():
    return render_template('new_worker.html')


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
    return render_template('apply_for_job.html')


@app.route('/contract-doc', methods=['GET'])
def contract_doc():
    code = request.args.get('code')
    document_url = None
    next_url = None

    has_next = request.args.get('n') == '✓'

    if has_next:
        time.sleep(int(settings.WAITING_FOR_GENERATING_CONTRACT_FILE))

    if code:
        try:
            form = HttpClient.get(f'{settings.BACKOFFICE_CONTRACT_URL}={code}').json()
            document_url = form.get('contract_url')
            next_url = form.get('sign_url')
        except json.decoder.JSONDecodeError:
            return render_template('error.html')
        except FrontOfficeHttpError:
            return render_template('error.html')

    has_next = has_next and document_url is not None
    return render_template('contract_doc.html', document_url=document_url, has_next=has_next, next_url=next_url)


@app.route('/integrations/did/')
def sign_finish():
    return 'hi'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
