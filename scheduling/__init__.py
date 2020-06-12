from collections import deque


def chu_ky_1(at, cpu1, q, time, process, time_r1, process_r1, time_r2, process_r2, io1):
    queue = deque([])
    t = 0
    da_lay = 0
    len_at = len(at)
    p = None
    dau = [False] * len_at
    while 1:
        done = True
        while da_lay <= len_at:
            for i in range(len_at):
                if at[i] <= t and dau[i] == False:
                    queue.append(cpu1[i])
                    dau[i] = True
                    da_lay += 1
            break
        if p is not None:
            queue.append(p)
        if len(queue) >= 1:
            done = False
            # print(queue)
            p = queue.popleft()
            process.append(p[0])
            time.append(p[0] * -1)
            if p[1] >= q:
                t += q
                p[1] -= q
            else:
                t += p[1]
                p[1] -= p[1]
            if p[1] == 0:
                if io1[p[0] - 1][1] == 0:
                    process_r1.append(p[0])
                    check_add_fcfs_on_R(t, time_r1, io1, p)
                else:
                    process_r2.append(p[0])
                    check_add_fcfs_on_R(t, time_r2, io1, p)
                p = None

            time.append(t)
        else:
            p = None
        if done:
            break


def chu_ky_2(cpu2, q, time, process, time_r1, process_r1, time_r2, process_r2, io2):
    queue = deque([])
    vtri_r2 = 0
    vtri_r1 = 0
    gt_dau_r1 = max(time_r1)
    gt_dau_r2 = max(time_r2)
    p = None
    da_lay = [False] * max(gt_dau_r1, gt_dau_r2)
    while 1:
        done = True
        t = time[len(time) - 1]
        while (time_r1[vtri_r1] < gt_dau_r1 and time_r2[vtri_r2] < gt_dau_r2) and (
                time_r1[vtri_r1] <= t or time_r2[vtri_r2] <= t):
            if not da_lay[(time_r1[vtri_r1] * -1) - 1] and not da_lay[(time_r2[vtri_r2] * -1) - 1]:
                if time_r1[vtri_r1] < 0 and time_r2[vtri_r2] < 0 and time_r1[vtri_r1 + 1] <= time_r2[vtri_r2 + 1] and \
                        time_r1[vtri_r1 + 1] <= t and time_r1[vtri_r1 + 1] <= gt_dau_r1:
                    t1 = time_r1[vtri_r1] * -1
                    if not da_lay[t1 - 1]:
                        add_queue(cpu2, t1, queue, da_lay)
                        if time_r1[vtri_r1 + 1] < gt_dau_r1:
                            vtri_r1 += 1
                elif time_r2[vtri_r2] < 0 and time_r1[vtri_r1] < 0 and time_r2[vtri_r2 + 1] < time_r1[vtri_r1 + 1] and \
                        time_r2[vtri_r2 + 1] <= t and time_r2[vtri_r2 + 1] <= gt_dau_r2:
                    t2 = time_r2[vtri_r2] * -1
                    if not da_lay[t2 - 1]:
                        add_queue(cpu2, t2, queue, da_lay)
                        if time_r2[vtri_r2 + 1] < gt_dau_r2:
                            vtri_r2 += 1
                else:
                    t1 = time_r1[vtri_r1] * -1
                    t2 = time_r2[vtri_r2] * -1
                    if time_r1[vtri_r1] >= 0:
                        if time_r1[vtri_r1] < gt_dau_r1:
                            vtri_r1 += 1
                    else:
                        if da_lay[(t1 - 1)]:
                            vtri_r1 += 1
                    if time_r2[vtri_r2] >= 0:
                        if time_r2[vtri_r2] < gt_dau_r2:
                            vtri_r2 += 1
                    else:
                        if da_lay[(t2 - 1)]:
                            vtri_r2 += 1
            elif not da_lay[(time_r1[vtri_r1] * -1) - 1] or time_r1[vtri_r1] > 0:
                t1 = time_r1[vtri_r1] * -1
                if time_r1[vtri_r1] < 0 and time_r2[vtri_r2] < 0 and time_r1[vtri_r1 + 1] <= gt_dau_r1:
                    if not da_lay[t1 - 1] and time_r1[vtri_r1 + 1] <= t:
                        add_queue(cpu2, t1, queue, da_lay)
                        if time_r1[vtri_r1 + 1] < gt_dau_r1:
                            vtri_r1 += 1
                else:
                    vtri_r1 += 1
            elif not da_lay[(time_r2[vtri_r2] * -1) - 1] or time_r2[vtri_r2] > 0:
                t2 = time_r2[vtri_r2] * -1
                if time_r2[vtri_r2] < 0 and time_r1[vtri_r1] < 0 and time_r2[vtri_r2 + 1] <= gt_dau_r2:
                    if not da_lay[t2 - 1] and time_r2[vtri_r2 + 1] <= t:
                        add_queue(cpu2, t2, queue, da_lay)
                        if time_r2[vtri_r2 + 1] < gt_dau_r2:
                            vtri_r2 += 1
                else:
                    vtri_r2 += 1
            if time_r1[vtri_r1] < 0 and time_r2[vtri_r2] < 0:
                if (da_lay[(time_r1[vtri_r1] * -1) - 1] or time_r1[vtri_r1 + 1] > t) and (
                        da_lay[(time_r2[vtri_r2] * -1) - 1] or time_r2[vtri_r2 + 1] > t):
                    break

        if p is not None:
            queue.append(p)
        if len(queue) >= 1:
            done = False
            p = queue.popleft()
            process.append(p[0])
            time.append(p[0] * -1)
            if p[1] >= q:
                t += q
                p[1] -= q
            else:
                t += p[1]
                p[1] -= p[1]
            if p[1] == 0:
                if io2[p[0] - 1][1] == 0:
                    process_r1.append(p[0])
                    check_add_fcfs_on_R(t, time_r1, io2, p)
                else:
                    process_r2.append(p[0])
                    check_add_fcfs_on_R(t, time_r2, io2, p)
                p = None
            time.append(t)
        else:
            p = None
        if done:
            break


