L, Q = map(int, input().split())
sushi_cnt = 0
customer_cnt = 0

all_q = []
make_sushi_q = dict()
new_customer_q = dict()

for _ in range(Q):
    cmd = list(input().split(" "))
    all_q.append([cmd[0], int(cmd[1])])     # 명령 종류와 시간만 저장 (시간은 정렬에 사용)

    if cmd[0] == '100':
        t, x = map(int, cmd[1:3])
        name = cmd[3]
        if name not in make_sushi_q:
            make_sushi_q[name] = []
        make_sushi_q[name].append([t, x])

    elif cmd[0] == '200':
        t, x = map(int, cmd[1:3])
        name = cmd[3]
        new_customer_q[name] = [t, x, -1]     # -1은 퇴장시간 초기화

# 초밥 먹는 시간 계산
for name in make_sushi_q:
    customer_t, customer_x, customer_out_t = new_customer_q[name]
    for sushi_info in make_sushi_q[name]:
        sushi_t, sushi_x = sushi_info
        # 스시가 먼저 올라온 경우 시간 맞추기
        if sushi_t < customer_t:
            sushi_x = (sushi_x + (customer_t - sushi_t)) % L
        # 스시 먹을 시간 계산
        time_to_eat = max(customer_t, sushi_t) + ((customer_x - sushi_x + L) % L)
        new_customer_q[name][2] = max(new_customer_q[name][2], time_to_eat)     # 마지막 초밥 먹는 시간 = 퇴장시간

        # 초밥 먹기 명령 추가
        all_q.append(['111', int(time_to_eat)])

# 퇴장 명령 추가
for name in new_customer_q:
    out_time = new_customer_q[name][2]
    all_q.append(['222', int(out_time)])

all_q.sort(key=lambda x : (x[1], x[0])) # 시간, 명령어순 오름차순 정렬

for cmd, t in (all_q):
    if cmd == '100':
        sushi_cnt += 1
    elif cmd == '111':
        sushi_cnt -= 1
    elif cmd == '200':
        customer_cnt += 1
    elif cmd == '222':
        customer_cnt -= 1
    else:
        print(f"{customer_cnt} {sushi_cnt}")