# Negative Feedback App

A simple Flask application for collecting anonymous negative feedback for registered users.

## Features

*   User registration and login
*   Submit anonymous feedback to specific users
*   View received feedback
*   Delete account

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**
    ```bash
    python app.py
    ```

3.  Open your web browser and go to `http://127.0.0.1:5000` (or the address provided by Flask).

## Data Storage

*   User credentials (hashed passwords) are stored in `data/users.json`.
*   Feedback for each user is stored in separate files like `data/feedback_<username>.json`. 