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

    # Ensure we are on the correct branch
    try:
        subprocess.run(["git", "checkout", branch_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error checking out branch {branch_name}: {e}")
        sys.exit(1)

    # Read the solution code from the .hidden_tasks directory
    solution_files = []
    try:
        for filename in os.listdir(".hidden_tasks"):
            if filename.endswith(".java"):
                with open(os.path.join(".hidden_tasks", filename), "r") as file:
                    solution_files.append(file.read())
    except FileNotFoundError:
        print("Error: Solution files not found in .hidden_tasks directory.")
        sys.exit(1)

    if not solution_files:
        print("Error: No Java solution files found in .hidden_tasks.")
        sys.exit(1)

    solution = "\n\n".join(solution_files)

    # Example tests to inspire the model (not to be directly copied)
    example_tests = """
    
        "import org.junit.BeforeClass;
        import org.junit.Test;

        import static org.junit.Assert.assertEquals;
        import static org.junit.Assert.assertFalse;
        import static org.junit.Assert.assertTrue;

        public class RectangleTest {

            public static final int RECT_WIDTH = 40;
            public static final int RECT_HEIGHT = 50;
            public static final int SQUARE_SIDE = 20;

            public static final double DIAGNONAL_ERROR_MARGIN = 0.1;

            private static Rectangle rectangle;
            private static Rectangle square;

            @BeforeClass
            public static void setUp() {
                rectangle = new Rectangle();
                rectangle.setWidth(RECT_WIDTH);
                rectangle.setHeight(RECT_HEIGHT);

                square = new Rectangle();
                square.setWidth(SQUARE_SIDE);
                square.setHeight(SQUARE_SIDE);
            }

            @Test
            public void testRectangleArea() {
                assertEquals(RECT_WIDTH * RECT_HEIGHT, rectangle.area());
            }

            @Test
            public void testSquareArea() {
                assertEquals(SQUARE_SIDE * SQUARE_SIDE, square.area());
            }

            @Test
            public void testRectangleDiagonalLength() {
                double expectedDiagonal = Math.sqrt(RECT_WIDTH * RECT_WIDTH + RECT_HEIGHT * RECT_HEIGHT);
                assertEquals(expectedDiagonal, rectangle.diagonalLength(), DIAGNONAL_ERROR_MARGIN);
            }

            @Test
            public void testSquareDiagonalLength() {
                double expectedDiagonal = Math.sqrt(SQUARE_SIDE * SQUARE_SIDE * 2);
                assertEquals(expectedDiagonal, square.diagonalLength(), DIAGNONAL_ERROR_MARGIN);
            }

            @Test
            public void testRectangleIsSquare() {
                assertFalse(rectangle.isSquare());
            }

            @Test
            public void testSquareIsSquare() {
                assertTrue(square.isSquare());
            }
        }"

        "
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;
        import static org.junit.Assert.assertTrue;
        import static org.junit.Test.None;

        public class TriangleTest {
            @Test(expected = Test.None.class)
            public void validTriangleIsValid() {
                new Triangle(1, 1, 1);
            }

            @Test(expected = IllegalArgumentException.class)
            public void invalidTriangleIsInvalid() {
                new Triangle(1, 1, 5);
            }

            @Test
            public void testTriangleTypeEquilateral() {
                Triangle t = new Triangle(1, 1, 1);
                assertEquals(t.getTriangleType(), "Equilateral");
            }

            @Test
            public void testTriangleTypeIsosceles() {
                Triangle t = new Triangle(2, 2, 1);
                assertEquals(t.getTriangleType(), "Isosceles");
            }

            @Test
            public void testTriangleTypeScalene() {
                Triangle t = new Triangle(2, 3, 4);
                assertEquals(t.getTriangleType(), "Scalene");
            }
        }
        "


    """

    # Combine the solution into a single prompt for test generation
    prompt = (
        f"Given the following Java solution, generate a set of high-quality unit tests. "
        f"Ensure the tests are thorough, robust, and cover all edge cases, including invalid inputs, boundary conditions, and performance considerations. "
        f"Ensure the tests use the correct imports and that each class is placed in the correct file as per Java naming conventions.\n\n"
        f"### Solution\n{solution}\n\n"
        f"### Example Tests (for inspiration only)\n{example_tests}\n\n"
        "IMPORTANT: The response must be plain Java code with no markdown formatting or ```java blocks. Ensure that the response is ready to be saved directly as a .java file."
    )

    response_content = generate_with_retries(client, prompt, max_retries=3)
    if response_content is None:
        print("Error: Failed to generate the tests after multiple retries.")
        sys.exit(1)

    # Write the generated tests to appropriate Java files in the gen_test directory
    gen_test_dir = os.path.join("gen_test")
    write_generated_tests_to_files(gen_test_dir, response_content)

    # Commit and push changes
    commit_and_push_changes(branch_name, gen_test_dir)

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
            print(f"Error generating the tests: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    return None

def write_generated_tests_to_files(directory, code_content):
    """
    Write generated Java tests to separate files based on class names.
    Handles cases where leftover comments or initializations are present.
    Also ensures that import statements and public class declarations are captured.
    """
    leftover_content = ""  # To capture leftover content before the first class
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

        # Construct the file content
        package_declaration = "package test;\n\n"
        imports = (
            "import org.junit.Before;\n"
            "import org.junit.Test;\n"
            "import static org.junit.Assert.*;\n\n"
        )
        file_content = package_declaration + imports + "class " + block

        file_name = f"{class_name}Test.java"
        file_path = os.path.join(directory, file_name)

        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        try:
            with open(file_path, "w") as java_file:
                java_file.write(file_content)
            print(f"Successfully wrote {file_name}")
        except IOError as e:
            print(f"Error writing file {file_name}: {e}")

def commit_and_push_changes(branch_name, directory):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        subprocess.run(["git", "add", directory], check=True)
        subprocess.run(["git", "commit", "-m", "Add generated tests"], check=True)
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