def pop_queue_add_time(p_0, t_0, time_r1_0, time_r2_0, io_0, done_0, process_0, time_0, q_0, process_r1_0, process_r2_0):
        process_0.append(p_0[0])
        time_0.append(p_0[0] * -1)
        if p_0[1] >= q_0:
            t_0 += q_0
            p_0[1] -= q_0
        else:
            t_0 += p_0[1]
            p_0[1] -= p_0[1]
        if p_0[1] == 0:
            if io_0[p_0[0] - 1][1] == 0:
                process_r1_0.append(p_0[0])
                check_add_fcfs_on_R(t_0, time_r1_0, io_0, p_0)
            else:
                process_r2_0.append(p_0[0])
                check_add_fcfs_on_R(t_0, time_r2_0, io_0, p_0)
            p_0 = None
        time_0.append(t_0)


def add_queue(cpu, t, queue, da_lay):
    for i in range(len(cpu)):
        if cpu[i][0] == t:
            queue.append(cpu[i])
            da_lay[i] = True
            break


def check_add_fcfs_on_R(t, time, io, p):
    vt = len(time)
    if vt != 0:
        if t > time[vt - 1]:
            time.append(t)
            time.append(-p[0])
            time.append(t + io[p[0] - 1][0])
        else:
            time.append(-p[0])
            time.append(time[vt - 1] + io[p[0] - 1][0])
    else:
        time.append(t)
        time.append(-p[0])
        time.append(t + io[p[0] - 1][0])


def print_time(time, R1):
    print("\n" + R1 + ":\t", end='')
    t = int(time[len(time) - 1])
    for i in range(len(time)):
        if i < len(time) - 2:
            if time[i] > 0 and time[i + 2] == time[i]:
                i += 2
                continue
        if time[i] < 0 and time[i] < t:
            print('P' + str(time[i] * -1), end='_')
        else:
            if time[i] == t:
                print(time[i])
            else:
                print(time[i], end='_')


if __name__ == '__main__':
    cpu10 = []
    io10 = []
    cpu20 = []
    io20 = []
    at0 = []

    f0 = open('C:/Users/nguye/OneDrive/Desktop/Scheduler2.txt', 'r')
    q0 = int(f0.readline())
    content = f0.readlines()
    for i in content:
        p0 = int(i.split('\t')[0])
        cpu10.append([p0, int(i.split('\t')[2])])
        io10.append((int(i.split('\t')[3]), int(i.split('\t')[4])))
        cpu20.append([p0, int(i.split('\t')[5])])
        io20.append((int(i.split('\t')[6]), int(i.split('\t')[7])))
        at0.append(int(i.split('\t')[1]))

    print('Quantum = ', q0)
    print('CPU 1:\t', cpu10)
    print('IO 1:\t', io10)
    print('CPU 2:\t', cpu20)
    print('IO 2:\t', io20)
    print('Arrival Time: ', at0)
    f0.close()

    print('\n######################################################################################################')
    time0 = [0]
    process0 = []
    time_r10 = []
    process_r10 = []
    time_r20 = []
    process_r20 = []

    chu_ky_1(at0, cpu10, q0, time0, process0, time_r10, process_r10, time_r20, process_r20, io10)
    chu_ky_2(cpu20, q0, time0, process0, time_r10, process_r10, time_r20, process_r20, io20)

    print_time(time0, R1='CPU')
    print_time(time_r10, R1='R1 ')
    print_time(time_r20, R1='R2 ')
