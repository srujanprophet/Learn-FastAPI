# Deploy Manually
You can deploy **FastAPI** manually as well.

You just need to install an ASGI compatible server like:
```bash
$ pip install 'uvicorn[standard]'
```

And run your application the same way you have done in the tutorials, but without the --reload option, e.g.:
```bash
$ uvicorn main:app --host 0.0.0.0 --port 80
```

You might want to set up some tooling to make sure it is restarted automatically if it stops.

You might also want to install Gunicorn and use it as a manager for Uvicorn, or use Hypercorn with multiple workers.

Making sure to fine-tune the number of workers, etc.

But if you are doing all that, you might just use the Docker image that does it automatically.