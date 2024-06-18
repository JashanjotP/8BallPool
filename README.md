# 8BallPool

A simple 8 Ball Pool game made using Python as a Web Server and C to do all the calculations 

## Required Installations

- Python3
- Clang compiler
- swig


## Getting Started

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

Project is Hosted on Railway

Link: [https://8ballpool-production.up.railway.app/]