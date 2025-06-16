# Dockerized TODO Application

A simple command-line TODO list application built with Python and PostgreSQL, containerized using Docker.

## Features

- User authentication (login system)
- Create TODO items
- Read TODO items
- Update TODO items
- Delete TODO items
- Multi-user support
- Persistent storage using PostgreSQL

## Prerequisites

- Docker
- Docker Compose

## Installation & Running

1. Clone this repository
2. Navigate to the project directory
3. Run the following command to start the application:

```bash
docker-compose up --build
```

## Usage

The application provides a simple command-line interface with the following options:

1. **Login/Exit**
   - Choose '1' to log in
   - Choose '2' to exit

2. **After Login**
   - Choose '1' to add a new TODO item
   - Choose '2' to delete an existing item
   - Choose '3' to edit an existing item
   - Choose '4' to log out

## Environment Variables

The application uses the following environment variables (already configured in docker-compose.yml):

- DB_HOST: Database host
- DB_PORT: Database port
- DB_NAME: Database name
- DB_USER: Database user
- DB_PASSWORD: Database password

## Project Structure

```
├── TODO.py             # Main application file
├── Dockerfile          # Docker configuration for the application
├── docker-compose.yml  # Docker Compose configuration
└── requirements.txt    # Python dependencies
```

## Database Schema

The application uses a single table `todolist` with the following structure:

- id: SERIAL PRIMARY KEY
- username: VARCHAR(30)
- list: VARCHAR(300)

## Technologies Used

- Python 3.10
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
