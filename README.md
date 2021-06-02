# metadatablocks_api

Learning to use Flama and FastAPI in the context of our metadata blocks

# Deploying the API

## Installing the requirements

To install the requirements for this API, you need to execute the following 
command, at the root of this repository: 

```shell
pip install -r requirements.txt
```

## Starting the API

Before starting the API, verify that the MongoDB container is started. You can 
do that by running the `docker-compose ps` command in the `mongo_container` 
directory. You should see something like:

```text
             Name                            Command               State            Ports          
---------------------------------------------------------------------------------------------------
mongo_container_mongo-express_1   tini -- /docker-entrypoint ...   Up      0.0.0.0:8081->8081/tcp  
mongo_container_mongo_mbapi_1     docker-entrypoint.sh mongod      Up      0.0.0.0:27017->27017/tcp
```

You can then go to the `src` directory and run the following command from there: 

```shell
uvicorn fa.main:app --reload
```

and visit the following URL: <http://127.0.0.1:8000/measurements/>. The 
first call should not display any data, but if you visit the <http://127.0.0.
1:8000/measurements/add_them_all> URL, the API will populate the `strict` 
database with some data as you'll see by visiting <http://127.0.0.
1:8000/measurements/> again.  
