from fastapi import FastAPI, Depends
from icecream import ic

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# from fastapi_limiter import FastAPILimiter
# from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

from fastapi import APIRouter
# from src.services.auth import auth_service

import uvicorn

# alembic revision --autogenerate -m 'Init'
# alembic upgrade head

# docker-compose up -d
# docker exec -it dcb9d sh

# uvicorn main:app --host localhost --port 8000 --reload

app = FastAPI()

# auth_router = APIRouter(prefix='/auth', tags=['auth'])
# email_router = APIRouter(prefix='/email', tags=['email'])
# contacts_router = APIRouter(prefix='/contacts', tags=['contacts'])

from src.services.slowapi import limiter

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [ 
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event('startup')
# async def startup():
#     await FastAPILimiter.init(auth_service.r)

@app.middleware("http")
async def log_requests(request, call_next):
    ic(f"Request: {request.method} - {request.url}")
    response = await call_next(request)
    return response

@app.middleware("http")
async def log_errors(request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        ic(f"Error: {e}")
        raise

from src.routes.email import router as email_router
from src.routes.auth import router as auth_router
from src.routes.contacts import router as contacts_router

app.include_router(email_router, prefix='/api')
app.include_router(contacts_router, prefix='/api')
app.include_router(auth_router, prefix='/api')

# @app.get('/', dependencies=[Depends(RateLimiter(times=2, seconds=5))])
@app.get('/')
@limiter.limit("5/minute")
def read_root(request: Request):
    return {'message': 'It works!'}

if __name__ == '__main__':
    ic('WTF')
    uvicorn.run('main:app', port=8000, reload=True)