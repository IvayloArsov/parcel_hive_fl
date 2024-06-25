# Webapp for Mouse Coordinates and Webcam Pictures

This web application is built with Python 3.10 and Flask,
incorporating vanilla JavaScript for client-side functionalities.
It runs on Ubuntu and uses SQLite for database storage.

## Features

- **Mouse Coordinates**: Visualizes the current coordinates (x, y) of the user's mouse cursor.
- **Webcam Picture Capture**: Takes a picture using the connected webcam upon left-click.

## Installation

1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
2. **Run the Application**:
    ```bash
    python3 app.py

3. **Usage**:

- Open a web browser and navigate to the application URL (default: http://localhost:5000).
- Move your mouse cursor to see live updates of the coordinates.
- Left-click anywhere on the page to capture a picture using the connected webcam.

4. **Database**:

- The SQLite database file (database.db) is generated automatically on startup.
- Stores mouse coordinate data and paths to captured webcam pictures.

**Notes**
- Stop the application (Ctrl+C) to shut down the Flask development server.