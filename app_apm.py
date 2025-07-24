import os
import logging
import random
import time
from flask import Flask
from elasticapm.contrib.flask import ElasticAPM
from dotenv import load_dotenv
import elasticapm

# Load environment variables from .env.apm
load_dotenv(dotenv_path='.apm.env')

app = Flask(__name__)

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Elastic APM
app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'my-flask-app-apm',
    'API_KEY': os.environ.get('ELASTIC_APM_API_KEY'),
    'SERVER_URL': os.environ.get('ELASTIC_APM_SERVER_URL'),
    'ENVIRONMENT': 'development',
}

apm = ElasticAPM(app)

@app.route('/')
def hello_world():
    logger.info("Root endpoint was called")
    return 'Hello, World from APM App!'

@app.route('/generate-data')
def generate_data():
    print("--- GENERATE-DATA ENDPOINT HIT ---")
    total_docs = 0
    # Each iteration generates roughly: 1 transaction, 2 spans, 2 logs, 1 metric, and sometimes 1 error.
    # This is about 7 documents per iteration, so 100 iterations will be ~700 docs.
    client = elasticapm.get_client()
    for i in range(1000):
        client.begin_transaction("task")
        try:
            elasticapm.set_custom_context({'loop_iteration': i})
            logger.info(f"Processing iteration {i}")
            total_docs += 2 # for transaction and log

            with elasticapm.capture_span("do_work_1"):
                time.sleep(random.uniform(0.01, 0.05))
                logger.warning(f"Doing some work in iteration {i}")
                total_docs += 2 # for span and log
                if i % 10 == 0:
                    try:
                        raise ValueError("A sample error")
                    except ValueError:
                        client.capture_exception()
                        total_docs += 1 # for the error
            
            with elasticapm.capture_span("do_work_2"):
                time.sleep(random.uniform(0.02, 0.07))
                total_docs += 1 # for span

            total_docs += 1 # for metric

        finally:
            client.end_transaction('task', 'success')


    return f'Generated approximately {total_docs} documents for Elastic APM.'

if __name__ == '__main__':
    print("--- STARTING FLASK SERVER (APM) ---")
    app.run(debug=True, port=5002)
