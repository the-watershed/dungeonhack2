import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        exit(1)
    return result.stdout

def main():
    branch_name = input("Enter the new branch name: ")

    # Step 1: Create a new branch
    run_command(f"git checkout -b {branch_name}")
    print(f"Created and switched to branch '{branch_name}'")

    # Step 2: Add all files to the branch
    run_command("git add .")
    print("Added all files to the staging area")

    # Step 3: Commit the changes
    commit_message = f"Initial commit on branch {branch_name}"
    run_command(f"git commit -m \"{commit_message}\"")
    print(f"Committed changes with message: '{commit_message}'")

if __name__ == "__main__":
    main()