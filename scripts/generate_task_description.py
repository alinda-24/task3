import os
import sys
import subprocess
from datetime import datetime
import openai  # Correct import
import pytz
from pytz import timezone

def main(api_key):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    # Set the OpenAI API key
    openai.api_key = api_key

    # Extract theme and language from environment variables
    theme = os.getenv("TASK_THEME", "Create a basic Java application with the following requirements.")
    language = os.getenv("TASK_LANGUAGE", "English")

    # Combine theme into a single prompt
    learning_goals = """
    * Designing Java classes
    * Adding instance fields
    * Adding a constructor method
    * Creating getters and setters
    * Printing to the terminal
    * Using the `main` method
    * Scope (or variable shadowing)

    """

    original_structure = """
    # Is this a Triangle?

    The following assignment is about geometry: rectangles and triangles modeled with Java! You are going to make decisions using `if` and `else` statements and be introduced to the *triangle inequality*.

    ### 👨🏽‍🏫 Instructions
    For instructions on how to do and submit the assignment, please see the [assignments section of the course instructions](https://gits-15.sys.kth.se/inda-23/course-instructions#assignments).

    ### 📝 Preparation
    - Read and answer all questions in Module 3: [Branching](https://qbl.sys.kth.se/sections/dd1337_ht23_programmering_prog/container/branching)
    - You can access the OLI material both:
      - via Canvas (see the [OLI Torus SE](https://canvas.kth.se/courses/41415/external_tools/4247) link in the left menu)
      - or directly at this [webpage](https://qbl.sys.kth.se/sections/dd1337_ht23_programmering_prog/container/dd1337__programming)

    ### ✅ Learning Goals

    * Branching (`if` and `else` statements)
    * Access object fields and methods with dot-notation
    * Using the Java Math Library

    ### 🏛 Assignment

    #### Exercise 3.0 -- A Triangle Object
    Create a new class called `Triangle.java` in the [src](src/) directory.
    The triangle class should have three fields of type `int` -- the sides `a`, `b`, and `c`. Add a constructor that takes one parameter per side of the triangle, setting each side's value to the corresponding parameter.
    The main method of the example below should compile if implemented correctly.

    <details>
      <summary> 🛠 Main method example </summary>

      ```Java
      public static void main(String[] args){
        Triangle triangle = new Triangle(3, 1, 1);
      }
      ```
    </details>

    #### Exercise 3.1 -- The Triangle Inequality
    Create a method in the `Triangle` class with the header `private boolean validTriangle(int a, int b, int c)` that returns `true` if the parameters can construct the sides of a triangle, and `false` otherwise.
    You also want to handle invalid input, making sure that a triangle object is created *iff* the parameters are valid.

    <details>
    <summary> 📚 What are Exceptions? </summary>
    Learn about exceptions in Java, such as `IllegalArgumentException`, which can help you manage invalid inputs.
    </details>

    #### Exercise 3.2 -- The three types of Triangles
    Make a method in the `Triangle` class called `String getTriangleType()` that returns a `String` of what type the triangle is (*"Equilateral"*, *"Isosceles"* or *"Scalene"*).

    #### Exercise 3.3 -- `Triangle.getArea()`
    Use Heron's Formula to calculate the area of the triangle. Create a `getArea()` method that returns the area as a `double`.

    #### Exercise 3.4 -- Reverse Engineering
    Create a `Rectangle` class by reverse-engineering the example in `RectangleExample.java`.

    #### Exercise 3.5 -- Returning a boolean expression
    Improve your code by using direct return statements for boolean expressions.

    ### ❎ Checklist

    - [ ] Create a Triangle class
    - [ ] Create a method to classify the triangle
    - [ ] Calculate the triangle's area
    - [ ] Create the Rectangle class
    - [ ] Improve your code by using direct return statements.
    """

    prompt = (
        f"Create a new programming task in {language} with the following theme: {theme}. "
        f"It is paramount that the generated task description includes and integrates the concepts of {learning_goals}"
        f"The task should follow a similar structure and format to the provided example {original_structure}, including detailed instructions, preparation steps, learning goals, and assignment description with exercises. "
        f"Make sure to include the title, subtitle, and emojis for aesthetics. "
        f"The description should be detailed, well-structured, and aesthetically pleasing to provide thorough instructions for the students."
    )

    # Call OpenAI API to generate the task description
    response_content = generate_with_retries(prompt, max_retries=3)
    if response_content is None:
        print("Error: Failed to generate task description after multiple retries.")
        sys.exit(1)

    # Create a new branch with a unique name
    stockholm_tz = timezone('Europe/Stockholm')
    branch_name = f"task-{datetime.now(stockholm_tz).strftime('%Y%m%d%H%M%S')}"
    create_branch(branch_name)

    # Ensure the 'tasks' directory exists
    tasks_dir = "tasks"
    os.makedirs(tasks_dir, exist_ok=True)

    # Write the response content to a markdown file
    task_file_path = os.path.join(tasks_dir, "new_task.md")
    with open(task_file_path, "w") as file:
        file.write(response_content)

    # Commit and push changes
    commit_and_push_changes(branch_name, task_file_path)

    # Output the branch name for the next job
    print(f"branch_name={branch_name}", file=sys.stdout)

def generate_with_retries(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating task description: {e}", file=sys.stderr)
            if attempt < max_retries - 1:
                print("Retrying...", file=sys.stderr)
    return None

def create_branch(branch_name):
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(
            [
                "git", "push", "-u", "origin", branch_name
            ],
            check=True,
            env={
                **os.environ,
                "GIT_ASKPASS": "echo",
                "GIT_USERNAME": "x-access-token",
                "GIT_PASSWORD": os.getenv('GITHUB_TOKEN')
            }
        )
    except subprocess.CalledProcessError as e:
        print(f"Error creating branch: {e}", file=sys.stderr)
        sys.exit(1)

def commit_and_push_changes(branch_name, task_file_path):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        subprocess.run(["git", "add", task_file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"Add new task description: {branch_name}"], check=True)
        subprocess.run(
            [
                "git", "push", "--set-upstream", "origin", branch_name
            ],
            check=True,
            env={
                **os.environ,
                "GIT_ASKPASS": "echo",
                "GIT_USERNAME": "x-access-token",
                "GIT_PASSWORD": os.getenv('GITHUB_TOKEN')
            }
        )
    except subprocess.CalledProcessError as e:
        print(f"Error committing and pushing changes: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: Missing required command line arguments 'api_key' and 'branch_name'", file=sys.stderr)
        sys.exit(1)

    api_key = sys.argv[1]
    branch_name = sys.argv[2]

    main(api_key, branch_name)
