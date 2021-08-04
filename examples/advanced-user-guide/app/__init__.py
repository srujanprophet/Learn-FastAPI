"""
The API docs use **Swagger UI** and **ReDoc**, and each of those need some JavaScript and CSS files.

By default, those files are served from a CDN

But it's possible to customize it, we can set a specific CDN, or serve the file ourselves.

That's useful, for example, if we need our app to keep working even while offline, without open Internet access, or in a local network.

Here, we'll see how to serve those file ourselves, in the same FastAPI app, and configure the docs to use them.
"""