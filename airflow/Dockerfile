FROM apache/airflow:2.9.1-python3.10

USER root
RUN apt-get update && apt-get install -y openjdk-17-jdk && apt-get clean
USER airflow

COPY dags/ /opt/airflow/dags/

# Create initialization script
COPY --chown=airflow:root init-airflow.sh /opt/airflow/init-airflow.sh
RUN chmod +x /opt/airflow/init-airflow.sh
