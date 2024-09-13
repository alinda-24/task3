import os
import re
import sys
import subprocess
from openai import OpenAI

def main(api_key, branch_name):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Read the new task description
    try:
        with open("tasks/new_task.md", "r") as file:
            task_description = file.read()
    except FileNotFoundError:
        print("Error: new_task.md file not found.")
        sys.exit(1)

    # Inspirational code snippet for the solution
    inspirational_code = """

        "/**
        * A class representing a rectangle with some common operations and properites.
        * Example solution for exercise 3.0
        */
        public class Rectangle {
            private int width;
            private int height;

            public void setWidth(int width) {
                this.width = width;
            }

            public void setHeight(int height) {
                this.height = height;
            }

            public int getWidth() {
                return width;
            }

            public int getHeight() {
                return height;
            }

            /**
            * Calculates the area of the rectangle
            * @return the area of the rectangle
            */
            public int area() {
                return width * height;
            }

            /**
            *  Get the diagonal length of the rectangle
            *  @return the diagonal length of the rectangle
            */
            public double diagonalLength() {
                return Math.sqrt(width * width + height * height);
            }

            /**
            *  Check wether this rectangle is a square
            *  @return true if the rectangle is a square, false otherwise
            */
            public boolean isSquare() {
                return width == height;
            }
        }"



        "public class RectangleExample {

            public static void main(String[] args) {
                System.out.println("Creating a rectangle with side lengths 40 and 50");
                Rectangle rectangle = new Rectangle();
                rectangle.setWidth(40);
                rectangle.setHeight(50);

                System.out.println("The area of the rectangle is " + rectangle.area());
                System.out.println("(The correct area is 2000)\n");

                System.out.println("The diagonal length of the rectangle is " + rectangle.diagonalLength());
                System.out.println("(The correct diagonal length is approximately 64.03)\n");

                System.out.println("Is the rectangle a square? " + rectangle.isSquare());
                System.out.println("(The correct answer should be false)\n");

                System.out.println("------------------------------------------------");
                System.out.println("Creating a square with side lenth 20");
                Rectangle square = new Rectangle();
                square.setWidth(20);
                square.setHeight(20);

                System.out.println("The area of the square is " + square.area());
                System.out.println("(The correct area is 400)\n");

                System.out.println("The diagonal length of the square is " + square.diagonalLength());
                System.out.println("(The correct diagonal length is approximately 28.28)\n");

                System.out.println("Is the square a square? " + square.isSquare());
                System.out.println("(The correct answer should be true)\n");
            }

        }"

        "

            /**
            * A class representing a triangle with some common operations.
            * Example solution for exercises 3.1 - 3.3
            */
            public class Triangle {
                // The side lengths of the triangles
                int a, b, c;

                /**
                * Construct a triangle with side lengths a, b, and c
                * @param a length of a side
                * @param b length of a side
                * @param c length of a side
                */
                public Triangle(int a, int b, int c) {
                    if (validTriangle(a, b, c)) {
                        this.a = a;
                        this.b = b;
                        this.c = c;
                    } else {
                        // this end the program with an error
                        throw new IllegalArgumentException();
                    }
                }

                /**
                * Decides whether the side lenghts a, b, and c can form a valid triangle,
                * by checking if the conform to the triangle inequality.
                * @param a a side length of the triangle
                * @param b a side length of the triangle
                * @param c a side length of the triangle
                * @return true if the sides can form a valid triangle
                */
                private boolean validTriangle(int a, int b, int c) {
                    if (a > (b+c)) {
                        return false;
                    } else if (b > (a+c)) {
                        return false;
                    } else if (c > (a+b)) {
                        return false;
                    } else {
                        return true;
                    }
                    // or you can put this in a neat one-liner
                    //return a < b + c && b < a + c && c < a + b;
                }

                /**
                * Returns a string giving the type of the triangle. A triangle can be
                * either "Equilateral", "Isosceles", or  "Scalene".
                * @return the type of the triangle.
                */
                String getTriangleType() {
                    if (a == b && b == c)
                        return "Equilateral";
                    else if (a == b || b == c || a == c)
                        return "Isosceles";
                    else
                        return "Scalene";
                }

                /**
                * Use Heron's formula to calculate the area.
                * @return the area of the triangle object
                */
                double getArea() {
                    double s = (a+b+c) / 2;
                    return Math.sqrt(s*(s-a)*(s-b)*(s-c));
                } 
            }"




    """

    # Combine task description and inspirational code into a single prompt for solution generation
    prompt = (
        f"Based on the following task description, generate a complete and functional Java solution that meets all the requirements. "
        f"The solution should be well-structured, use meaningful variable names, include necessary comments for clarity, "
        f"and be ready to pass a comprehensive set of unit tests.\n\n"
        f"### Task Description\n\n"
        f"{task_description}\n\n"
        f"### Inspirational Code Snippet\n\n"
        f"{inspirational_code}\n\n"
        "IMPORTANT: The response must be plain Java code with no markdown formatting or ```java blocks. "
        "Ensure that each class is entirely self-contained and is not left incomplete. "
        "No part of the next file should be left in the current file. "
        "Ensure that each class is saved in its own appropriately named file, and that there are no 'leftover' initializers or class definitions from subsequent files."
        "Ensure all imports, public classes, and everything related to the class is included in the appropriate file."
        "Write NO TEXT beyond the code itself, whatsoever. "
    )

    # Call OpenAI API to generate the solution code
    response_content = generate_with_retries(client, prompt, max_retries=3)
    if response_content is None:
        print("Error: Failed to generate solution code after multiple retries.")
        sys.exit(1)

    # Ensure the .hidden_tasks directory exists
    hidden_tasks_dir = os.path.join(".hidden_tasks")
    os.makedirs(hidden_tasks_dir, exist_ok=True)

    # Write the generated code to Java files
    write_generated_code_to_files(hidden_tasks_dir, response_content)

    # Commit and push changes
    commit_and_push_changes(branch_name, hidden_tasks_dir)

