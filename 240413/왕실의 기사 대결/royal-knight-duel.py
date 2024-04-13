from collections import deque

class Knight:
    def __init__(self,num, r, c, h, w, k):
        self.num = num
        self.r = r
        self.c = c
        self.h = h
        self.w = w
        self.k = k


def isIn(r, c):
    if 0 <= r < L and 0 <= c < L:
        return True
    return False


def move_knight(num, d):
    after_move = []
    q = deque()

    # 명령받은 기사 추가
    q.append(knights[num])

    # 이동 후 이동한 위치에 겹치는 기사가 있는지 확인 (큐로 연쇄 반응)
    while q:
        cur = q.popleft()
        nr = cur.r + dr[d]      # 이동
        nc = cur.c + dc[d]

        # 범위 밖으로 이동한 경우
        if not isIn(nr, nc) or not isIn(nr + cur.h - 1, nc + cur.w - 1):
            return []

        # 벽이 포함된 경우
        for row in range(nr, nr + cur.h):
            for col in range(nc, nc + cur.w):
                if chess[row][col] == 2:
                    return []

        after_move.append(Knight(cur.num, nr, nc, cur.h, cur.w, cur.k))

        row_cmp = [0]*L
        col_cmp = [0]*L

        # cur 기사 이동한 위치 표시
        for row in range(nr, nr + cur.h):
            row_cmp[row] += 1
        for col in range(nc, nc + cur.w):
            col_cmp[col] += 1

        # 기존 기사들과 위치 비교
        for knight in knights:
            if not inChess[knight.num] or knight.num == cur.num:     # 체스판에서 사라진 경우 or 자기자신은 제외
                continue

            # 비교 기사 범위 표시
            row_cnt, col_cnt = 0, 0
            for row in range(knight.r, knight.r + knight.h):
                row_cmp[row] += 1
                if row_cmp[row] > 1:
                    row_cnt += 1
            for col in range(knight.c, knight.c + knight.w):
                col_cmp[col] += 1
                if col_cmp[col] > 1:
                    col_cnt += 1

            # 겹치는 부분이 있으면 얘도 밀려남
            if row_cnt > 0 and col_cnt > 0:
                q.append(knight)

            # 되돌리기
            for row in range(knight.r, knight.r + knight.h):
                row_cmp[row] -= 1
            for col in range(knight.c, knight.c + knight.w):
                col_cmp[col] -= 1

    return after_move


# 상 우 하 좌
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

L, N, Q = map(int, input().split())
chess = []
for _ in range(L):
    chess_input = list(map(int, input().split()))
    chess.append(chess_input)

knights = []
for i in range(N):
    r, c, h, w, k = map(int, input().split())
    knights.append(Knight(i, r-1, c-1, h, w, k))

damage = [0] * N
inChess = [True] * N

for idx in range(Q):
    num, d = map(int, input().split())

    # 체스 밖의 기사는 명령 받지 않음
    if not inChess[num-1]:
        continue

    after_move = move_knight(num-1, d)
    if not after_move:  # 끝에 벽이 있는 경우 - 모든 기사가 움직이지 못함
        continue

    for knight in after_move:
        # 위치 업데이트
        knights[knight.num].r = knight.r
        knights[knight.num].c = knight.c

        if knight.num == num-1:   # 명령 받은 기사는 피해 입지 않음
            continue

        dmg_cnt = 0
        for r in range(knight.r, knight.r + knight.h):
            for c in range(knight.c, knight.c + knight.w):
                if chess[r][c] == 1:
                    dmg_cnt += 1

        # 피해 업데이트
        damage[knight.num] += dmg_cnt

        # 체력 업데이트
        knights[knight.num].k -= dmg_cnt
        # 체력 다하면 사라짐
        if knights[knight.num].k <= 0:
            inChess[knight.num] = False

# 생존한 기사들의 데미지 합
tot_damage = 0
for i in range(N):
    if inChess[i]:
        tot_damage += damage[i]

print(tot_damage)