#include <stdio.h>
#include <stdlib.h>

#define _board_(y, x) (board[(y)*W + (x)])

int findStartingPosition(char* board, int H, int W) {
    for(int y = 1; y < H-1; y++) {
        for(int x = 1; x < W-1; x++) {
            if(_board_(y, x) == 'O')
                return y*W + x;
        }
    }
}

int route(char*, int, int, int, int, int, char*, char, int);

int checkVerticalMove(
    char* board, int y, int x, int W, int H, int S, char* path, int level, int dir) {
    // dir = 1 dla ruchu w dół, -1 dla ruchu w górę
    int eaten = 0;
    int finY = y;
    char old[W + H];
    int oldInd = 0;

    while(_board_(finY+dir, x) == '.' || _board_(finY+dir, x) == '*') {
        if(_board_(finY+dir, x) == '*') eaten++;
        finY += dir;
        old[oldInd++] = _board_(finY, x);
        _board_(finY, x) = '#';
    }

    path[level] = dir == 1 ? 'D' : 'G';
    int sol = finY != y ? route(board, finY, x, W, H, S - eaten, path, 'V', level+1) : 0;
    if(!sol) {
        for(int i = 0; i < dir * (finY - y); i++)
            _board_(y + dir*(i + 1), x) = old[i];
    }
    return sol;
}

int checkHorizontalMove(
    char* board, int y, int x, int W, int H, int S, char* path, int level, int dir) {
    // dir = 1 dla ruchu w prawo, -1 dla ruchu w lewo
    int eaten = 0;
    int finX = x;
    char old[W + H];
    int oldInd = 0;

    while(_board_(y, finX+dir) == '.' || _board_(y, finX+dir) == '*') {
        if(_board_(y, finX+dir) == '*') eaten++;
        finX += dir;
        old[oldInd++] = _board_(y, finX);
        _board_(y, finX) = '#';
    }

    path[level] = dir == 1 ? 'P' : 'L';
    int sol = finX != x ? route(board, y, finX, W, H, S - eaten, path, 'H', level+1) : 0;
    if(!sol) {
        for(int i = 0; i < dir * (finX - x); i++)
            _board_(y, x + dir*(i + 1)) = old[i];
    }
    return sol;
}

int route(
    char* board, int y, int x, int W, int H, int S, char* path, char last, int level) {
    if(S <= 0) {
        path[level] = '\0';
        return 1;
    }

    // sprawdzenie ruchów pionowych
    if(last != 'V') {
        // w dół
        if(checkVerticalMove(board, y, x, W, H, S, path, level, 1))
            return 1;

        // w górę
        if(checkVerticalMove(board, y, x, W, H, S, path, level, -1))
            return 1;
    }

    // sprawdzenie ruchów poziomych
    if(last != 'H') {
        // w prawo
        if(checkHorizontalMove(board, y, x, W, H, S, path, level, 1))
            return 1;

        // w lewo
        if(checkHorizontalMove(board, y, x, W, H, S, path, level, -1))
            return 1;
    }

    return 0;
}

void longcat(int W, int H, int S, char* board) {
    int startPos = findStartingPosition(board, H, W);
    int y = startPos / W;
    int x = startPos % W;
    _board_(y, x) = '#';

    char path[W * H];
    route(board, y, x, W, H, S, path, 'X', 0);
    printf("%s\n", path);
}

int main(void) {
    int W, H, S, temp;
    temp = scanf("%d %d %d", &W, &H, &S);
    char board[W * H];

    for(int i = 0; i < H; i++)
        temp = scanf("%s", board + i*W);

    longcat(W, H, S, board);
    return 0;
}
