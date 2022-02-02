# NewYorkTimes-bestseller-book-pipeline
This data pipeline will programmatically fetch the latest list of Combined Print &amp; E-Book Fiction and Combined Print &amp; E-Book Nonfiction through NYTimes Books API and send the results to some email recipients.

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

Docker-compose airflow

```
docker-compose up -d
```

When all containers are healthy, Open http://localhost:8080

**Import variables in the UI by Admin -> variables**, variables file is config/variables_config.json. If you don't do this step, it will use the default email list ['yan.test@gmail.com', 'zheyan.test@gmail.com', 'zheyan.test@yahoo.com']
![image](https://user-images.githubusercontent.com/90377706/152095188-f6cc7018-b370-40b0-956c-ff22650c0047.png)






