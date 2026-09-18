FROM apache/airflow:3.0.6-python3.12

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt
