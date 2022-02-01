import sys

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

def sched_srtn(jobs):
    return

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