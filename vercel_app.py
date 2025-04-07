from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vercel_wsgi import handle_asgi

from main import app  # your existing FastAPI app

# Add CORS middleware again (to be safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This makes FastAPI compatible with Vercel's WSGI
def handler(environ, start_response):
    return handle_asgi(app, environ, start_response)
