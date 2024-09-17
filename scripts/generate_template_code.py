import os
import sys
import subprocess
from openai import OpenAI

def main(api_key, branch_name):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Read the existing solution code from .hidden_tasks directory
    solution_dir = ".hidden_tasks"
    solution_files = []
    try:
        for filename in os.listdir(solution_dir):
            if filename.endswith(".java"):
                with open(os.path.join(solution_dir, filename), "r") as file:
                    solution_files.append((filename, file.read()))
    except FileNotFoundError:
        print("Error: Solution files not found in .hidden_tasks directory.")
        sys.exit(1)

    if not solution_files:
        print("Error: No Java solution files found in .hidden_tasks.")
        sys.exit(1)

    # Generate a template from the solution for each file
    for filename, solution_content in solution_files:
        template_content = generate_template_from_solution(solution_content)

        # Review the generated template using OpenAI API
        reviewed_template = review_template_with_openai(client, template_content)

        # Write the final reviewed template to gen_src directory
        gen_src_dir = "gen_src"
        os.makedirs(gen_src_dir, exist_ok=True)
        file_path = os.path.join(gen_src_dir, filename)

        try:
            with open(file_path, "w") as template_file:
                template_file.write(reviewed_template)
            print(f"Successfully created and reviewed template for {filename}")
        except IOError as e:
            print(f"Error writing file {filename}: {e}")

    # Commit and push changes
    commit_and_push_changes(branch_name, gen_src_dir)

def generate_template_from_solution(solution_content):
    """
    Simplifies the solution code to create a student template by removing method bodies
    and complex logic while keeping method signatures and class structures intact.
    """
    template_lines = []
    in_method_body = False

    for line in solution_content.splitlines():
        stripped_line = line.strip()

        # Detect the start of a method (i.e., a line ending with '{')
        if stripped_line.endswith("{") and not stripped_line.startswith("class"):
            template_lines.append(line)  # Keep the method signature
            in_method_body = True  # Enter method body, which will be removed
        elif in_method_body:
            # Detect the end of a method (a single '}')
            if stripped_line == "}":
                template_lines.append(line)  # Keep the closing brace
                in_method_body = False  # Exit method body
            # Replace method body with a TODO placeholder
            else:
                if "return" in stripped_line:
                    # Retain return types for completeness
                    template_lines.append("    // TODO: Implement logic and return the appropriate value.")
                else:
                    template_lines.append("    // TODO: Implement this method.")
        else:
            template_lines.append(line)  # Keep the rest of the class structure intact

    return "\n".join(template_lines)

def review_template_with_openai(client, template_content):
    """
    Uses the OpenAI API to review the generated template and make any final adjustments.
    """
    prompt = (
        f"This is a code template for students to solve your job is to review it to make sure it is structurally correct."
        f"Review the following Java code template, generated for students to fill in the missing parts. "
        f"Ensure that the structure is correct, no methods are missing, and the placeholders for implementation are clear. "
        f"Make sure that imports, method signatures, and class structures are properly defined. "
        f"Do not provide any additional implementation, but adjust any formatting or structure issues.\n\n"
        f"### Template Code:\n{template_content}\n\n"
        "IMPORTANT: Provide a revised version of the template that ensures all structures are complete."
        "IMPORTANT: The response must be plain Java code with no markdown formatting or ```java blocks. Ensure that the response is ready to be saved directly as a .java file."
        "DO NOT INCLUDE ANY TEXT int the code files except for the potential comments."
    )

    reviewed_template = generate_with_retries(client, prompt, max_retries=3)
    return reviewed_template if reviewed_template else template_content

def generate_with_retries(client, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    return None

def commit_and_push_changes(branch_name, directory_path):
    if not branch_name:
        print("Error: Branch name is empty.")
        sys.exit(1)

    try:
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        # Fetch the latest changes from the remote
        subprocess.run(["git", "fetch", "origin"], check=True)
        
        # Check if there are new changes on the remote branch
        subprocess.run(["git", "pull", "origin", branch_name], check=True)

        # Stage changes and commit
        subprocess.run(["git", "add", directory_path], check=True)
        subprocess.run(["git", "commit", "-m", "Add generated template"], check=True)
        
        # Push the changes
        subprocess.run(
            ["git", "push", "--set-upstream", "origin", branch_name],
            check=True,
            env=dict(os.environ, GIT_ASKPASS='echo', GIT_USERNAME='x-access-token', GIT_PASSWORD=os.getenv('GITHUB_TOKEN'))
        )
    except subprocess.CalledProcessError as e:
        print(f"Error committing and pushing changes: {e}")
        sys.exit(1)

if len(sys.argv) != 3:
    print("Error: Missing required command line arguments 'api_key' and 'branch_name'")
    sys.exit(1)

api_key = sys.argv[1]
branch_name = sys.argv[2]

main(api_key, branch_name)
