from fastapi import FastAPI, Depends
from icecream import ic
from src.routes import contacts, auth, email

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware

from src.services.auth import auth_service

import uvicorn

# alembic revision --autogenerate -m 'Init'
# alembic upgrade head

# docker-compose up -d
# docker exec -it dcb9d sh
# icacls "C:\Users\Professional\Documents\GitHub\RestAPI\.postgres-data" /grant Professional:(OI)(CI)F /T
# uvicorn main:app --host localhost --port 8000 --reload

app = FastAPI()

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

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(email.router, prefix='/api')

@app.on_event('startup')
async def startup():
    await FastAPILimiter.init(auth_service.r)

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

@app.get('/', dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def read_root():
    return {'message': 'It works!'}

if __name__ == '__main__':
    ic('WTF')
    uvicorn.run('main:app', port=8000, reload=True)