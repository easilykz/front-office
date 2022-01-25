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

    if code:
        try:
            description = HttpClient.get(f'{settings.BACKOFFICE_SHIFT_URL}={code}').content.decode('utf8').strip('"')
        except FrontOfficeHttpError:
            pass

    return render_template('apply.html', description=description)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
