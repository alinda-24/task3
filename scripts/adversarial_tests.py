# shared-workflows/scripts/adversarial_tests.py

import os
import re
import sys
import subprocess
import openai  # Corrected import

def main(api_key, test_dir):
    if not api_key:
        print("Error: OpenAI API key is missing.", file=sys.stderr)
        sys.exit(1)

    # Set the OpenAI API key
    openai.api_key = api_key

    # Read all test files in the test directory
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.java')]
    
    if not test_files:
        print(f"Error: No Java test files found in '{test_dir}'.", file=sys.stderr)
        sys.exit(1)
    
    for test_file in test_files:
        test_file_path = os.path.join(test_dir, test_file)
        
        with open(test_file_path, "r") as file:
            test_content = file.read()

        # Send the test content to OpenAI for adversarial review and improvement
        improved_content = adversarial_review(test_content)

        if improved_content is None:
            print(f"Error: Failed to generate improved test code for {test_file} after multiple retries.", file=sys.stderr)
            continue  # Skip to the next file

        # Save the improved test content
        with open(test_file_path, "w") as file:
            file.write(improved_content)
        
        print(f"Adversarial review completed for: {test_file}")
    
    # After all tests are improved, commit and push changes with a summary
    commit_and_push_changes(test_dir)

def adversarial_review(test_content):
    # Prepare a prompt that asks OpenAI to review the test file
    prompt = (
        "Review the following Java test code and make necessary improvements to ensure it is well-structured, follows proper test practices, "
        "and can be executed without issues. Make sure that there are no extraneous content like markdown blocks or incomplete class definitions. "
        "Ensure that imports, method names, and test annotations are correct. If there are unfinished or misplaced code sections, clean them up "
        "to make the test files function properly:\n\n"
        f"### Test Code:\n{test_content}\n\n"
        "IMPORTANT: Do not include markdown code blocks (` ``` `) in your response. Ensure that all test classes are properly structured and can be executed."
    )

    # Generate the improved test code
    improved_content = generate_with_retries(prompt, max_retries=3)
    
    if improved_content:
        improved_content = clean_up_test_code(improved_content)
    
    return improved_content

def generate_with_retries(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Replace with the correct model name if needed
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating improved test code: {e}", file=sys.stderr)
            if attempt < max_retries - 1:
                print("Retrying...", file=sys.stderr)
    return None

def clean_up_test_code(test_code):
    """
    Clean up the improved test code by removing markdown formatting, ensuring balanced braces,
    and removing any extraneous content.
    """
    # Remove any markdown-like blocks (```java, ``` etc.)
    test_code = re.sub(r'```[\w]*', '', test_code)

    # Remove any misplaced file declarations (e.g., "Enemy.java:" or "Player.java:")
    test_code = re.sub(r'\w+\.java:', '', test_code)

    # Ensure that there are no unclosed curly braces
    open_braces = test_code.count('{')
    close_braces = test_code.count('}')
    if open_braces > close_braces:
        test_code += '}' * (open_braces - close_braces)

    # Remove extraneous or repeated imports, if any
    test_code = clean_up_imports(test_code)

    return test_code

def clean_up_imports(test_code):
    """
    Remove duplicate imports and ensure necessary imports are present.
    """
    # Define required imports based on common Java testing classes
    required_imports = {
        "Before": "import org.junit.Before;",
        "Test": "import org.junit.Test;",
        "Assert": "import static org.junit.Assert.*;",
    }

    # Extract existing imports from the test code
    existing_imports = re.findall(r'^\s*import .*;', test_code, re.MULTILINE)

    # Add missing imports
    imports_to_add = []
    for class_name, import_statement in required_imports.items():
        if class_name in test_code and import_statement not in existing_imports:
            imports_to_add.append(import_statement)

    # Remove duplicate imports
    unique_imports = list(set(existing_imports))

    # Prepend missing imports at the start of the test code
    if imports_to_add:
        unique_imports.extend(imports_to_add)

    # Reconstruct the imports section
    imports_section = "\n".join(sorted(unique_imports)) + "\n\n"

    # Remove existing imports from the test code
    test_code = re.sub(r'^\s*import .*;\n', '', test_code, flags=re.MULTILINE)

    # Prepend the imports section
    test_code = imports_section + test_code

    return test_code

def commit_and_push_changes(test_dir):
    """
    Commit and push the changes made to the test files with a summary of changes.
    """
    try:
        # Stage the changes in the test directory
        subprocess.run(["git", "add", test_dir], check=True)

        # Get a summary of the changes
        diff_summary = subprocess.run(
            ["git", "diff", "--cached", "--stat"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdout.strip()

        if not diff_summary:
            print("No changes to commit.", file=sys.stderr)
            return

        # Configure git user
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        # Commit the changes with the diff summary in the commit message
        commit_message = f"Adversarial Review: Improve Tests\n\nChanges:\n{diff_summary}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes
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

        print("Successfully committed and pushed improved tests.")
    except subprocess.CalledProcessError as e:
        print(f"Error committing and pushing changes: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: Missing required command line arguments 'api_key' and 'test_dir'", file=sys.stderr)
        sys.exit(1)

    api_key = sys.argv[1]
    test_dir = sys.argv[2]

    main(api_key, test_dir)
