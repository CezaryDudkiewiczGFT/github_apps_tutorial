from fastapi import FastAPI
from starlette.requests import Request

from main import main

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/")
async def read_response(request: Request):
    req = await request.json()
    print(req['action'])


main()
