# 8BallPool

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Hosting](#hosting)
- [Contributing](#contributing)

## Technologies used

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![Javascript](https://img.shields.io/badge/Javascript-F0DB4F?style=for-the-badge&labelColor=black&logo=javascript&+logoColor=F0DB4F)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## Introduction

Welcome to the Pool Game Application! This is a full stack web application that simulates a pool game. The game features realistic physics, allowing players to enjoy a smooth and engaging experience.

## Features

- Realistic physics using a C library, allowing for precise ball movements and collision handling.
- Backend scripting and server handling with Python.
- SQLite database to store game and player information.
- Interactive front end built with HTML, CSS, and JavaScript.
- Easy-to-use interface for entering game and player information.

## Technology Stack

- **C**: Physics engine for the game.
- **Python**: Backend and scripting.
- **Swig**: To connect Python and C code.
- **SQLite**: Database management.
- **JavaScript**: Frontend interactivity.
- **HTML/CSS**: Frontend structure and styling.

## Required Installations

- Python3
- Clang compiler
- swig


## Usage

Ensure you have make utility installed if not already. Python3, clang, and swig installed for your machine

### Installation 

1. Clone the Repo
```sh
   git clone https://github.com/JashanjotP/8BallPool.git
   ```

2. Run make to compile the C code into an executable and create a shared library used by Python
```sh
   make
   ```

3. The make file will run a lot of commands these basically use the compiler and swig to create a library that can call C functions from within Python. We also need to tell the OS where this library is located during runtime

```sh
   export LD_LIBRARY_PATH=`pwd`
   ```

4. Now you can run the web server locally

```sh
   python3 server.py
   ```

### Hosting

Link: [https://8ballpool-production.up.railway.app/]

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
