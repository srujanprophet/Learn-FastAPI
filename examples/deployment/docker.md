# Deploy with Docker

In this section are the instructions and links to guides to know how to:
- Make our **FastAPI** application a Docker image/container with maximum performance. In about **5 min.**
- (Optionally) understand, what you, as a developer, need to know about HTTPS.
- Set up a Docker Swarm mode cluster with automatic HTTPS, even on a simple $5 USD/month server. In about **20 min.**
- Generate and deploy a full **FastAPI** application, using our Docker Swarm cluster, with HTTPS, etc. In about **10 min.**

We can use Docker for deployment. It has several advantages like security, replicability, development simplicity, etc.

If we are using Docker, we can use the official Docker image:
tiangolo/uvicorn-gunicorn-fastapi
This image has an "auto-tuning" mechanism included, so that you can just add your code and get very high performance automatically. And without making sacrifices.

But you can still change and update all the configurations with environment variables or configuration files.

## Create a `Dockerfile`
- Go to your project directory
- Create a `Dockerfile` with:
```DOCKERFILE
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app
```

### Raspberry Pi and other architectures
If you are running Docker in a Raspberry Pi (that has an ARM processor) or any other architecture, you can create a `Dockerfile` from scratch, based on Python base image (that is multi-architecture) and use Uvicorn alone.

In this case, your `Dockerfile` could look like:
```
FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"] 
```

## Create the **FastAPI** Code
- Create an `app` directory and enter in it.
- Create a `main.py` file with:
```python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```
- You should now have a directory structure like:
```
.
|__ app
|   |__ main.py
|__ Dockerfile
```

## Build the Docker image
- Go to the project directory (in where your `Dockerfile` is, containing your `app` directory).
- Build your FastAPI image:
```
$ docker build -t myimage .
```

## Start the Docker container
- Run a container based on your image:
```bash
$ docker run -d --name mycontainer -p 80:80 myimage
```
Now you have an optimized FastAPI server in a Docker container. Auto-tuned for your current server (and number of CPU cores).

## Check it
You should be able to check it in your Docker container's URL, for example: http://192.168.99.100/items/5?q=somequery or http://127.0.0.1/items/5?q=somequery (or equivalent, using your Docker host)
You will see something like:
`{"item_id": 5, "q": "somequery"}`

## Interactive API docs
Now you can go to http://192.168.99.100/docs or http://127.0.0.1/docs (or equivalent, using your Docker host).
You will see the automatic interactive API documentation (provided by Swagger UI)

## Alternative API docs
And you can also go to http://192.168.99.100/redoc or http://127.0.0.1/redoc (or equivalent, using your Docker host).

You will see the alternative automatic documentation (provided by ReDoc)

## Traefik
Traefik is a high performance reverse proxy / load balancer. It can do the "TLS Termination Proxy" job (apart from other features).

It has integration with Let's Encrypt. So, it can handle all the HTTPS parts, including certificate acquisition and renewal.

It also has integrations with Docker. So, you can declare your domains in each application configurations and have it read thos configurations, generate the HTTPS certificates and serve HTTPS to your application automatically, without requiring any changes in its configuration.

## Docker Swarm mode cluster with Traefik and HTTPS
You can have a Docker Swarm mode cluster set up in minutes (about 20 min) with a main Traefik handling HTTPS (including certificate acquisition and renewal).

By using Docker Swarm mode, you cam start with a "cluster" of a single machine (it can even be a $5 USD / month server) and then you can grow as much as you need adding more servers.

### Deploy a FastAPI application
The easiest way to set everything up, would be using the FastAPI Project Generators.

It is designed to be integrated with this Docker Swarm cluster with Traefik and HTTPS described above.

You can generate a project in about 2 min.

The generated project has instructions to deploy it, doing it takes another 2 min.