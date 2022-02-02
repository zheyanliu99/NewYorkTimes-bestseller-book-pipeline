from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.models import Variable

import datetime
import csv
import requests
import json
import pandas as pd

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5)
}

email_list = ['yan.test@gmail.com', 'zheyan.test@gmail.com', 'zheyan.test@yahoo.com']

def download_books():
    my_key = 'CXuUEJbjPaKIkPDIuzgIuijzx2YGgg4J'
    today = datetime.datetime.now()
    date = today.strftime("%Y-%m-%d")
    # weeknum = today.isocalendar().week
    year = today.isocalendar()[0]
    week =  today.isocalendar()[1]
    book_types = ['combined-print-and-e-book-fiction', 'combined-print-and-e-book-nonfiction']
    for book_type in book_types:
        # url = f'https://api.nytimes.com/svc/books/v3/lists.json?list={book_type}&bestsellers-date={date}&api-key={my_key}'
        r = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/{date}/{book_type}.json?api-key={my_key}')
        data = r.json()

        title = []
        author = []
        publisher = []
        price = []
        description = []
        amazon_product_url = []

        for book in data['results']['books']:
            title.append(book['title'])
            author.append(book['author'])
            publisher.append(book['publisher'])
            price.append(book['price'])
            description.append(book['description'])
            amazon_product_url.append(book['amazon_product_url'])

        book_dict = {
            'title':title,
            'author':author,
            'publisher':publisher,
            'price':price,
            'description':description,
            'amazon_product_url':amazon_product_url
        }

        book_df = pd.DataFrame(book_dict, columns = ['title', 'author', 'publisher', 'price', 'description', 'amazon_product_url'])
        book_df.to_csv(f'/opt/airflow/dags/files/{book_type}_{date}.csv', index = False)
        
    return (year, week)

def check_email(**context):
    year, week = context['ti'].xcom_pull(task_ids='downloading_books')
    # email_list = ['yan.test@gmail.com', 'zheyan.test@gmail.com']
    email_df = pd.read_csv('/opt/airflow/dags/files/email_sent.csv')
    email_df = email_df[(email_df['year']==year)&(email_df['week']==week)]
    email_sublist = [email for email in email_list if email not in email_df.email.to_list()]

    return ','.join(email_sublist)


def update_sent_emails(**context):
    with open(r'/opt/airflow/dags/files/email_sent.csv', 'a') as file:
        writer = csv.writer(file)
        year, week = context['ti'].xcom_pull(task_ids='downloading_books')
        for email in context['ti'].xcom_pull(task_ids='check_emails').split(','):
            if email:
                newrow = [email, year, week]
                writer.writerow(newrow)


with DAG("nyt_book_pipeline", start_date=datetime.datetime(2021, 1 ,1), 
    schedule_interval="@daily", default_args=default_args, catchup=False) as dag:

    downloading_books = PythonOperator(
        task_id="downloading_books",
        python_callable=download_books
    )

    check_emails = PythonOperator(
        task_id="check_emails",
        python_callable=check_email
    )

    send_emails = EmailOperator(
        task_id='send_emails',
        to="{{ task_instance.xcom_pull(task_ids='check_emails') }}",
        subject="New York Times Weekly Bestseller Books",
        html_content="<h3>forex_data_pipeline</h3>"
    )

    update_sent_emails = PythonOperator(
        task_id="update_sent_emails",
        python_callable=update_sent_emails
    )
    
    downloading_books >> check_emails >> send_emails >> update_sent_emails