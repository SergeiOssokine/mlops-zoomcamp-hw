FROM apache/airflow:latest-python3.10

ENV AIRFLOW_HOME=/usr/local/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


WORKDIR $AIRFLOW_HOME

COPY scripts scripts

#RUN chmod +x scripts

USER $AIRFLOW_UID