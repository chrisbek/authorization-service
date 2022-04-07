from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from app.adapters.rest.authorization_controller import router as authorization_router
from app.adapters.rest.client_controller import router as client_router
from app.adapters.rest.user_controller import router as user_router
from app.adapters.rest.exception_serializer import add_exception_handlers_to_app
# from fastapi.middleware.cors import CORSMiddleware


def init() -> FastAPI:
    app = FastAPI(
        title="Local authorization server",
        description='Dummy authorization server for local testing',
        root_path_in_servers=False,
        servers=[
            {"url": f'https://authorization-server.local', "description": "Local environment"},
        ]
    )
    # Mount order matters
    app.include_router(authorization_router, prefix='/auth', tags=['auth'])
    app.include_router(client_router, prefix='/api', tags=['api/client'])
    app.include_router(user_router, prefix='/api', tags=['api/user'])
    # app.mount(
    #     "/",
    #     StaticFiles(directory="./dist", html=True),
    #     name="static"
    # )
    add_exception_handlers_to_app(app)

    # origins = [
    #     "http://localhost:8080",
    # ]
    #
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=origins,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    return app
