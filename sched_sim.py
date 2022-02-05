import sys
import collections

# have bash script call this python script

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
        cur_wait = total_time - job[2]
        total_time += job[1]
        cur_turnaround = total_time - job[2]
        avg_wait += cur_wait
        avg_turnaround += cur_turnaround
        print_job(job[0], cur_turnaround, cur_wait)
        job_count += 1
    print_avg(avg_turnaround / len(jobs), avg_wait / len(jobs))

# gets lists of all currently active jobs
def find_active(jobs, total_time):
    active_jobs = []
    for i in range(len(jobs)):
        if total_time >= jobs[i][2]:
            active_jobs.append(jobs[i])
    return active_jobs

# gets the job index based on the shortest remaining burst time
# as long as it has arrived (arrival time <= total time elapsed)
def index(jobs, total_time):
    active_jobs = find_active(jobs, total_time)
    if active_jobs == None or active_jobs == []:
        return None
    shortest_burst_index = 0
    shortest_burst = active_jobs[0][1]
    for i in range(len(active_jobs)):
        if active_jobs[i][1] < shortest_burst:
            shortest_burst = active_jobs[i][1]
            shortest_burst_index = i
        elif active_jobs[i][1] == shortest_burst: # if same remaining burst time, schedule job that came first
            if active_jobs[i][2] < active_jobs[shortest_burst_index][2]:
                shortest_burst = active_jobs[i][1]
                shortest_burst_index = i
    return shortest_burst_index

def sched_srtn(jobs):
    avg_turnaround = 0
    avg_wait = 0
    total_time = 0
    cur_job = 0
    job_count = len(jobs)
    wait_time = [0] * len(jobs)
    burst_time = [0] * len(jobs)

    while(len(jobs) >= 1):
        # if current job has finished running ie. it's burst time is now zero,
        # terminate it and move to next in queue. Print stats and add to avg stats as well.
        if cur_job != None and jobs[cur_job][1] <= 0:
            job_id = jobs[cur_job][0]
            cur_wait = wait_time[job_id]
            cur_turnaround = cur_wait + burst_time[job_id]
            avg_wait += cur_wait
            avg_turnaround += cur_turnaround
            print_job(job_id, cur_turnaround, cur_wait)
            jobs.pop(cur_job)
            if len(jobs) == 0:
                break

        cur_job = index(jobs, total_time)

        # decrease burst time of current job by 1 and increase total time elapsed by 1
        # if it was None there were no jobs available at current time, so just inc. time by 1
        if cur_job != None:
            jobs[cur_job][1] -= 1
        total_time += 1

        # increase wait time for every job that is waiting except current job cuz its running
        for i in jobs:
            if total_time > i[2]:
                wait_time[i[0]] += 1

        # increase burst time of current job if not None
        if cur_job != None:
            wait_time[jobs[cur_job][0]] -= 1
            burst_time[jobs[cur_job][0]] += 1

    print_avg(avg_turnaround / job_count, avg_wait / job_count)

def get_lst_idx(jobs, id):
    idx = -1

    for job in jobs:
        idx += 1
        if job[0] == id:
            return idx

    return -1

def is_in_rq (ready_queue, id):
    return id in ready_queue

def get_job_idx (jobs, id):
    for i in range(len(jobs)):
        if jobs[i][0] == id:
            return i

