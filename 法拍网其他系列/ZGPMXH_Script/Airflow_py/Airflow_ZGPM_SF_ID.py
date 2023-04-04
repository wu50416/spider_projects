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

with DAG(
        dag_id="Spider_ZGPM_SF_ID", catchup=False, default_args=default_args, tags=['spider'],
        start_date=utc_dt, max_active_runs=1, schedule_interval='30 01-23/4 * * *') as dag:
    SpiderBD = SSHOperator(ssh_conn_id="ssh.192.168.1.119.wangdong",
                           task_id="ZGPM_SF_ID",
                           command="cd /home/wangdong/fp_spider/ZGPMXH_Script/; /home/wangdong/anaconda3/envs/python3.9.5/bin/python -u Crawl_ZGPM_SF_ID.py",
                           dag=dag
                           )
