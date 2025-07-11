# todo: create issue bot app
import os

import uvicorn
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from github import Github, GithubIntegration
from github import Auth
from azure.keyvault.secrets import SecretClient

from utils import create_logger
GITHUB_APP_ID = 1552123

from fastapi import FastAPI
from starlette.requests import Request

logger = create_logger()

logger.info("Creating APP")
app = FastAPI()


@app.get("/")
async def read_root():
    logger.info("!!!!!!!!!!!!!!!!!!Trying to create an issue!!!!!!!!!!!!!!!!!!!")
    deployment = os.getenv("DEPLOYMENT")
    if deployment == "LOCAL":
        from secrets_ import PRIVATE_KEY
        auth = Auth.AppAuth(GITHUB_APP_ID, PRIVATE_KEY)
    elif deployment == "DEV":
        try:
            print("MI")
            credentials = ManagedIdentityCredential()
            print("Trying to start sc")
            sc = SecretClient("https://gh-key-vaultt.vault.azure.net/", credentials)
        except:
            print("default")
            credentials = DefaultAzureCredential()
            sc = SecretClient("https://gh-key-vaultt.vault.azure.net/", credentials)
        print("Getting key from kv")
        private_key = sc.get_secret("gh-key")
        print("creating auth")
        auth = Auth.AppAuth(GITHUB_APP_ID, private_key.value)
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
    print("Handling response from github:")
    req = await request.json()
    print(f"Request['action']: {req['action']}")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
