# Task Generation and Submission System

Welcome to the Task Generation and Submission System! This guide will walk you through the steps of creating a new task, solving it, and submitting your solution for review.

## 💀 Deadline
 This work should be completed before the exercise, on **Friday 20th September**.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Step 1: Generating a New Task](#step-1-generating-a-new-task)
- [Step 2: Pulling the Task to Your Local Environment](#step-2-pulling-the-task-to-your-local-environment)
- [Step 3: Solving the Task](#step-3-solving-the-task)
- [Step 4: Committing and Pushing Your Solution](#step-4-committing-and-pushing-your-solution)
- [Step 5: Creating a Pull Request](#step-5-creating-a-pull-request)
- [Step 6: Review and Merge Process](#step-6-review-and-merge-process)
- [Troubleshooting](#troubleshooting)

## Overview

This system allows you to generate new programming tasks, solve them locally, and submit your solution through a pull request (PR). The PR will be automatically reviewed, and your code will be tested before it is merged.

## Step 1: Generating a New Task

1. **Navigate to the GitHub Repository**:
   - Go to the repository where the task generation system is hosted.

2. **Generate a New Task**:
   - Click on the "Actions" tab in the repository.
   - Select the "Generate Task" workflow from the list on the left.
   - Click the "Run workflow" button on the right.
   - Fill in the required fields:
     - **Theme**: Describe the theme or concept of the task.
     - **Difficulty**: Select the difficulty level (basic, medium, or hard).
     - **Language**: Choose the natural language for the task description.
   - Click "Run workflow" to start the task generation process.

3. **Wait for the Task Generation**:
   - The system will automatically create a new branch in the repository with the generated task. This branch will be named something like `task-YYYYMMDDHHMMSS`.

## Step 2: Pulling the Task to Your Local Environment

1. **Clone the Repository**:
   - If you haven't already, clone the repository to your local machine:
     ```bash
     git clone https://github.com/your-username/your-repo.git
     ```

2. **Check Out the Task Branch**:
   - Navigate to the repository directory:
     ```bash
     cd your-repo
     ```
   - List all branches to find the new task branch:
     ```bash
     git branch -r
     ```
   - Check out the new task branch:
     ```bash
     git checkout -b task-YYYYMMDDHHMMSS origin/task-YYYYMMDDHHMMSS
     ```

## Step 3: Solving the Task

1. **Open the Task Description**:
   - Navigate to the `tasks/` directory and open the `new_task.md` file. This file contains the detailed description of the task you need to solve.

2. **Edit the Template Code**:
   - Go to the `src/` directory and open the `template_code.java` file.
   - Solve the task by writing your solution in this file.

3. **Test Your Solution**:
   - Before committing, make sure your code works by running any available tests.

## Step 4: Committing and Pushing Your Solution

1. **Commit Your Changes**:
   - Once you're satisfied with your solution, stage and commit your changes:
     ```bash
     git add src/template_code.java
     git commit -m "Solved the task"
     ```

2. **Push Your Branch to GitHub**:
   - Push your local branch to GitHub:
     ```bash
     git push origin task-YYYYMMDDHH
     ```

