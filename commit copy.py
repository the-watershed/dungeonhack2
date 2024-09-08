import subprocess
import sys

def run_command(commaupdatend):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(result.returncode)
    return result.stdout
20
def main():
    commit_message = input("Enter commit message: ")

    # Add all changes
    print("Adding changes...")
    run_command("git add .")

    # Commit changes
    print("Committing changes...")
    run_command(f'git commit -m "{commit_message}"')

    # Push changes
    print("Pushing changes...")
    run_command("git push")

    print("Changes committed and pushed successfully.")

if __name__ == "__main__":
    main()