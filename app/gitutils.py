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

def get_tree(repo_dir, repo_name, commit_hash, tree_path=""):
    path = os.path.join(repo_dir, repo_name + ".git")
    if not os.path.exists(path):
        return []

    tree_path = tree_path.strip("/")
    tree_ref = commit_hash if tree_path == "" else f"{commit_hash}:{tree_path}"

    try:
        output = subprocess.check_output(
            ["git", "--git-dir", path, "ls-tree", tree_ref],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError:
        return []

    entries = []
    for line in output.strip().split("\n"):
        if not line:
            continue
        meta, name = line.split("\t", 1)
        parts = meta.split()
        if len(parts) < 2:
            continue
        entry_type = parts[1]
        entry_path = f"{tree_path}/{name}" if tree_path else name
        entries.append({
            "name": name,
            "path": entry_path,
            "type": entry_type,
        })

    entries.sort(key=lambda e: (e["type"] != "tree", e["name"].lower()))
    return entries

def get_file_content(repo_dir, repo_name, commit_hash, file_path):
    path = os.path.join(repo_dir, repo_name + ".git")
    if not os.path.exists(path):
        return ""

    file_ref = f"{commit_hash}:{file_path}"

    try:
        output = subprocess.check_output(
            ["git", "--git-dir", path, "show", file_ref],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError:
        return ""

    return output