def sched_rr(jobs, q):
    ready_queue = collections.deque()
    curr_time = 0
    wait_time = [0] * len(jobs)
    burst_time = [0] * len(jobs)
    total_wait = 0
    total_burst = 0
    total_turnaround = 0
    num_jobs = len(jobs)

    while (len(jobs) >= 1):
        if len(ready_queue) == 0 and jobs[0][2] > curr_time:
            curr_time += 1
        else:
            # check if any jobs should be put in RQ
            for job in jobs:
                if job[2] <= curr_time and not is_in_rq(ready_queue, job[0]):
                    ready_queue.append(job[0])
            
            # execute first job in RQ
            curr_job = ready_queue[0]
            curr_job_idx = get_job_idx(jobs, curr_job)
            burst_time_left = jobs[get_job_idx(jobs, curr_job)][1]
            
            if burst_time_left - q < 0:
                execution_time = burst_time_left
                jobs.remove(jobs[curr_job_idx])
                curr_time += execution_time
                jobs[curr_job_idx].pop()          
            elif burst_time_left - q == 0:
                execution_time = q
                jobs.remove(jobs[curr_job_idx])
                curr_time += execution_time
                jobs[curr_job_idx].pop()
            else:
                execution_time = q
                jobs[curr_job_idx][1] -= q
                curr_time += execution_time
                # check if any jobs should be put in RQ
                for job in jobs:
                    if job[2] <= curr_time and not is_in_rq(ready_queue, job[0]):
                        ready_queue.append(job[0])
                ready_queue.pop()
                ready_queue.append(curr_job_idx)
            
            # update burst time for current job
            # update wait time for all other jobs in RQ
            burst_time[curr_job] += execution_time
            for i in range(len(wait_time)):
                if i != curr_job:
                    wait_time[i] += execution_time

    total_wait = sum(wait_time)
    total_burst = sum(burst_time)
    total_turnaround = total_wait + total_burst

    for i in range(num_jobs):
        print_job(i, wait_time[i] + burst_time[i], wait_time[i])

    for i in range(num_jobs):
        print_avg(total_turnaround / num_jobs, total_wait / num_jobs)
        
# sets algorithm or exits if multiple algorithms in cmd line args
def set_algo(algo, algo_match):
    if algo_match:
        usage()
        exit()
    else:
        algo_match = True
        return algo

def usage():
    print("Usage: schedSim <job-file.txt> -p <ALGORITHM> -q <QUANTUM>")

def main():
    num_args = len(sys.argv)
    algo_match = False
    q_match = False
    algo = 'FIFO'
    q = 1

    if num_args > 1:
        file_name = sys.argv[1]
        with open(file_name) as job_file:
            # for each line split into int list and sort by second column (arrival time)
            jobs = ([list(map(int, line.rstrip('\n').split())) for line in job_file])
            # add job ids in increasing order
            for i in range(len(jobs)):
                jobs[i].insert(0, i)
            # sort in order of arrival times
            jobs = sorted(jobs, key=lambda x: x[2])

    # cmd line arg parsing
    for i in range(1, num_args):
        if sys.argv[i] == 'FIFO':
            algo = set_algo('FIFO', algo_match)
        elif sys.argv[i] == 'SRTN':
            algo = set_algo('SRTN', algo_match)
        elif sys.argv[i] == 'RR':
            algo = set_algo('RR', algo_match)
        elif type(sys.argv[i]) is int:
            if q_match:
                usage()
                exit()
            else:
                q = sys.argv[i]

    #     elif num_args == 4 or num_args == 6:
    #         if sys.argv[2] == '-p' or sys.argv[2] == '-q':
    #             if sys.argv[3] == 'SRTN' or sys.argv[3] == 'FIFO' or sys.argv[3] == 'RR':
    #                 algo = sys.argv[3]
    #             elif sys.argv[3].isnumeric():
    #                 q = int(sys.argv[3])
    #             else:
    #                 sys.exit()
    #         else:
    #             sys.exit()

    #         if num_args == 6:
    #             if sys.argv[4] == '-p' or sys.argv[4] == '-q':
    #                 if sys.argv[5] == 'SRTN' or sys.argv[5] == 'FIFO' or sys.argv[3] == 'RR':
    #                     algo = sys.argv[5]
    #                 elif sys.argv[5].isnumeric():
    #                     q = int(sys.argv[5])
    #                 else:
    #                     sys.exit()
    #             else:
    #                 sys.exit()
    #     else:
    #         sys.exit()
    # else:
    #     sys.exit()

    if algo == 'SRTN':
        sched_srtn(jobs)
    if algo == 'FIFO':
        sched_fifo(jobs)
    if algo == 'RR':
        sched_rr(jobs, q)


if __name__ == '__main__':
    main()
