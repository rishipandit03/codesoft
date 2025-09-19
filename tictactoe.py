from typing import List, Optional, Tuple

Board = List[str]

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6)              # diagonals
]


def print_board(board: Board) -> None:
    def cell(i):
        return board[i] if board[i] != " " else str(i + 1)
    row = lambda r: f" {cell(3*r)} | {cell(3*r+1)} | {cell(3*r+2)} "
    sep = "---+---+---"
    print("\n" + row(0))
    print(sep)
    print(row(1))
    print(sep)
    print(row(2) + "\n")


def available_moves(board: Board) -> List[int]:
    return [i for i, c in enumerate(board) if c == " "]


def winner(board: Board) -> Optional[str]:
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: Board) -> bool:
    return winner(board) is None and all(c != " " for c in board)


def minimax(board: Board,
            depth: int,
            alpha: int,
            beta: int,
            maximizing: bool,
            ai: str,
            human: str) -> Tuple[int, Optional[int]]:
    """
    Returns (score, move_index). Score is from AI's perspective.
    Terminal scoring uses depth so AI prefers faster wins and slower losses.
    """
    win = winner(board)
    if win == ai:
        return 10 - depth, None
    elif win == human:
        return depth - 10, None
    elif is_draw(board):
        return 0, None

    if maximizing:
        best_score = -10**9
        best_move = None
        for move in available_moves(board):
            board[move] = ai
            score, _ = minimax(board, depth + 1, alpha, beta, False, ai, human)
            board[move] = " "
            if score > best_score:
                best_score, best_move = score, move
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = 10**9
        best_move = None
        for move in available_moves(board):
            board[move] = human
            score, _ = minimax(board, depth + 1, alpha, beta, True, ai, human)
            board[move] = " "
            if score < best_score:
                best_score, best_move = score, move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score, best_move


def get_ai_move(board: Board, ai: str, human: str) -> int:
    # First move opportunism: take center if free, else a corner — speeds up search
    if board.count(" ") == 9:
        return 4  # center
    if board[4] == " ":
        return 4
    score, move = minimax(board, 0, -10*9, 10*9, True, ai, human)
    assert move is not None
    return move


def get_human_move(board: Board) -> int:
    while True:
        raw = input("Your move (1-9): ").strip()
        if not raw.isdigit():
            print("Please enter a number between 1 and 9.")
            continue
        pos = int(raw) - 1
        if pos < 0 or pos > 8:
            print("Position must be between 1 and 9.")
            continue
        if board[pos] != " ":
            print("That cell is already taken. Choose another.")
            continue
        return pos


def play_game():
    board: Board = [" "] * 9
    print("\n=== Tic-Tac-Toe AI (Unbeatable) ===")
    print("Choose your symbol: X or O")
    human = ""
    while human not in ("X", "O"):
        human = input("You are (X/O): ").upper().strip()
    ai = "O" if human == "X" else "X"

    human_turn = True if human == "X" else False
    print_board(board)

    while True:
        if human_turn:
            pos = get_human_move(board)
            board[pos] = human
        else:
            print("AI is thinking...")
            pos = get_ai_move(board, ai, human)
            board[pos] = ai
            print(f"AI played at position {pos + 1}.")

        print_board(board)

        w = winner(board)
        if w:
            if w == human:
                print("You win! (This should be rare 😅)")
            else:
                print("AI wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        human_turn = not human_turn

    print("Game over. Thanks for playing!")


def main():
    while True:
        play_game()
        again = input("Play again? (y/n): ").lower().strip()
        if again != "y":
            print("Goodbye!")
            break


if _name_ == "_main_":
    main()