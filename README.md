# Flask APM Project

This is a minimal Flask project configured to send APM data to an Elastic APM server.

## Setup

1.  **Create and activate a conda environment:**

    ```bash
    conda create --name flask-apm-env python=3.9
    conda activate flask-apm-env
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your environment variables:**

    Copy the `.env.example` file to a new file named `.env`:

    ```bash
    cp .env.example .env
    ```

    Then, open the `.env` file and add your Elastic APM server URL and secret token.

## Running the application

To run the Flask application, use the following command:

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`.

### Generate APM data

You can generate APM data by visiting the `/generate-data` endpoint in your browser or using a tool like `curl`.

URL: `http://127.0.0.1:5000/generate-data`



