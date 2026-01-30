import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .gitutils import list_repos, get_commits, get_tree
from .git_sync import sync_repos

import uvicorn
from .gitutils import get_file_content

LANGUAGE_BY_EXTENSION = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "javascript",
    ".tsx": "typescript",
    ".json": "json",
    ".html": "xml",
    ".htm": "xml",
    ".css": "css",
    ".md": "markdown",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".toml": "ini",
    ".ini": "ini",
    ".cfg": "ini",
    ".xml": "xml",
    ".java": "java",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
}

def detect_language(file_path: str) -> str:
    _, ext = os.path.splitext(file_path.lower())
    return LANGUAGE_BY_EXTENSION.get(ext, "plaintext")

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
    entries = get_tree(REPO_DIR, repo_name, commits[0]["hash"], "") if commits else []
    return templates.TemplateResponse(
        "repo.html",
        {
            "request": request,
            "repo_name": repo_name,
            "commits": commits,
            "entries": entries,
            "tree_path": "",
        },
    )

@app.get("/repo/{repo_name}/tree/{tree_path:path}", response_class=HTMLResponse)
def view_repo_tree(request: Request, repo_name: str, tree_path: str):
    repos = list_repos(REPO_DIR)
    if repo_name not in repos:
        return HTMLResponse(content="Repository not found", status_code=404)

    commits = get_commits(REPO_DIR, repo_name, n=10) if repos else []
    if not commits:
        return HTMLResponse(content="No commits found", status_code=404)

    entries = get_tree(REPO_DIR, repo_name, commits[0]["hash"], tree_path)
    return templates.TemplateResponse(
        "repo.html",
        {
            "request": request,
            "repo_name": repo_name,
            "commits": commits,
            "entries": entries,
            "tree_path": tree_path.strip("/"),
        },
    )

@app.get("/repo/{repo_name}/file/{file_path:path}", response_class=HTMLResponse)
def view_file(request: Request, repo_name: str, file_path: str):
    repos = list_repos(REPO_DIR)
    if repo_name not in repos:
        return HTMLResponse(content="Repository not found", status_code=404)

    commits = get_commits(REPO_DIR, repo_name, n=10) if repos else []
    if not commits:
        return HTMLResponse(content="No commits found", status_code=404)

    content = get_file_content(REPO_DIR, repo_name, commits[0]["hash"], file_path)
    if not content:
        return HTMLResponse(content="File not found", status_code=404)

    language = detect_language(file_path)
    
    return templates.TemplateResponse(
        "file.html",
        {
            "request": request,
            "repo_name": repo_name,
            "file_path": file_path,
            "content": content,
            "commits": commits,
            "file_content": content,
            "language": language,
        },
    )


@app.get("/repos", response_class=HTMLResponse)
def ping():
    return {"repos": list_repos(REPO_DIR)}

