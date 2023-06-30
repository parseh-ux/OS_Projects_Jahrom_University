import sys

from load_data import load_data
from generate_output import generate_output
from utils import proc_insert

# Get the input file from the first command line argument and load its data.
if len(sys.argv) < 2:
    sys.exit("name of the input file must be given as a command line argument.")
    
q, dl, new = load_data(fname=sys.argv[1])

# Sort the processes in `new` based on their names.
new.sort(key=lambda x: x.pname)

# Shifts all processes to make the first process start from time 0.
first_proc = min([p.arrival_time for p in new])
for p in new:
    p.arrival_time -= first_proc

rr = []
sjf = []
waiting = []
complete = []
current_proc = None

time = 0
total_waiting_time = 0
cycles = []         # Store what happens in each clock cycle.
process_count = len(new)
temp_dl = 0         # In the case of a context switch, holds a temporary dispatch latency
                    # that decrements by 1 at every clock cycle to keep track of how much
                    # time is left for each dl.

temp_q = q          # Holds the remaining time quantum of the current process.

while True:
    # THE Mazloom Navazi Principle
    # Insert processes into their respective queue if the arrival time is reached.
    for p in new[:]:          
        if p.arrival_time == time:
            proc_insert(p, rr, sjf)
            new.remove(p)


    # Remove a process from the waiting queue and add it back
    # to its respective queue if it finished its IO.
    waiting.sort(key=lambda x: x.pname)
    for p in waiting[:]:
        if p.bursts[0] == 0:
            p.bursts.pop(0)
            proc_insert(p, rr, sjf)
            waiting.remove(p)


    # If current process has reached its quantum limit get the CPU back from it.
    if current_proc and current_proc.finished_q_flag:
        current_proc.finished_q_flag = False
        proc_insert(current_proc, rr, sjf)
        current_proc = None


    # Give the CPU to a new process if nothing is being run.
    if not current_proc:
        if rr:
            current_proc = rr.pop()
            if time != 0: temp_dl = dl

        elif sjf:
            current_proc = sjf.pop()
            if time != 0: temp_dl = dl

        elif new or waiting:
            cycles.append("idle")
            total_waiting_time += 1
        else:
            break        
    

    # If there's a process running, append its name to the cycles list
    # and subtract its CPU burst by 1.
    if not temp_dl and current_proc:
        cycles.append(current_proc.pname)
        current_proc.bursts[0] -= 1
        temp_q -= 1

        # If a process has finished its current CPU burst, check to see
        # if it was the first CPU burst and calculate its response time if it is.
        # Then check to see if there are any other bursts left.
        # If there are, add the process to the waiting list, else add it to 
        # the complete list to show that its finished.
        if current_proc.bursts[0] == 0:
            if current_proc.response_time is None:
                current_proc.response_time = (time - current_proc.arrival_time) + 1

            current_proc.bursts.pop(0)
            if current_proc.bursts:
                current_proc.entered_waiting_flag = True
                waiting.append(current_proc)
            else:
                current_proc.turnaround_time += 1
                complete.append(current_proc)
            current_proc = None
            temp_q = q

        # If a process has finished its time slice, set its finished q flag
        # to True to avoid giving it CPU on the next clock cycle.
        if current_proc and (current_proc.queue_num == 1 and temp_q == 0):
            current_proc.finished_q_flag = True
            temp_q = q


    # We're in the middle of a dispatch latency.
    if temp_dl != 0:
        cycles.append("dl")
        total_waiting_time += 1
        temp_dl -= 1


    # Subtract the IO bursts of each process by one if its in the waiting list.
    if waiting:
        for p in waiting:
            if p.entered_waiting_flag:
                p.entered_waiting_flag = False
            else:
                p.bursts[0] -= 1


    # Calculate the turnaround time for each process.
    for p in rr + sjf + waiting:
        p.turnaround_time += 1

    if current_proc:
        current_proc.turnaround_time += 1

    # Calculate the waiting time for each process.
    for p in rr + sjf:
        p.waiting_time += 1  
            

    time += 1

# Calculate different scheduling criteria. 
avg_turnaround_time = [p.turnaround_time for p in complete]
avg_turnaround_time = sum(avg_turnaround_time) / process_count

avg_waiting_time = [p.waiting_time for p in complete]
avg_waiting_time = sum(avg_waiting_time) / process_count

avg_response_time = [p.response_time for p in complete]
avg_response_time = sum(avg_response_time) / process_count


output = generate_output(cycles, process_count, time, total_waiting_time,
                      avg_turnaround_time, avg_waiting_time, avg_response_time)

print(output)

if len(sys.argv) == 3:
    with open(sys.argv[2], "w") as f:
        print(generate_output(cycles, process_count, time, total_waiting_time,
                            avg_turnaround_time, avg_waiting_time, avg_response_time), file=f)



                      