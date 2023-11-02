from fastapi import FastAPI
from icecream import ic
from src.routes import contacts, auth

# alembic revision --autogenerate -m 'Init'
# alembic upgrade head

# uvicorn main:app --host localhost --port 8000 --reload

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

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

@app.get('/')
def read_root():
    return {'message': 'It works!'}