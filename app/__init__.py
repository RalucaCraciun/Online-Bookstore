import os
import time

from traceback import print_exception

from elasticsearch import Elasticsearch
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config import get_api_settings, settings
from app.routers.books import books_router
from app.routers.cart import cart_router
from app.routers.orders import orders_router
# from app.elasticsearch.elastic import create_es_client, es_client  # Import Elasticsearch functions
from app.elasticsearch.elastic import es_connect

api_settings = get_api_settings()

elastic_connection, connect_ok = es_connect


async def catch_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)  # Ensure this returns a valid response
    except Exception as e:
        print_exception(e)
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred"}
        )


def start_app() -> FastAPI:
    if not connect_ok:
        raise RuntimeError(f"Failed to initialize Elasticsearch connection: {elastic_connection}")

    # es_client = create_es_client()
    print("There", os.getenv("DEBUG"))

    application = FastAPI(
        title=api_settings.title,
        description=api_settings.description,
        version=api_settings.version,
        docs_url=api_settings.doc_url,
        redoc_url=api_settings.redoc_url,
        debug=api_settings.debug_status
    )

    application.middleware('http')(catch_exception_middleware)

    origins = [
        settings.CLIENT_ORIGIN,
        'http://localhost:5173/'
    ]

    origins = ["*"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @application.get("/")
    async def root():
        return {'detail': 'Hellow World'}

    # @application.on_event("startup")
    # async def startup_event():
    #     global es_client
    #     es_client = create_es_client()
    #     wait_for_es(es_client)
    #     if not es_client.ping():
    #         print("Elasticsearch is not available.")
    #     else:
    #         print("Connected to Elasticsearch")
    #
    # @application.on_event("shutdown")
    # async def shutdown_event():
    #     global es_client
    #     if es_client:
    #         es_client.close()
    #         print("Elasticsearch client closed.")

    application.include_router(
        books_router,
        prefix='',
        tags=['books'],
        dependencies=[]
    )

    application.include_router(
        cart_router,
        prefix='',
        tags=['cart'],
        dependencies=[]
    )

    application.include_router(
        orders_router,
        prefix='',
        tags=['orders'],
        dependencies=[]
    )

    return application


def wait_for_es(es: Elasticsearch, retries: int = 5, delay: int = 5):
    """
    Wait for Elasticsearch to be ready.
    """
    for i in range(retries):
        try:
            if es.ping():
                print("Elasticsearch is ready.")
                return
        except Exception:
            print(f"Retrying connection to Elasticsearch... ({i + 1}/{retries})")
        time.sleep(delay)
    raise RuntimeError("Elasticsearch is not ready after retries.")


app = start_app()
