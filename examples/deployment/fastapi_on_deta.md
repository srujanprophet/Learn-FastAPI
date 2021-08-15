# Deploy FastAPI on Deta
## A basic **FastAPI** app
    - create a directory for our app, for example `./fastapidelta/` and enter in it.

### FastAPI code
- Create a `main.py` file with:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### Requirements
Now, int the same directory create a file `requirements.txt` with:
`fastapi`

### Directory structure
We will now have one directory `./fastapidelta/` with two files:
```
.
|__ main.py
|__ requirements.txt
```

## Create a free Deta account
Now create a free account on Deta, you just need an email and password.
You don't even need a credit card.

## Install the CLI
Once you have your account, install the Deta CLI:
```bash
$ curl -fsSL
https://get.deta.dev/cli.sh | sh
```

After installing it, open a new terminal so that the installed CLI is detected.
In a new terminal, confirm that it was correctly installed with:
```bash
$ deta --help
```

## Login with the CLI
Now login to Deta from the CLI with:
```bash
$ deta login
```
This will open a web browser and authenticate automatically.

## Deploy with Deta
Next, deploy your application with the Deta CLI:
```bash
$ deta new
```
You will see a JSON message similar to:
```json
{
    "name": "fastapideta",
    "runtime": "python3.7",
    "endpoint": "https://qltnci.deta.dev",
    "visor": "enabled",
    "http_auth": "enabled"
}
```

## Check it
Now open your browser in your `endpoint` URL. In this example above it was `https://qltnci.data.dev`, but yours will be different.

You will see the JSON response from your FastAPI app:
```json
{
    "Hello" : "World"
}
```
And now go to the `/docs` for your API, in the example above it would be `https://qltnci.deta.dev/docs`.

## Enable public access
By default, Deta will handle authentication using cookies for your account.

But once you are ready, you can make it public with:
```bash
$ deta auth disable
Successfully disabled http auth
```
Now we can share that URL with anyone and they will be able to access our API.

## HTTPS
Also notice that Deta correctly handles HTTPS for us, so we don't have to take care of that and can be sure that our clients will have a secure encrypted connection.

## Check the Visor
From our docs UI (they will be in a URL like `https://qlntci.deta.dev/docs`) send a request to our *path operation* `/item/{item_id}`

For example with ID `5`.

Now go to `https://web.deta.sh`.

You will see there's a section to the left called "Micros" with each of your apps.

You will see a tab with "Details", and also a tab "Visor", go to the tab "Visor".

In there you can inspect the recent requests sent to your app.

You can also edit them and re-play them.
