# Fields Reservation API

This is the backend API for a reservations app, which includes an admin section and a user section (mobile). This project is part of the ioet University 2.0 program.

## Table of Contents

1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Available Commands](#available-commands)
4. [Project Structure](#project-structure)
5. [Development Guidelines](#development-guidelines)
6. [Troubleshooting](#troubleshooting)

## Requirements

- Docker
- Docker Compose
- Make (optional, but recommended for easier command execution)
- Python 3.12+

## Setup

1. Clone the repository:

```bash
git clone git@github.com:Gerardo-rios/reservation-api.git
cd reservation-api
```

2. Copy the example environment file:

```bash
cp .env.example .env
```

Edit the `.env` file with your specific configuration if needed.

3. Build and start the Docker containers:

```bash
make build
make up
```

If you don't have Make installed, you can use `docker-compose build` and `docker-compose up -d` instead.

4. Create the database init file:

```bash
cp init.sql.example db/mysql/mysql-init/init.sql
```


Your API should now be running at `http://localhost:8000`.

## Available Commands

Here are some useful commands you can use (assuming you have Make installed):

- `make build`: Build the Docker images
- `make up`: Start the Docker containers
- `make down`: Stop the Docker containers
- `make logs`: View the logs of all containers
- `make shell`: Open a shell in the app container
- `make test`: Run the test suite
- `make lint`: Run the linter
- `make format`: Format the code using Black
- `make db-rebuild`: Rebuild the database (drops and recreates)
- `make mysql-cli`: Enter MySQL CLI
- `make db-dump`: Dump the database
- `make db-restore`: Restore the database from a dump

If you don't have Make installed, you can find the equivalent Docker and Docker Compose commands in the Makefile.

## Project Structure

```bash
├── db
│   ├── mysql
│   │   ├── mysql-data
│   │   ├── mysql-dump
│   │   └── mysql-init
│   └── neo4j
│       ├── conf
│       ├── data
│       ├── logs
│       └── plugins
├── docker-compose.yml
├── Dockerfile
├── init.sql.example
├── makefile
├── mypy.ini
├── poetry.lock
├── pyproject.toml
├── README.md
└── src
    ├── config
    ├── core
    │   ├── entities
    │   └── use_cases
    ├── infraestructure
    │   ├── database
    │   ├── framework
    ├── interface
    │   ├── controllers
    │   └── repositories
    └── tests
        ├── core
        └── interface
```

## Development Guidelines

1. Follow the Test-Driven Development (TDD) approach.
2. Write unit tests for all new functionality.
3. Ensure all tests pass before submitting a pull request.
4. Use Black for code formatting.
5. Follow PEP 8 style guide for Python code.
