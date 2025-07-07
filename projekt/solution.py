def longcat(W, H, S, board):
    y, x = find_starting_position(board, H, W)
    board[y][x] = "#"
    return route(board, y, x, S)


def find_starting_position(board, H, W):
    for y in range(1, H-1):
        for x in range(1, W-1):
            if board[y][x] == "O":
                return y, x

          
def route(board, y, x, S, path = "", last = None):
    if S <= 0:
        return path
    
    # sprawdzenie ruchów pionowych
    if last != "V": 
        # w dół
        down = check_vertical_move(board, y, x, S, path, 1)
        if down is not None: return down

        # w górę
        up = check_vertical_move(board, y, x, S, path, -1)
        if up is not None: return up     

    # sprawdzenie ruchów poziomych
    if last != "H":
        # w prawo 
        right = check_horizontal_move(board, y, x, S, path, 1)
        if right is not None: return right

        # w lewo
        left = check_horizontal_move(board, y, x, S, path, -1)
        if left is not None: return left
        

def check_vertical_move(board, y, x, S, path, dir):
    # dir = 1 for south, -1 for north
    eaten = 0
    fin_y = y 
    old = []

    while board[fin_y+dir][x] in [".", "*"]:
        if board[fin_y+dir][x] == "*": eaten += 1
        fin_y += dir
        old.append(board[fin_y][x])
        board[fin_y][x] = "#"

    move = "D" if dir == 1 else "G"
    sol = route(board, fin_y, x, S - eaten, path + move, "V") if fin_y != y else None
    if sol is None:
        for i in range(dir * (fin_y - y)):
            board[y + dir*(i + 1)][x] = old[i]
    else: return sol


def check_horizontal_move(board, y, x, S, path, dir):
    # dir = 1 for east, -1 for west
    eaten = 0
    fin_x = x 
    old = []

    while board[y][fin_x+dir] in [".", "*"]:
        if board[y][fin_x+dir] == "*": eaten += 1
        fin_x += dir
        old.append(board[y][fin_x])
        board[y][fin_x] = "#"

    move = "P" if dir == 1 else "L"
    sol = route(board, y, fin_x, S - eaten, path + move, "H") if fin_x != x else None
    if sol is None:
        for i in range(dir * (fin_x - x)):
            board[y][x + dir*(i + 1)] = old[i]
    else: return sol


if __name__ == "__main__":
    W, H, S = map(int, input().split())
    board = []

    for i in range(H):
        board.append(list(input()))

    print(longcat(W, H, S, board))