def write_generated_code_to_files(directory, code_content):
    """
    Write generated Java code to appropriate files in the specified directory.
    Handles cases where leftover comments or initializations are present.
    Also ensures that import statements and public class declarations are captured.
    """
    leftover_content = ""  # To capture leftover content before the first class
    current_imports = ""   # To capture and carry over import statements
    file_blocks = re.split(r'\b(class|public\s+class|abstract\s+class|final\s+class)\b', code_content)  # Split on different class declarations

    for i in range(1, len(file_blocks), 2):  # Iterate over every class block
        class_declaration = file_blocks[i] + file_blocks[i + 1]  # Reattach split 'class' or 'public class'
        block = leftover_content + class_declaration

        # Extract class name
        class_name_match = re.search(r'class\s+([A-Za-z_]\w*)\s*{', block)  # Match 'class ClassName {'
        if class_name_match:
            class_name = class_name_match.group(1)  # Extract the class name
        else:
            print(f"Skipping block due to missing class name in block: {block[:50]}")
            continue

        # Clean up the block, removing content after the last closing brace
        cleaned_block = clean_class_block(block)

        # Ensure the necessary imports are included
        cleaned_block = check_and_add_missing_imports(cleaned_block)

        # Prepend any import statements (gathered from previous blocks)
        cleaned_block = current_imports + cleaned_block

        # Clear leftover and import content for the next file
        leftover_content = ""
        current_imports = ""

        # Write cleaned code to a file
        file_name = f"{class_name}.java"
        file_path = os.path.join(directory, file_name)

        try:
            with open(file_path, "w") as java_file:
                java_file.write(cleaned_block)
            print(f"Successfully wrote {file_name}")
        except IOError as e:
            print(f"Error writing file {file_name}: {e}")

def clean_class_block(block):
    """Ensure the block only contains content until the last closing brace."""
    
    # Find the position of the last closing brace '}' in the block
    last_closing_brace = block.rfind("}")
    
    if last_closing_brace != -1:
        # Truncate the block at the last closing brace
        block = block[:last_closing_brace + 1]
    
    return block

def check_and_add_missing_imports(block):
    """
    Check the class block for missing imports and add necessary imports based on the content.
    """
    required_imports = {
        "List": "import java.util.List;",
        "ArrayList": "import java.util.ArrayList;",
        "Map": "import java.util.Map;",
        "HashMap": "import java.util.HashMap;",
        "Scanner": "import java.util.Scanner;",
        "Set": "import java.util.Set;",
        "HashSet": "import java.util.HashSet;",
        "Random": "import java.util.Random;"
    }

    # Extract existing imports from the block
    existing_imports = re.findall(r'^\s*import .*;', block, re.MULTILINE)

    # Add missing imports
    imports_to_add = []
    for class_name, import_statement in required_imports.items():
        if class_name in block and import_statement not in existing_imports:
            imports_to_add.append(import_statement)

    # Prepend missing imports at the start of the block
    if imports_to_add:
        block = "\n".join(imports_to_add) + "\n\n" + block

    return block

def generate_with_retries(client, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="o1-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating solution code: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    return None

def commit_and_push_changes(branch_name, directory_path):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        subprocess.run(["git", "add", directory_path], check=True)
        subprocess.run(["git", "commit", "-m", "Add generated solution"], check=True)
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
