# NewYorkTimes-bestseller-book-pipeline
This data pipeline will programmatically fetch the latest list of Combined Print &amp; E-Book Fiction and Combined Print &amp; E-Book Nonfiction through [NYTimes Books API](https://developer.nytimes.com/docs/books-product/1/routes/lists.json/get)and send the results to some email recipients.

## Steps

Make sure you download Docker Desktop.

First, clone this repo 

```
git clone https://github.com/zheyanliu99/NewYorkTimes-bestseller-book-pipeline.git
```

Make a new folder 'logs' in current directory
```
mkdir logs
```

Then, initialize docker with 
```
docker-compose up airflow-init
```

**Do this only if you are Linux/Mac user**

```
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

Docker-compose airflow (this can take 10 minutes for the first time)

```
docker-compose up -d
```

When all containers are healthy, Open http://localhost:8080

**Import variables in the UI by Admin -> variables**, variables file is config/variables_config.json. If you don't do this step, it will use the default email list ['yan.test@gmail.com', 'zheyan.test@gmail.com', 'zheyan.test@yahoo.com']. You succeed if you see something like this.
![image](https://user-images.githubusercontent.com/90377706/152095188-f6cc7018-b370-40b0-956c-ff22650c0047.png)

That's all for the setup, contact me if you met any issues or refer to this video https://www.youtube.com/watch?v=aTaytcxy2Ck&t=403s.

## Examples

Graph View of the DAG
![image](https://user-images.githubusercontent.com/90377706/152095681-3d06f911-aad9-41c2-98e7-2957c1a82b65.png)


Email sent
![image](https://user-images.githubusercontent.com/90377706/152095720-b7e736a7-fb75-42f9-bb0b-b67d6a7576a0.png)

Raise error if all the user in the email_list are sent
![image](https://user-images.githubusercontent.com/90377706/152095851-9048d31b-7896-472c-9d8f-f04165a33e80.png)






