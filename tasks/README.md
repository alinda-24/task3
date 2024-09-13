# Is this a Triangle?

The following assignment is about geometry: rectangles and triangles modeled with Java! You are going to make decisions using `if` and `else` statements and be introduced to the *triangle inequality*.

<img src="images/is_this_a_triangle.png" alt="very funny boomer meme" width="500"/>

### 💀 Deadline
This work should be completed before the exercise on **Friday 22 September**.

### 👨🏽‍🏫 Instructions
For instructions on how to do and submit the assignment, please see the
[assignments section of the course instructions](https://gits-15.sys.kth.se/inda-23/course-instructions#assignments).

### 📝 Preparation

- Read and answer all questions in Module 3: [Branching](https://qbl.sys.kth.se/sections/dd1337_ht23_programmering_prog/container/branching)
- You can access the OLI material both:
  - via Canvas (see the [OLI Torus SE](https://canvas.kth.se/courses/41415/external_tools/4247) link in the left menu)
  - or directly at this [webpage](https://qbl.sys.kth.se/sections/dd1337_ht23_programmering_prog/container/dd1337__programming)

### ✅ Learning Goals

1. Branching (`if` and `else` statements)
2. Access object fields and methods with dot-notation
3. Using the Java Math Library

### 🚨 Troubleshooting Guide

1. Look at this week's [posted issues](https://gits-15.sys.kth.se/inda-23/help/issues). Are other students asking about your problem?
2. If not, post a question yourself by creating a [New Issue](https://gits-15.sys.kth.se/inda-23/help/issues/new). Add a descriptive title, beginning with "Task *x*: *summary of problem here*"
3. Ask a TA in person during the [weekly lab](https://queue.csc.kth.se/Queue/INDA). Check your schedule to see when the next lab is.

We encourage you to discuss with your course friends, but **do not share answers**!

### 🏛 Assignment

#### Exercise 3.0 -- A Triangle Object
Create a new class called `Triangle.java` in the [src](src/) directory. 

The triangle class should have three fields of type `int` -- the sides `a`, `b` and `c`. Add a constructor that takes one parameter (or *argument*) per side of the triangle, setting each side's value to the corresponding parameter. 

The main method of the example below should compile if implemented correctly.

<details>
  <summary> 🛠 Main method example </summary>

```Java
public static void main(String[] args){
  // create a new Triangle object with the sides 3, 1 and 1
  Triangle triangle = new Triangle(3, 1, 1);
}
```
</details>

#### Exercise 3.1 -- The Triangle Inequality
Last week we learned about accessors and mutators but did not implement any restrictions on when you may read or write to the fields. Let's create such a restriction for the constructor method now.  

*The Triangle Inequality* is a popular theorem in mathematics. In simplified terms, it lets you know if three sides, *a*, *b*, and, *c*, can make a triangle. For example, if I give you *a = 3*, *b = 1* and *c = 1*, you can **not** make a triangle. An example of valid input is *a = 1*, *b = 1* and *c = 1*.

Create a method in the `Triangle` class with the following header `private boolean validTriangle(int a, int b, int c)`, that returns `true` if the parameters can construct the sides of a triangle, and `false` in all other cases.

A straightforward approach is checking if the three following relations are true. If they are, then the sides *a*, *b* and *c*, can make a triangle:

<img src="images/triangle-inequality.png" alt="drawing" width="400"/>


You also want to handle invalid input, making sure that a triangle object is created *iff* the parameters are valid. In the provided example, you see an example of how to *throw an exception* that exits the program with an error message.

<details>
<summary> 📚 What are Exceptions? </summary>
<! -- requires a blank space -->

When a program tries to do something unexpected, like dividing by zero, Java creates a special object called an exception to signal the issue. An exception is a class that provides details about the problem. This creation process is known as *throwing an exception*. These objects are created from classes meant for errors like `Exception`, `IllegalArgumentException`, or `NullPointerException`.

To prepare our program for these unexpected events, we use *exception handling*. It acts like a safety net, allowing us to catch these thrown exceptions. We can then decide on the next steps, like showing an error message or attempting an alternative approach. Through this mechanism, we ensure that even if one part of our program faces a problem, the rest can continue to function smoothly.

In this case, we chose the `IllgalArgumentException`, because we want to signal that the arguments are *illegal*. 
You are going to learn more about exception handling throughout the course.
 
</details>

You should put the check at the top of your constructor and try the previous example again:

```Java
public Triangle(int a, int b, int c) {
  if(validTriangle(a, b, c)) {
    // Okay to create the Triangle object!
  } else {
    // End the program with an error message
    throw new IllegalArgumentException("This is not a valid triangle!");
  }
}
```

> **Assistant's Note:** There are various ways to achieve this. Under the [Wikipedia page for the Triangle Inequality](https://en.wikipedia.org/wiki/Triangle_inequality#Mathematical_expression_of_the_constraint_on_the_sides_of_a_triangle) there are some useful expressions you can use. Although it is not necessary, you may also use the [Java Math Library](https://docs.oracle.com/javase/tutorial/java/data/beyondmath.html).

#### Exercise 3.2 -- The three types of Triangles

From the [Wikipedia page on Triangles](https://en.wikipedia.org/wiki/Triangle) you can read about the three types of triangles. Make a method in the `Triangle` class called `String getTriangleType()` that returns a `String` of what type the triangle is (*"Equilateral"*, *"Isosceles"* or *"Scalene"*).

Equilateral Triangle             |  Isosceles Triangle | Scalene Triangle
:-------------------------:|:-------------------------:|:-------------------------:
![](https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Triangle.Equilateral.svg/240px-Triangle.Equilateral.svg.png)  |  ![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Triangle.Isosceles.svg/156px-Triangle.Isosceles.svg.png) | ![](https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Triangle.Scalene.svg/240px-Triangle.Scalene.svg.png)

> **From Wikipedia:** Hatch marks, also called tick marks, are used in diagrams of triangles and other geometric figures to identify sides of equal lengths. A side can be marked with a pattern of "ticks", short line segments in the form of tally marks; two sides have equal lengths if they are both marked with the same pattern.

#### Exercise 3.3 -- `Triangle.getArea()`
In this exercise, you have to calculate the area of a triangle. Mathematicians have come up with *many* formulas to achieve this, but since our triangle object has the side lengths as fields, we recommend using [Heron's Formula](https://en.wikipedia.org/wiki/Heron%27s_formula). The formula states that the area of a triangle whose sides have lengths *a*, *b*, and *c* is

<img src="images/herons-formula.png" alt="Heron's formula" width="400"/>

where *s* is the *semi-perimeter* of the triangle:

<img src="images/semi-perimeter.png" alt="Semi-perimeter" width="200"/>

The method should be called `getArea()` and returns a `double`. Test your implementation before you push your solution to GitHub!

<details>
<summary> 📚 How-to: square root (Java Math Library) </summary>
<! -- requires a blank space -->

To find the square root of an expression, you have to use the [Java Math library](https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html). To take the square root of any number, you make the following call:

```Java
Math.sqrt(argument); // "argument" can be either a number, or an expression that evaluates to a number
```

</details>

> **Assistant's Note:** To use Heron's Formula you need the *semi-perimeter* *s*. We suggest you add a *helper method*, called `getPerimeter()`, to your Triangle class.

##### 💭 Food for thought
An example of why one would use getters and setters to ensure encapsulation:

1. Create a triangle with the sides *a = 1*, *b = 1*, and, *c = 1*.
2. Change *a* from 1 to 3.
3. Do you still have a valid triangle?
4. How would you fix this?

You don't have to provide any answers, but it will be helpful to think about how to solve this with the code you already have.

#### Exercise 3.4 -- Reverse Engineering
Now that you have created a `Triangle` class, let's also create a `Rectangle` class along with some useful methods.

For this exercise, you will not be given detailed instructions. Instead, you will need to read through the code in the [`src/RectangleExample`](src/RectangleExample.java) file. This code will attempt to create a `Rectangle` object and call three different methods on it. At the moment, it will not compile and run, since there is no `Rectangle.java` file, so start by creating this file in your [src](src) folder.

You will now need to create the fields, getters, setters, and required methods in your `Rectangle` class that will allow `RectangleExample` to run and produce the correct results. Your code does not need to cover every edge case, but make sure to run the `RectangleExample` and check that your methods return the expected values. If you get stuck, don't hesitate to get help through any of the channels listed in the Troubleshooting section.

#### Exercise 3.5 -- Returning a boolean expression
Instead of writing a function that uses if statements to return either true or false, sometimes you can just return a boolean expression instead. This is because the expression we are passing to the if statement is the exact value we want to return.

<details>
  <summary> 🛠 Returning a boolean expression </summary>

  Using if statements to return either true or false.
  ```java
  public boolean isRegularPentagon(int numSides, boolean hasEqualSides) {
      if (numSides == 5 && hasEqualSides) {
          return true;
      } else {
          return false;
      }
  }
  ```

  Using a direct return statement.
  ```java
  public boolean isRegularPentagon(int numSides, boolean hasEqualSides) {
      return numSides == 5 && hasEqualSides;
  }
  ```
</details>

Using this principle, improve the code you have written this week. If you have already done this, good job! 

### ❎ Checklist
- [ ] Create a Triangle class with a constructor that takes three sides and checks if they forma a valid triangle. 
- [ ] Create a method to classify a triangle based on its sides. The three types are equilateral triangles, isosceles triangles, and scalene triangles. 
- [ ] Create a method to calculate the triangle's area.
- [ ] Create the Rectangle class by reverse engineering the RectangleExample.java file which calls its methods.
- [ ] Improve your code by using direct return statements.

> **Assistant's note:** We have added this checklist for you to make a final check before handing in your work. You don't have to tick the boxes unless you want to (to tick a box, place an "x" within the brackets when editing the README.md)

### 🐞 Bugs and errors?
If you find any inconsistencies or errors in this exercise, please open a [New Issue](https://gits-15.sys.kth.se/inda-23/help/issues/new) with the title "Task *x* Error: *summary of error here*". Confirmed bugs will be rewarded by mentions in the acknowledgment section.

### 🙏 Acknowledgment
This task was designed by                <br>
[Linus Östlund](mailto:linusost@kth.se)  <br>
[Sofia Bobadilla](mailto:sofbob@kth.se)  <br>
[Gabriel Skoglund](mailto:gabsko@kth.se) <br>
[Arvid Siberov](mailto:asiberov@kth.se)  <br>
[Alexander Runebou](mailto:alerun@kth.se)<br>
