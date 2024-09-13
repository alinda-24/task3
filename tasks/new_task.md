# 💻 Simple Java Game Development

Explore object-oriented programming by designing a simple game application in Java. This assignment will help you understand the components of a Java class and how they interact in the context of game development.

### 📅 Deadline

Complete this assignment by **Friday, 30th September**.

### 📚 Instructions

Please refer to the [assignment guidelines](https://example.com/assignments) for details on submission and requirements.

### 📝 Preparation

Before starting the assignment, make sure to complete the following:

- Read [Object-Oriented Programming in Java](https://example.com/oop-java)
- Review materials in Module 3 of the OLI course.

> **Note:** The course content might be updated, so make sure to check for new materials.

### 🎯 Learning Goals

By the end of this task, you should be able to:

- Design Java classes
- Add instance fields
- Implement constructor methods
- Create *getters* and *setters*
- Print information to the terminal
- Utilize the `main` method
- Understand scope and variable shadowing

### 🔧 Troubleshooting Guide

If you encounter any issues:

1. Check the [discussion forum](https://example.com/forum) to see if any solutions exist.
2. Post your question with a clear title if you don’t find an answer.
3. Ask a TA during the weekly lab sessions.

Please remember to collaborate wisely and avoid sharing direct answers.

### 🎮 Assignment Overview

In this project, you will create a simple Java game featuring player movement, a scoring system, and enemy interactions. You will implement this with various Java classes to encapsulate functionality and data. Follow the instructions below to complete the task.

---

#### Exercise 1 -- Player Class Design

Create a `Player` class with the following fields:

- `String name` - the name of the player.
- `int score` - the current score of the player.
- `int position` - the player's position on the game board.

Follow these steps:

1. Add private fields for the above attributes.
2. Implement a constructor that initializes the fields.
3. Add *getters* (`getName`, `getScore`, `getPosition`) and *setters* (`setScore`, `setPosition`) for these fields.
4. Implement a `printInfo` method to print player details in a formatted way.

```java
public class Player {

    // Define the player's fields

    // Implement the constructor

    // Add getters and setters
    
    public void printInfo() {
        // Print player details
    }

    public static void main(String[] args) {
        Player player = new Player("Hero");
        player.setScore(100);
        player.setPosition(5);
        
        player.printInfo();  // Print info
    }
}
```

#### Exercise 2 -- Game Logic

Now, create a main class `Game` to manage the overall game logic:

- Declare a player instance.
- Implement a method `movePlayer(int steps)` to update the player's position and increase score.
- Use the `main` method to simulate a game session.

```java
public class Game {
    
    private Player player;

    public Game(String playerName) {
        player = new Player(playerName);
    }

    public void movePlayer(int steps) {
        // Implement logic to move player and update score
        // Example: player.setPosition(player.getPosition() + steps);
    }

    public static void main(String[] args) {
        Game game = new Game("Hero");
        game.movePlayer(3);
        game.player.printInfo();
    }
}
```

#### Exercise 3 -- Enemy Interaction

Design an `Enemy` class and update the `Player` and `Game` classes to handle interactions with enemies:

- Add a `boolean alive` field to track if the enemy is alive.
- Implement methods to simulate encounters and outcomes (e.g., combat).
- Update `movePlayer` to include possible enemy encounters.

```java
public class Enemy {
    
    private boolean alive;

    public Enemy() {
        alive = true;
    }

    // Define methods for interaction with the player

    public boolean isAlive() {
        return alive;
    }
}
```

#### Exercise 4 -- Variable Shadowing

Review the following example to understand variable shadowing:

```java
public class ShadowExample {

    private int score = 0;

    public void increaseScore() {
        int score = 10;
        System.out.println(score);  // Prints the local variable, not the field
    }

    public static void main(String[] args) {
        ShadowExample example = new ShadowExample();
        example.increaseScore();  // Understand why it prints 10
    }
}
```

Investigate how to correct variable shadowing using the `this` keyword and be prepared to discuss in lab sessions.

> **Note:** Pay attention to the distinction between local variables and instance fields.

---

Feel free to unleash your creativity and expand the game capabilities further! Enjoy coding and happy gaming!