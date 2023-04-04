import pytz
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "email": ["wangdong@iunispace.com"],
    "email_on_failure": True,
}
tz = pytz.timezone('Asia/Shanghai')
dt = datetime(2022, 11, 1, tzinfo=tz)
utc_dt = dt.astimezone(pytz.utc).replace(tzinfo=None)
# 00 20 * * *   20:00，每天
with DAG(
        dag_id="Backups_Start", catchup=False, default_args=default_args, tags=['spider'],
        start_date=utc_dt, max_active_runs=1, schedule_interval='00 20 * * *') as dag:
    SpiderBD = SSHOperator(ssh_conn_id="ssh.192.168.1.119.wangdong",
                           task_id="DB_Backups",
                           command="cd /home/wangdong/fp_spider/DB_Backups/; /home/wangdong/anaconda3/envs/python3.9.5/bin/python -u Backups_Start.py",
                           dag=dag
                           )
