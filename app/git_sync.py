import os
import subprocess

LOCAL_DIR = "./repos"
SERVER = "git@balam"

def list_remote_repos():
    """Return list of (repo_name, remote_path) tuples."""
    output = subprocess.check_output(
        ["ssh", SERVER, "ls -1 ~/*.git"],
        universal_newlines=True
    )
    repos = []
    for line in output.strip().split("\n"):
        line = line.strip()  # remove trailing/leading spaces
        #print(f"Remote line: {line}")
        # get only .git lines
        if not line.endswith(".git:"):
            continue
        name = os.path.basename(line)[:-5]  # remove .git:
        print(f"Repo name: {name}")
        repos.append((name, line[:-1]))  # remove trailing colon
    return repos


def sync_repos():
    os.makedirs(LOCAL_DIR, exist_ok=True)
    print("[*] Syncing repositories...")
    #print(list_remote_repos())
    #return
    for name, remote_path in list_remote_repos():
        local_path = os.path.join(LOCAL_DIR, f"{name}.git")
        if os.path.exists(local_path):
            head_file = os.path.join(local_path, "HEAD")
            if os.path.exists(head_file):
                print(f"[+] Fetching updates for {name}...")
                subprocess.run(
                    ["git", "--git-dir", local_path, "fetch", "--all"],
                    check=True
                )
            else:
                print(f"[!] Local path exists but is not a git repo. Re-cloning {name}...")
                subprocess.run(["rm", "-rf", local_path])
                subprocess.run(
                    ["git", "clone", "--mirror", f"{SERVER}:{remote_path}", local_path],
                    check=True
                )
        else:
            print(f"[+] Cloning new repo {name}...")
            subprocess.run(
                ["git", "clone", "--mirror", f"{SERVER}:{remote_path}", local_path],
                check=True
            )

    print("[✓] All repos synced!")
    print("Starting server at http://0.0.0.0:8000")
    # post the link so the user can see it
    print('\x1b]8;;http://localhost:8000/\x1b\\Click here\x1b]8;;\x1b\\')   


if __name__ == "__main__":
    sync_repos()
