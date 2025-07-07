#include <stdio.h>
#include <stdlib.h>

#define _board(y, x) (board[(y)*(W) + (x)])
#define _board_(y, x) (ca->board[(y)*(ca->W) + (x)])

typedef struct {
    char* board;
    int y;
    int x;
    int W;
    int H;
    int S;
    char* path;
} CommonArgs;

int findStartingPosition(char* board, int H, int W) {
    for(int y = 1; y < H-1; y++) {
        for(int x = 1; x < W-1; x++) {
            if(_board(y, x) == 'O')
                return y*W + x;
        }
    }
}

int route(CommonArgs*, char, int);

int checkVerticalMove(CommonArgs* ca, int level, int dir) {
    // dir = 1 dla ruchu w dół, -1 dla ruchu w górę
    int eaten = 0;
    int finY = ca->y;
    char old[ca->W + ca->H];
    int oldInd = 0;

    while(_board_(finY+dir, ca->x) == '.' || _board_(finY+dir, ca->x) == '*') {
        if(_board_(finY+dir, ca->x) == '*') eaten++;
        finY += dir;
        old[oldInd++] = _board_(finY, ca->x);
        _board_(finY, ca->x) = '#';
    }

    int oldY = ca->y;
    int oldS = ca->S;

    ca->path[level] = dir == 1 ? 'D' : 'G';
    ca->y = finY;
    ca->S -= eaten;

    int sol = finY != oldY ? route(ca, 'V', level+1) : 0;
    if(!sol) {
        ca->y = oldY;
        ca->S = oldS;
        for(int i = 0; i < dir * (finY - ca->y); i++)
            _board_(ca->y + dir*(i + 1), ca->x) = old[i];
    }
    return sol;
}

int checkHorizontalMove(CommonArgs* ca, int level, int dir) {
    // dir = 1 dla ruchu w prawo, -1 dla ruchu w lewo
    int eaten = 0;
    int finX = ca->x;
    char old[ca->W + ca->H];
    int oldInd = 0;

    while(_board_(ca->y, finX+dir) == '.' || _board_(ca->y, finX+dir) == '*') {
        if(_board_(ca->y, finX+dir) == '*') eaten++;
        finX += dir;
        old[oldInd++] = _board_(ca->y, finX);
        _board_(ca->y, finX) = '#';
    }

    int oldX = ca->x;
    int oldS = ca->S;

    ca->path[level] = dir == 1 ? 'P' : 'L';
    ca->x = finX;
    ca->S -= eaten;

    int sol = finX != oldX ? route(ca, 'H', level+1) : 0;
    if(!sol) {
        ca->x = oldX;
        ca->S = oldS;
        for(int i = 0; i < dir * (finX - ca->x); i++)
            _board_(ca->y, ca->x + dir*(i + 1)) = old[i];
    }
    return sol;
}

int route(CommonArgs* ca, char last, int level) {
    if(ca->S <= 0) {
        ca->path[level] = '\0';
        return 1;
    }

    // sprawdzenie ruchów pionowych
    if(last != 'V') {
        // w dół
        if(checkVerticalMove(ca, level, 1))
            return 1;

        // w górę
        if(checkVerticalMove(ca, level, -1))
            return 1;
    }

    // sprawdzenie ruchów poziomych
    if(last != 'H') {
        // w prawo
        if(checkHorizontalMove(ca, level, 1))
            return 1;

        // w lewo
        if(checkHorizontalMove(ca, level, -1))
            return 1;
    }

    return 0;
}

void longcat(int W, int H, int S, char* board) {
    int startPos = findStartingPosition(board, H, W);
    int y = startPos / W;
    int x = startPos % W;
    _board(y, x) = '#';

    char path[W * H];
    CommonArgs ca = { board, y, x, W, H, S, path };
    route(&ca, 'X', 0);
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
