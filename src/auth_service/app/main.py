from fastapi import FastAPI
from src.auth_service.app.utils import add_routers, add_exception_handlers

app = FastAPI()

add_routers(app)
add_exception_handlers(app)
