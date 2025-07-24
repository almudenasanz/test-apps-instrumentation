# Python Instrumentation Project for Elastic

This project demonstrates two different ways to instrument a Python application to send telemetry data to Elastic Observability:

1.  **`app_apm.py`**: A Flask application instrumented with the Elastic APM Python Agent.
2.  **`app_otel.py`**: A simple Python script instrumented with OpenTelemetry.

Both applications are configured to generate traces, logs, and errors. Follow the instructions below to run either version.

## Running the APM Agent Application

This project includes a Flask application, `app_apm.py`, that is instrumented with the Elastic APM agent.

### 1. Install Dependencies

If you haven't already, install the required Python packages:

```bash
pip3 install -r requirements.txt
```

### 2. Configure APM Environment Variables

Copy the example environment file to a new `.apm.env` file:

```bash
cp .apm.env.example .apm.env
```

Next, open `.apm.env` and add your Elastic APM server URL and API key.

### 3. Run the Application

A helper script, `run_apm.sh`, is provided to export the environment variables and run the application.

First, make the script executable:

```bash
chmod +x run_apm.sh
```

Then, run the script:

```bash
./run_apm.sh
```

The application will start on `http://127.0.0.1:5002`.

### 4. Generate APM Data

You can generate APM data by visiting the `/generate-data` endpoint.

URL: `http://127.0.0.1:5002/generate-data`

---

## Running the OpenTelemetry Application

This project also includes a script, `app_otel.py`, that uses OpenTelemetry for instrumentation instead of the Elastic APM agent.

### 1. Install Dependencies

If you haven't already, install the required Python packages:

```bash
pip3 install -r requirements.txt
```

### 2. Configure OpenTelemetry Environment Variables

Copy the example environment file to a new `.otel.env` file:

```bash
cp .otel.env.example .otel.env
```

Next, open `.otel.env` and fill in the required values for the following variables:

- `OTEL_EXPORTER_OTLP_ENDPOINT`: Your Elastic APM OTLP endpoint URL.
- `OTEL_EXPORTER_OTLP_HEADERS`: Your Elastic APM secret token, formatted as `Authorization=Bearer YOUR_TOKEN`. Use %20 to represent the space character.

The other variables are pre-configured for a typical setup:

- `OTEL_RESOURCE_ATTRIBUTES`: Sets the service name, version, and environment.
- `OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED`: Enables automatic log instrumentation.
- `OTEL_PYTHON_LOG_CORRELATION`: Injects trace context into logs.
- `OTEL_METRICS_EXPORTER`: Configures metrics to be sent via OTLP.
- `ELASTIC_OTEL_SYSTEM_METRICS_ENABLED`: Enables system-level metrics.
- `OTEL_METRIC_EXPORT_INTERVAL`: Sets the metric export interval to 5 seconds.
- `OTEL_LOGS_EXPORTER`: Sends logs to both OTLP and the console.

### 3. Run the Application

A helper script, `run_otel.sh`, is provided to export the environment variables and run the application with OpenTelemetry auto-instrumentation.

First, make the script executable:

```bash
chmod +x run_otel.sh
```

Then, run the script:

```bash
./run_otel.sh
```

This will start the `app_otel.py` script, and you will see logs, traces, and metrics being sent to your Elastic deployment.
