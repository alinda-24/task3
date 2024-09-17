# shared-workflows/scripts/adversarial_review.py

import os
import re
import sys
import subprocess
import openai  # Corrected import

def main(api_key, task_file, solution_dir):
    if not api_key:
        print("Error: OpenAI API key is missing.", file=sys.stderr)
        sys.exit(1)

    # Set the OpenAI API key
    openai.api_key = api_key

    # Read the task description
    try:
        with open(task_file, "r") as file:
            task_description = file.read()
    except FileNotFoundError:
        print("Error: Task description file not found.", file=sys.stderr)
        sys.exit(1)

    # Read the existing solution files in the solution directory
    solution_files = []
    try:
        for filename in os.listdir(solution_dir):
            if filename.endswith(".java"):
                with open(os.path.join(solution_dir, filename), "r") as file:
                    solution_files.append(file.read())
    except FileNotFoundError:
        print(f"Error: Solution directory '{solution_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    if not solution_files:
        print(f"Error: No Java solution files found in '{solution_dir}'.", file=sys.stderr)
        sys.exit(1)

    solution_content = "\n\n".join(solution_files)

    # Prompt to improve the solution
    prompt = (
        f"Given the following task description and solution code, analyze the solution and improve it. "
        f"Correct any issues or missing requirements that might be present in the solution.\n\n"
        f"### Task Description\n{task_description}\n\n"
        f"### Current Solution\n{solution_content}\n\n"
        "IMPORTANT: Provide an improved version of the solution with corrections, if necessary, and ensure that the updated code is complete and functional. "
        "Check for missing imports, misplaced code, and correct all invalid or incomplete class definitions. "
        "Ensure all methods are correctly implemented, all imports are included, and the solution can be compiled and run without errors. "
        "The response must be in plain Java code with no markdown formatting or ```java blocks."
    )

    # Generate the improved solution
    improved_solution = generate_with_retries(prompt, max_retries=3)
    if improved_solution is None:
        print("Error: Failed to generate improved solution after multiple retries.", file=sys.stderr)
        sys.exit(1)

    # Ensure the solution directory exists
    os.makedirs(solution_dir, exist_ok=True)

    # Save existing solution files' content for diff
    existing_solution_content = "\n\n".join(solution_files)

    # Write the improved solution to the solution files
    write_improved_solution(solution_dir, improved_solution)

    # Fetch the diff summary
    try:
        diff_summary = get_diff_summary()
    except Exception as e:
        print(f"Error obtaining diff summary: {e}", file=sys.stderr)
        sys.exit(1)

    # Commit and push changes with the diff summary in commit message
    commit_and_push_changes(diff_summary)

def generate_with_retries(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-2024-08-06",  # Replace with the correct model name if needed
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating improved solution: {e}", file=sys.stderr)
            if attempt < max_retries - 1:
                print("Retrying...", file=sys.stderr)
    return None

def write_improved_solution(directory, improved_solution):
    """Overwrite the existing solution files with the improved solution."""
    # Split the improved solution by class definitions
    class_blocks = re.findall(r'(public\s+class\s+\w+\s*{[\s\S]*?})', improved_solution)

    if not class_blocks:
        # Fallback: assume single class
        class_blocks = [improved_solution]

    for block in class_blocks:
        # Extract class name
        class_name_match = re.search(r'public\s+class\s+(\w+)\s*{', block)
        if class_name_match:
            class_name = class_name_match.group(1)
        else:
            print(f"Skipping block due to missing class name: {block[:50]}", file=sys.stderr)
            continue

        # Define the file name
        file_name = f"{class_name}.java"
        file_path = os.path.join(directory, file_name)

        # Write the improved code to the file
        try:
            with open(file_path, "w") as file:
                file.write(block)
            print(f"Successfully wrote {file_name}")
        except IOError as e:
            print(f"Error writing file {file_name}: {e}", file=sys.stderr)

def get_diff_summary():
    """Get a summary of changes using git diff --stat."""
    try:
        # Ensure that git is aware of the changes
        subprocess.run(["git", "add", "."], check=True)
        # Get the diff summary
        result = subprocess.run(
            ["git", "diff", "--staged", "--stat"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        diff_summary = result.stdout.strip()
        return diff_summary
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff summary: {e.stderr}", file=sys.stderr)
        raise e

def commit_and_push_changes(diff_summary):
    """Commit and push the changes with the diff summary in the commit message."""
    try:
        # Configure git user
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        # Commit changes with diff summary
        commit_message = f"Adversarial Review: Improve solution\n\nChanges:\n{diff_summary}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push changes
        subprocess.run(
            ["git", "push", "origin"],
            check=True,
            env={
                **os.environ,
                "GIT_ASKPASS": "echo",
                "GIT_USERNAME": "x-access-token",
                "GIT_PASSWORD": os.getenv('GITHUB_TOKEN')
            }
        )
        print("Successfully committed and pushed changes.")
    except subprocess.CalledProcessError as e:
        print(f"Error committing and pushing changes: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error: Missing required command line arguments 'api_key', 'task_file', and 'solution_dir'", file=sys.stderr)
        sys.exit(1)

    api_key = sys.argv[1]
    task_file = sys.argv[2]
    solution_dir = sys.argv[3]

    main(api_key, task_file, solution_dir)
