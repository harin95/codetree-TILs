from collections import deque

def rotate(sr, sc, d):
    # 회전 불가능
    if not 1 <= sr <= 3 or not 1 <= sc <= 3:
        return []

    # 변수 초기화
    copy_map = [[0 for _ in range(5)] for _ in range(5)]
    small_map = [[0 for _ in range(3)] for _ in range(3)]
    small_map_rotate = [[0 for _ in range(3)] for _ in range(3)]

    # 3*3 범위
    sm_row_idx = [sr - 1, sr, sr + 1]
    sm_col_idx = [sc - 1, sc, sc + 1]

    # 전체 맵 복사
    for r in range(5):
        for c in range(5):
            copy_map[r][c] = game_map[r][c]

    # 3*3 복사
    for sm_r, cp_r in enumerate(sm_row_idx):
        for sm_c, cp_c in enumerate(sm_col_idx):
            small_map[sm_r][sm_c] = game_map[cp_r][cp_c]

    # 회전
    if d == 0:  # 90도
        for r in range(3):
            for c in range(3):
                small_map_rotate[c][3-1-r] = small_map[r][c]
    elif d == 1:  # 180도
        for r in range(3):
            for c in range(3):
                small_map_rotate[3-1-r][3-1-c] = small_map[r][c]
    elif d == 2:  # 270도
        for r in range(3):
            for c in range(3):
                small_map_rotate[3-1-c][r] = small_map[r][c]

    # 회전 적용
    for sm_r, cp_r in enumerate(sm_row_idx):
        for sm_c, cp_c in enumerate(sm_col_idx):
            copy_map[cp_r][cp_c] = small_map_rotate[sm_r][sm_c]

    return copy_map


def is_in(r, c):
    if 0 <= r < 5 and 0 <= c < 5:
        return True
    return False


def bfs(copy_map, r, c, visit_tf):
    # 이미 방문
    if visit_tf[r][c]:
        return 0, []

    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    visit_list = []
    q = deque()
    q.append([r, c])
    visit_tf[r][c] = True
    visit_list.append([r, c])
    cnt = 1

    while q:
        cur = q.popleft()
        cur_num = copy_map[cur[0]][cur[1]]

        for dir in range(4):
            nr = cur[0] + dr[dir]
            nc = cur[1] + dc[dir]

            # 게임맵 밖일 경우, 게임판 숫자 같이 않을 경우, 이미 방문한 경우
            if not is_in(nr, nc) or copy_map[nr][nc] != cur_num or visit_tf[nr][nc]:
                continue
            q.append([nr, nc])
            visit_tf[nr][nc] = True
            visit_list.append([nr, nc])
            cnt += 1

    return cnt, visit_list


def get_point(copy_map):
    visit_tf = [[False for _ in range(5)] for _ in range(5)]
    visit_list = []
    point = 0

    for r in range(5):
        for c in range(5):
            res, visit_list_temp = bfs(copy_map, r, c, visit_tf)
            if res >= 3:    # 인접한 같은 숫자 3개 이상일 경우만
                point += res
                visit_list.extend(visit_list_temp)

    return point, visit_list


K, M = map(int, input().split())
game_map = []
for _ in range(5):
    game_map_temp = list(map(int, input().split()))
    game_map.append(game_map_temp)

yebi_blocks = deque(list(map(int, input().split())))
answer = []

for _ in range(K):
    turn_point = 0
    rotate_cases = []

    for r in range(5):
        for c in range(5):
            for d in range(3):
                copy_map = rotate(r, c, d)
                if not copy_map:
                    continue
                # 각 회전케이스마다 초기 점수랑 방문 좌표 저장
                point, visit_list = get_point(copy_map)
                rotate_cases.append([r, c, d, point, visit_list])

    rotate_cases.sort(key=lambda x: (-x[3], x[2], x[1], x[0]))  # 점수 높을수록(내림), 회전각도 작을수록(오름), 열 작을수록(오름), 행 작을수록(오름)
    best_case = rotate_cases[0]
    r, c, d, point, visit_list = best_case
    copy_map = rotate(r, c, d)  # 베스트 케이스 적용
    turn_point += point

    # 채우기
    visit_list.sort(key=lambda x: (x[1], -x[0]))  # 열 작은순(오름), 행번호 큰 순(내림)
    for pos in visit_list:
        r, c = pos
        copy_map[r][c] = yebi_blocks.popleft()

    # 추가점수 획득
    while point > 0:
        point, visit_list= get_point(copy_map)
        visit_list.sort(key=lambda x: (x[1], -x[0]))  # 열 작은순(오름), 행번호 큰 순(내림)
        for pos in visit_list:
            r, c = pos
            copy_map[r][c] = yebi_blocks.popleft()

        turn_point += point

    if turn_point == 0:
        break

    answer.append(str(turn_point))

    # 턴 적용
    game_map = copy_map

print(' '.join(answer))