import sys

def main():
    num_args = len(sys.argv)
    algo = 'FIFO'
    q = 1
    jobs = []

    if num_args > 1:
        file_name = sys.argv[1]

        with open(file_name) as job_file:
            lines = [lines.rstrip('\n') for line in job_file]
        
        for line in lines:
            tokens = line.split()
            token[0] = int(token[0])
            token[1] = int(token[1])
            jobs.append(tokens)

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
        sched_srtn(jobs, q)
    if algo == 'FIFO':
        sched_fifo(jobs, q)
    if algo == 'RR':
        sched_rr(jobs, q)


def sched_srtn(jobs, q):

def sched_fifo(jobs, q):

def sched_rr(jobs, q):


if __name__ == '__main__':
    main()