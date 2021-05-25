# Docker containers to test our APIs

## Starting the containers

If `docker` and `docker-compose` are properly installed, you can start those 
containers with the following commands:

* `cd mongo_container` # from the root of this repository
* `docker-compose up`
  * as an alternative, you can use `docker-compose up -d` that will run those 
    containers in the background
* you can now visit the following link: <http://localhost:8081/> to access 
  Mongo-Express
  
## Stopping the containers

* If you used the `docker-compose up` command, you can simply use `Ctrl-C` to 
  stop the containers
  
or, you can execute the following commands:

* `cd mongo_container` # from the root of this repository
* `docker-compose down`
