# metadatablocks_api

Learning to use Flama and FastAPI in the context of our metadata blocks

# Deploying the API

## Installing the requirements

To install the requirements for this API, you need to execute the following 
commands, at the root of this repository: 

```shell
python -m venv venv   # Creating a virtual environment for our application
source venv/bin/activate  # Activating the virtual environment
pip install -r requirements.txt  # Installing requirements
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
uvicorn main:app --reload
```

and visit the following URL: <http://127.0.0.1:8000/measurements/>. The 
first call should not display any data, but if you visit the <http://127.0.0.
1:8000/measurements/add_them_all> URL, the API will populate the `strict` 
database with some data as you'll see by visiting <http://127.0.0.
1:8000/measurements/> again.  

You can also visit either <http://127.0.0.1:8000/docs> or <http://127.0.0.
1:8000/redoc> to consult the documentation of the API generated by FastAPI. 
