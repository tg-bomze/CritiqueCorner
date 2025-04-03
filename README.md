# CritiqueCorner: Anonymous Feedback Platform

CritiqueCorner is a simple web application built with Flask that allows registered users to give and receive anonymous constructive feedback.

## Purpose

The main goal of this application is to provide a safe and anonymous space for users to share feedback with each other. This can be useful in various contexts, such as:

*   Peer reviews within a team or organization.
*   Collecting feedback after presentations or workshops.
*   Personal development by understanding how others perceive you.
*   Any situation where honest, anonymous feedback is valuable.

## Features

*   **User Registration:** New users can create an account.
*   **User Login:** Registered users can securely log in.
*   **Submit Feedback:** Logged-in users can select another registered user and submit anonymous feedback for them.
*   **View Feedback:** Users can view all the anonymous feedback they have received.
*   **Account Deletion:** Users can delete their own accounts and associated data.

## How it Works

1.  **Register:** Create a new user account with a unique username and password.
2.  **Login:** Access your account using your credentials.
3.  **Give Feedback:** Navigate to the feedback submission section, choose a recipient user from the list, type your feedback, and submit it anonymously.
4.  **Receive Feedback:** Check your dashboard or feedback section to view comments left for you by other users. The identity of the sender is kept anonymous.
5.  **Manage Account:** Delete your account if you no longer wish to use the platform.

## Technology Stack

*   **Backend:** Flask (Python web framework)
*   **Data Storage:** JSON files (`data/users.json` for user credentials, `data/feedback_<username>.json` for feedback per user).

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd CritiqueCorner 
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    python app.py
    ```
4.  Open your web browser and go to `http://127.0.0.1:5000` (or the address provided by Flask).

## Data Storage

*   User credentials (usernames and hashed passwords) are stored in `data/users.json`.
*   Feedback intended for a specific user is stored in a dedicated JSON file named `data/feedback_<username>.json`. 