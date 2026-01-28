from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .gitutils import list_repos, get_commits, get_files
from .git_sync import sync_repos

import uvicorn

app = FastAPI()
sync_repos()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

REPO_DIR = "./repos"
SERVER = "git@balam"

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    repos = list_repos(REPO_DIR)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "repos": repos,
        },
    )

@app.get("/repo/{repo_name}", response_class=HTMLResponse)
def view_repo(request: Request, repo_name: str):
    repos = list_repos(REPO_DIR)
    if repo_name not in repos:
        return HTMLResponse(content="Repository not found", status_code=404)

    commits = get_commits(REPO_DIR, repo_name, n=10) if repos else []
    files = get_files(REPO_DIR, repo_name, commits[0]["hash"]) if commits else []
    return templates.TemplateResponse(
        "repo.html",
        {
            "request": request,
            "repo_name": repo_name,
            "commits": commits,
            "files": files,
        },
    )

@app.get("/repos", response_class=HTMLResponse)
def ping():
    return {"repos": list_repos(REPO_DIR)}

