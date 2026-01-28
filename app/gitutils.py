import os
import subprocess

def list_repos(repo_dir):
    if not os.path.exists(repo_dir):
        return []

    repos = []
    for name in os.listdir(repo_dir):
        if name.endswith(".git"):
            repos.append(name[:-4])

    return sorted(repos)

def get_commits(repo_dir, repo_name, n=10):
    path = os.path.join(repo_dir, repo_name + ".git")
    if not os.path.exists(path):
        return []

    try:
        output = subprocess.check_output(
            ["git", "--git-dir", path, "log", f"--pretty=format: %h|%s", f"-n{n}"],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError:
        return []

    commits = []
    for line in output.strip().split("\n"):
        if "|" in line:
            h, msg = line.split("|", 1)
            commits.append({"hash": h, "message": msg})
    
    return commits

def get_files(repo_dir, repo_name, commit_hash):
    path = os.path.join(repo_dir, repo_name + ".git")
    if not os.path.exists(path):
        return []

    try:
        output = subprocess.check_output(
            ["git", "--git-dir", path, "ls-tree", "--name-only", "-r", commit_hash],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError:
        return []

    files = output.strip().split("\n")
    return files