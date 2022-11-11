from routes.routes import router as router_routes
from routes.vessels import router as vessels_router
from routes.ports import router as ports_router
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Dark Activity Detection",
        version="0.1.0",
        description="This API is used for dark activity detection in AIS systems.",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.include_router(vessels_router)
app.include_router(ports_router)
app.include_router(router_routes)

app.openapi = custom_openapi
