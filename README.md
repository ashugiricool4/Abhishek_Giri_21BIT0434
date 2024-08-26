# Abhishek_Giri_21BIT0434

# file 🔗 
//https://drive.google.com/file/d/1To4hm_5WaZN6TVh0U98lcOtd_T2lVmso/view?usp=drive_link

. Chess-Like Game

This project implements a chess-like game with a server-side implementation in Python and a web-based client interface.

# Features

- 5x5 grid game board
- Two players: A and B
- Three types of pieces: Pawns (P), Hero1 (H1), and Hero2 (H2)
- WebSocket-based real-time communication between server and clients

# Server-Side Implementation

The server is implemented in Python using the asyncio and websockets libraries. 
It manages the game state, handles player moves, and broadcasts updates to connected clients.

. Key Components
- GameState` class: Manages the game board, player turns, and piece movements
- WebSocket handler: Manages client connections and processes game moves

# Requirements
- Python 3.7+
- Websockets library

# install the required package using pip:
-bash
-pip install websockets

# Run the server:

--To start the WebSocket server, run the following command:
-python websocket_server.py

-- To serve an HTML client interface, create a simple Flask app:
-python app.py

-The server will start on `localhost:8765`.

# Web Client Implementation

The client is implemented as an HTML page with JavaScript for WebSocket communication and game board rendering.

 # Features
- Real-time game board updates
- Player assignment (A or B)
- Move validation feedback

# Game Rules
- Pawns (P) can move one space in any direction (left, right, forward, backward)
- Hero1 (H1) can move two spaces horizontally or vertically
- Hero2 (H2) can move two spaces diagonally
- Players take turns moving their pieces
- Pieces can capture opponent pieces by moving to their space

# Getting Started

--To play the game:

-Open the HTML client interface (if running the Flask server) or use a WebSocket client like websocat or a browser-based client.

-Two players should connect to the WebSocket server.

-Players will be assigned either "A" or "B".

-Players take turns making moves on the grid.

# Future Improvements
- Add win condition logic
- Implement more sophisticated AI for single-player mode
- Enhance the user interface with piece graphics and move animations
- Deploying the server on a cloud platform for broader accessibility.
- Adding a more sophisticated UI for a better user experience.

# If any issue is encounterd then:
-Ensure that the WebSocket server is running on ws://localhost:8765.

-Check that the Python environment has the websockets package installed.

-Review the console logs for any errors.



