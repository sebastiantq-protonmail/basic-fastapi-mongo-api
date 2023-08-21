
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes and config modules import
from app.api.config.env import API_NAME
from app.api.routes.routes import router

app = FastAPI(
    openapi_url=f'/api/v1/{API_NAME}/openapi.json',
    docs_url=f'/api/v1/{API_NAME}/docs',
    title=f'{API_NAME} API',
    description='ENTER THE DESCRIPTION.',
    version='0.0.1',
    terms_of_service='',
    contact={
        'name': '',
        'url': '',
        'email': '',
    },
    license_info={
        'name': '',
        'url': '',
    },
)

# CORS middleware configuration
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
async def on_startup():
    # Actions to be executed when the API starts.
    print('API started')

@app.on_event('shutdown')
async def on_shutdown():
    # Actions to be executed when the API shuts down.
    print('API shut down')

# Include the routes
app.include_router(router, prefix=f'/api/v1/{API_NAME}')
