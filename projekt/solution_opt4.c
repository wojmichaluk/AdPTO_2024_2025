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

void determine_gains(char* board, int* gains, int H, int W) {
    // ustawienie zer w tablicy
    for(int i = 0; i < 4*W*H; i++) {
        gains[i] = 0;
    }

    for(int y = 1; y < H-1; y++) {
        for(int x = 1; x < W-1; x++) {
            if(_board_(y, x) != '#') {
                int thisFieldGains = _board_(y, x) == '*' ? 1 : 0;
                gains[y*W + x] = gains[y*W + x-1] + thisFieldGains;
                gains[2*W*H + y*W + x] = gains[2*W*H + (y-1)*W + x] + thisFieldGains;

                for(int i = x; i < W-1; i++)
                    gains[W*H + y*W + x] += _board_(y, i) == '*' ? 1 : 0;

                for(int i = y; i < H-1; i++)
                    gains[3*W*H + y*W + x] += _board_(i, x) == '*' ? 1 : 0;
            }
        }
    }
}

int route(char*, int*, int, int, int, int, int, char*, char, int);

int checkVerticalMove(
    char* board, int* gains, int y, int x, int W, int H, int S, char* path, int level, int dir) {
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
    int sol = finY != y ? route(board, gains, finY, x, W, H, S - eaten, path, 'V', level+1) : 0;
    if(!sol) {
        for(int i = 0; i < dir * (finY - y); i++)
            _board_(y + dir*(i + 1), x) = old[i];
    }
    return sol;
}

int checkHorizontalMove(
    char* board, int* gains, int y, int x, int W, int H, int S, char* path, int level, int dir) {
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
    int sol = finX != x ? route(board, gains, y, finX, W, H, S - eaten, path, 'H', level+1) : 0;
    if(!sol) {
        for(int i = 0; i < dir * (finX - x); i++)
            _board_(y, x + dir*(i + 1)) = old[i];
    }
    return sol;
}

int route(
    char* board, int* gains, int y, int x, int W, int H, int S, char* path, char last, int level) {
    if(S <= 0) {
        path[level] = '\0';
        return 1;
    }

    // sprawdzenie ruchów pionowych
    if(last != 'V') {
        if(gains[3*W*H + y*W + x] > gains[2*W*H + y*W + x]) {
            // w dół
            if(checkVerticalMove(board, gains, y, x, W, H, S, path, level, 1))
                return 1;

            // w górę
            if(checkVerticalMove(board, gains, y, x, W, H, S, path, level, -1))
                return 1;
        } else {
            // w górę
            if(checkVerticalMove(board, gains, y, x, W, H, S, path, level, -1))
                return 1;

            // w dół
            if(checkVerticalMove(board, gains, y, x, W, H, S, path, level, 1))
                return 1;
        }        
    }

    // sprawdzenie ruchów poziomych
    if(last != 'H') {
        if(gains[W*H + y*W + x] > gains[y*W + x]) {
            // w prawo
            if(checkHorizontalMove(board, gains, y, x, W, H, S, path, level, 1))
                return 1;

            // w lewo
            if(checkHorizontalMove(board, gains, y, x, W, H, S, path, level, -1))
                return 1;
        } else {
            // w lewo
            if(checkHorizontalMove(board, gains, y, x, W, H, S, path, level, -1))
                return 1;

            // w prawo
            if(checkHorizontalMove(board, gains, y, x, W, H, S, path, level, 1))
                return 1;
        }
    }

    return 0;
}

void longcat(int W, int H, int S, char* board) {
    int startPos = findStartingPosition(board, H, W);
    int y = startPos / W;
    int x = startPos % W;

    char path[W * H];
    int gains[4 * W * H];
    determine_gains(board, gains, H, W);
    _board_(y, x) = '#';
    route(board, gains, y, x, W, H, S, path, 'X', 0);
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
