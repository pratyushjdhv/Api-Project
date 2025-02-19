#  API - PROJECT

This is a simple Todo API built with Flask, Flask-RESTful, and Flask-SQLAlchemy.

## Requirements

The required packages are listed in the `req.txt` file. You can install them using pip:

```sh
pip install -r req.txt
```

## Database

The project uses SQLite as the database. The database file is located at `instance/todo.sqlite3`.

## Running the Application

To run the application, execute the following command:

```sh
python api.py
```

The application will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### Create a Todo

- **URL:** `/todo`
- **Method:** `POST`
- **Payload:**
  ```json
  {
    "title": "Daily Tasks",
    "task": "Complete unit testing"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Todo-list created"
  }
  ```

### Get All Todos

- **URL:** `/todo/task`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "tasks": [
      {
        "title": "Daily Tasks",
        "tasks": ["Complete unit testing"]
      }
    ]
  }
  ```

### Get Single Todo

- **URL:** `/todo/task/<int:task_id>`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "tasks": ["Complete unit testing"]
  }
  ```

### Update a Todo

- **URL:** `/todo/<int:task_id>`
- **Method:** `PUT`
- **Payload:**
  ```json
  {
    "task": "Complete unit testing and review code"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Task updated"
  }
  ```

### Delete a Todo

- **URL:** `/todo/<int:task_id>`
- **Method:** `DELETE`
- **Response:**
  ```json
  {
    "message": "Task deleted"
  }
  ```

## Running Tests

To run the tests, execute the following command:

```sh
python -m unittest test.py

