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
    return render_template('remote_apply_for_job.html')


@app.route('/confirm', methods=['POST'])
def confirm_for_job_application():
    code = request.args.get('code')
    return render_template('job_confirmation.html', code=code)


@app.route('/contract-sign', methods=['GET'])
def contract_sign():
    code = request.args.get('code')

    if not code:
        return render_template('error.html')

    try:
        form = HttpClient.get(f'{settings.BACKOFFICE_CONTRACT_URL}={code}').json()
        contract_url = form['contract_url']
        sign_url = form['sign_url']
    except FrontOfficeHttpError:
        return render_template('error.html')

    return render_template('contract_sign.html', contract_url=contract_url, sign_url=sign_url)


@app.route('/contract-upload')
def contract_upload():
    code = request.args.get('code')
    return render_template('contract_upload.html', code=code)


@app.route('/integrations/did/')
def sign_finish():
    return render_template('sign_finish.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
