import os
import subprocess
import requests

# Step 1: Check if Git is installed
def check_git_installed():
    try:
        subprocess.run(["git", "--version"], check=True)
    except subprocess.CalledProcessError:
        print("Git is not installed. Please install Git and try again.")
        exit(1)

# Step 2: Initialize a Git repository
def initialize_git_repo():
    subprocess.run(["git", "init"], check=True)

# Step 3: Create a new repository on GitHub
def create_github_repo(repo_name, github_token):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False  # Change to True if you want a private repository
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Successfully created repository {repo_name} on GitHub.")
        return response.json()["clone_url"]
    else:
        print(f"Failed to create repository: {response.json()}")
        exit(1)

# Step 4: Add the remote repository
def add_remote_repo(remote_url):
    subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)

# Step 5: Commit and push the code
def commit_and_push():
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

def main():
    repo_name = input("Enter the new GitHub repository name: ")
    github_token = input("Enter your GitHub personal access token: ")

    check_git_installed()
    initialize_git_repo()
    remote_url = create_github_repo(repo_name, github_token)
    add_remote_repo(remote_url)
    commit_and_push()

if __name__ == "__main__":
    main()