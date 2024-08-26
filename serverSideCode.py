import asyncio
import websockets
import json

GRID_SIZE = 5
INITIAL_POSITIONS = {
    "A": ["P1", "H1", "H2", "H1", "P1"],
    "B": ["P1", "H1", "H2", "H1", "P1"]
}

class GameState:
    def __init__(self):
        self.board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.turn = "A"
        self.players = {"A": None, "B": None}
        self.positions = {"A": [], "B": []}  # Track positions of all characters

    def reset_game(self):
        self.__init__()

    def initialize_game(self):
        for i, char in enumerate(INITIAL_POSITIONS["A"]):
            self.board[0][i] = f"A-{char}"
            self.positions["A"].append((0, i))
        for i, char in enumerate(INITIAL_POSITIONS["B"]):
            self.board[4][i] = f"B-{char}"
            self.positions["B"].append((4, i))

    def make_move(self, player, move):
        character_type, direction = move.split(":")
        row, col = self.get_position(player, character_type)

        if character_type.startswith("P"):  # Pawn
            new_row, new_col = self.move_pawn(row, col, direction)
        elif character_type.startswith("H1"):  # Hero1
            new_row, new_col = self.move_hero1(row, col, direction)
        elif character_type.startswith("H2"):  # Hero2
            new_row, new_col = self.move_hero2(row, col, direction)
        else:
            return False  # Invalid character type

        if self.is_valid_move(player, new_row, new_col):
            self.update_board(row, col, new_row, new_col, character_type)
            self.switch_turn()
            return True
        return False

    def get_position(self, player, character_type):
        for i, (r, c) in enumerate(self.positions[player]):
            if self.board[r][c] == f"{player}-{character_type}":
                return r, c
        return None, None

    def move_pawn(self, row, col, direction):
        if direction == "L":
            return row, col - 1
        elif direction == "R":
            return row, col + 1
        elif direction == "F":
            return row - 1 if self.turn == "A" else row + 1
        elif direction == "B":
            return row + 1 if self.turn == "A" else row - 1
        return row, col

    def move_hero1(self, row, col, direction):
        if direction == "L":
            return row, col - 2
        elif direction == "R":
            return row, col + 2
        elif direction == "F":
            return row - 2 if self.turn == "A" else row + 2
        elif direction == "B":
            return row + 2 if self.turn == "A" else row - 2
        return row, col

    def move_hero2(self, row, col, direction):
        if direction == "FL":
            return row - 2 if self.turn == "A" else row + 2, col - 2
        elif direction == "FR":
            return row - 2 if self.turn == "A" else row + 2, col + 2
        elif direction == "BL":
            return row + 2 if self.turn == "A" else row - 2, col - 2
        elif direction == "BR":
            return row + 2 if self.turn == "A" else row - 2, col + 2
        return row, col

    def is_valid_move(self, player, new_row, new_col):
        if not (0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE):
            return False  # Out of bounds
        if self.board[new_row][new_col].startswith(player):
            return False  # Cannot move onto own character
        return True

    def update_board(self, old_row, old_col, new_row, new_col, character_type):
        opponent = "B" if self.turn == "A" else "A"
        # Capture opponent's character if present
        if self.board[new_row][new_col].startswith(opponent):
            self.positions[opponent].remove((new_row, new_col))

        # Move the character
        self.board[new_row][new_col] = f"{self.turn}-{character_type}"
        self.board[old_row][old_col] = ""
        for i, (r, c) in enumerate(self.positions[self.turn]):
            if r == old_row and c == old_col:
                self.positions[self.turn][i] = (new_row, new_col)
                break

    def get_board(self):
        return self.board

    def switch_turn(self):
        self.turn = "B" if self.turn == "A" else "A"

async def handler(websocket, path):
    state = GameState()
    state.initialize_game()
    player = None

    # Assign player A or B
    if state.players["A"] is None:
        state.players["A"] = websocket
        player = "A"
    elif state.players["B"] is None:
        state.players["B"] = websocket
        player = "B"

    await websocket.send(json.dumps({"type": "game_state", "board": state.get_board(), "turn": state.turn}))

    async for message in websocket:
        data = json.loads(message)

        if data["type"] == "move":
            if state.turn == player:
                move = data["move"]
                if state.make_move(player, move):
                    # Broadcast new game state to both players
                    for p in state.players.values():
                        if p:
                            await p.send(json.dumps({"type": "game_state", "board": state.get_board(), "turn": state.turn}))
                else:
                    await websocket.send(json.dumps({"type": "invalid_move", "message": "Invalid move. Try again."}))

        elif data["type"] == "reset":
            state.reset_game()
            state.initialize_game()
            for p in state.players.values():
                if p:
                    await p.send(json.dumps({"type": "game_state", "board": state.get_board(), "turn": state.turn}))

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
