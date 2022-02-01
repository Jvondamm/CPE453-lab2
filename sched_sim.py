import sys
from textwrap import shorten

def print_job(a, b, c):
    print('Job {0:03d} -- '.format(a), end='')
    print('Turnaround {:.2f}  Wait {:.2f}'.format(b, c))

def print_avg(a, b):
    print('Average -- Turnaround {:.2f}  Wait {:.2f}'.format(a, b))

def sched_fifo(jobs):
    avg_turnaround = 0
    avg_wait = 0
    total_time = 0
    job_count = 0
    for job in jobs:
        cur_wait = total_time
        total_time += job[0]
        cur_turnaround = total_time
        avg_wait += cur_wait
        avg_turnaround += cur_turnaround
        print_job(job_count, cur_turnaround, cur_wait)
        job_count += 1
    print_avg(avg_turnaround / len(jobs), avg_wait / len(jobs))

# gets the job index based on the shortest remaining burst time
# as long as it has arrived (arrival time <= total time elapsed)
def find_shortest_index(jobs, total_time):
    init_index = None
    for i in range(len(jobs)):
        if total_time >= jobs[i][2]:
            init_index = i
            break
    if init_index == None:
        return None
    else:
        shortest = jobs[init_index][1]

    for i in range(len(jobs)):
        if jobs[i][1] < shortest and total_time >= jobs[i][2]:
            return i
    return init_index

def sched_srtn(jobs):
    avg_turnaround = 0
    avg_wait = 0
    total_time = 0
    cur_job = 0
    job_count = len(jobs)
    wait_time = [0] * len(jobs)
    burst_time = [0] * len(jobs)

    # add job ids in increasing order
    for i in range(len(jobs)):
        jobs[i].insert(0, i)

    while(len(jobs) >= 1):
        # if current job has finished running ie. it's burst time is now zero,
        # terminate it and move to next in queue. Print stats and add to avg stats as well.
        if jobs[cur_job][1] <= 0:
            job_id = jobs[cur_job][0]
            cur_wait = wait_time[job_id]
            cur_turnaround = cur_wait + burst_time[job_id]
            avg_wait += cur_wait
            avg_turnaround += cur_turnaround
            print_job(job_id, cur_turnaround, cur_wait)
            jobs.pop(cur_job)
            if len(jobs) == 0:
                break

        cur_job = find_shortest_index(jobs, total_time)

        # decrease burst time of current job by 1 and increase total time elapsed by 1
        jobs[cur_job][1] -= 1
        total_time += 1

        # increase wait time for every job except current job cuz its running
        # increase burst time of curret job
        wait_time = [x + 1 for x in wait_time]
        wait_time[jobs[cur_job][0]] -= 1
        burst_time[jobs[cur_job][0]] += 1

    print_avg(avg_turnaround / job_count, avg_wait / job_count)

def sched_rr(jobs, q):
    return


def main():
    num_args = len(sys.argv)
    algo = 'FIFO'
    q = 1

    if num_args > 1:
        file_name = sys.argv[1]
        with open(file_name) as job_file:
            # for each line split into int list and sort by second column (arrival time)
            jobs = sorted(([list(map(int, line.rstrip('\n').split())) for line in job_file]), key=lambda x: x[1])

        if num_args == 2:
            sched_fifo(jobs, q)
        elif num_args == 4 or num_args == 6:
            if sys.argv[2] == '-p' or sys.argv[2] == '-q':
                if sys.argv[3] == 'SRTN' or sys.argv[3] == 'FIFO' or sys.argv[3] == 'RR':
                    algo = sys.argv[3]
                elif sys.argv[3].isnumeric():
                    q = int(sys.argv[3])
                else:
                    sys.exit()
            else:
                sys.exit()

            if num_args == 6:
                if sys.argv[4] == '-p' or sys.argv[4] == '-q':
                    if sys.argv[5] == 'SRTN' or sys.argv[5] == 'FIFO' or sys.argv[3] == 'RR':
                        algo = sys.argv[5]
                    elif sys.argv[5].isnumeric():
                        q = int(sys.argv[5])
                    else:
                        sys.exit()
                else:
                    sys.exit()
        else:
            sys.exit()
    else:
        sys.exit()

    if algo == 'SRTN':
        sched_srtn(jobs)
    if algo == 'FIFO':
        sched_fifo(jobs)
    if algo == 'RR':
        sched_rr(jobs, q)


if __name__ == '__main__':
    main()