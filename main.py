# todo: create issue bot app
import os

import uvicorn
from github import Github, GithubIntegration
from github import Auth

GITHUB_APP_ID = 1552123

from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()


@app.get("/")
async def read_root():
    deployment = os.getenv("DEPLOYMENT")
    if deployment == "LOCAL":
        from secrets_ import PRIVATE_KEY
        auth = Auth.AppAuth(GITHUB_APP_ID, PRIVATE_KEY)
    elif deployment == "DEV":
        from azure.identity import ManagedIdentityCredential
        token = ManagedIdentityCredential().get_token().token
        auth = Auth.AppAuthToken(token)
    elif deployment == "LOCAL_USER_TOKEN":
        from secrets_ import TOKEN
        auth = Auth.Token(TOKEN)
        g = Github(auth=auth)
        for repo in g.get_user().get_repos():
            print(repo.name)
            print(repo.create_issue(title="App created issue"))
    else:
        raise Exception("'DEPLOYMENT' env variable must be set!")

    if deployment != "LOCAL_USER_TOKEN":
        g = GithubIntegration(auth=auth)
        inst = g.get_installations()[0]
        for repo in inst.get_repos():
            print(repo.name)
            print(repo.create_issue(title=f"App created issue. {deployment}"))

    # To close connections after use
    g.close()
    return {"Hello": "World created issue"}


@app.post("/")
async def read_response(request: Request):
    req = await request.json()
    print(req['action'])


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
