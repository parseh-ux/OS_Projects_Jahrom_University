import sys
from Process import Process

# Read input.txt file
with open(r"input4.txt", "r") as f:
    # Get q from input
    q = int(f.readline().strip())
    # Get dl from input
    dl = int(f.readline().strip())
    # list of processes in input file
    processes = []
    # Putting each process from the input file into the processes list
    for line in f:
        PID, Values = line.split(":")
        PID = PID.strip()
        Bursts = [int(x.strip()) for x in Values.split(",")]
        # Get QueueNum from first of the Bursts
        QueueNum = Bursts.pop(0)
        # Get ArrivalTime from first of the Bursts
        ArrivalTime = Bursts.pop(0)

        processes.append(Process(PID, QueueNum, ArrivalTime, Bursts))

# Round Robin Queue as a list
RR = []
# SJF Queue as a list
SJF = []
# IO wait Queue
wait = []
# CPU_PCB for running processes
CPU_PCB = None
# Stop
HLT = False
# Clock
CLK = 0
# idle time
idle = 0
# idle + Dispatcher Latency time
over_all_idle = 0
# temporarily q to work with and keep the original q
temp_q = 0
# temporarily dl to work with and keep the original dl
temp_dl = 0
# list of what's happening in each clock to use in gantt chart
chart = []
# Making sure that only one thing is being added to chart
gc = True

# Sorting processes based on their ArrivalTime
processes.sort(key=lambda x: x.ArrivalTime, reverse=False)

# Shift processes ArrivalTime to zero
Shift_Amount = processes[0].ArrivalTime
for process in processes:
    process.ArrivalTime = process.ArrivalTime - Shift_Amount

tmp_PCB1 = None
# Main
while not HLT:
    # Reading each process from processes list
    for TheProcess in processes[:]:
        # If the process ArrivalTime is equal to Clock
        # it will be added to the respectable Queue
        # and popped from the processes Queue
        if TheProcess.ArrivalTime == CLK:
            if TheProcess.QueueNum == 1:
                RR.append(TheProcess)
                processes.pop(processes.index(TheProcess))
            elif TheProcess.QueueNum == 2:
                SJF.append(TheProcess)
                processes.pop(processes.index(TheProcess))

    # Decreasing the process IO time by 1 for each clock
    # if it's not its first clock in IO waiting Queue
    # coming from PCB to prevent both CPU Burst
    # and IO Bursts reduction in 1 clock (if wait isn't empty)
    for p in wait:
        if p.entered_wait:
            p.entered_wait = False
        else:
            p.Bursts[0] = p.Bursts[0] - 1

    # If wait isn't empty
    if wait:
        # If any process has finished its IO Burst
        # we will remove the Burst from Bursts list
        # and  add the process to its respectable Queue
        # and popping it from wait queue
        for p in wait:
            if p.Bursts:
                if p.Bursts[0] == 0:
                    p.Bursts.pop(0)
                    if p.QueueNum == 1:
                        RR.append(p)
                    elif p.QueueNum == 2:
                        SJF.append(p)
                    wait.pop(wait.index(p))
    if tmp_PCB1:
        RR.append(tmp_PCB1)
        tmp_PCB1 = None

    # If PCB is empty we will go to the queues
    if not CPU_PCB:
        # If RR isn't empty we will put its first element into PCB
        # and remove the process from RR queue
        if RR:
            CPU_PCB = RR[0]
            RR.pop(0)
            # Putting temp_q = q for the new process in PCB
            temp_q = q
        # If RR is empty we will put SJFs first element into PCB
        # and remove the process from SJF queue
        elif SJF:
            SJF.sort(key=lambda x: x.Bursts[0], reverse=False)
            CPU_PCB = SJF[0]
            SJF.pop(0)

    # if PCB isn't empty we will add 1 to its Turnaround_Time
    # for being in the system in that 1 clock
    if CPU_PCB:
        CPU_PCB.Turnaround_Time += 1
    # if RR or SJF or wait queues aren't empty we will add 1 to their processes
    # Turnaround_Times for being in the system in that 1 clock
    for p in RR + SJF + wait:
        p.Turnaround_Time += 1
    # if RR or SJF queues aren't empty we will add 1 to their processes Waiting_Time
    # for being in the system in that 1 clock
    for p in RR + SJF:
        p.Waiting_Time += 1

    # if PCB isn't empty
    if CPU_PCB:
        # We will check if Dispatcher is inactive
        if temp_dl == 0:
            # If Dispatcher is inactive we will put the process name
            # in the chart for being worked on in cpu in that clock
            if gc:
                chart.append(CPU_PCB.PID)
                # Only one process allowed to be added to chart in 1 clock
                gc = False
            # Checking the process queue number to work with it as intended
            if CPU_PCB.QueueNum == 1:
                # Making sure the process CPU Burst isn't 0
                if CPU_PCB.Bursts[0] != 0:
                    # Reducing 1 from process CPU Burst for this clock in CPU/PCB
                    CPU_PCB.Bursts[0] = CPU_PCB.Bursts[0] - 1
                    # Reducing 1 from process temp_q for this clock in CPU/PCB
                    temp_q -= 1
                    # If the process has run out of temp_q, but it still has CPU Burst left
                    if temp_q == 0 and CPU_PCB.Bursts[0] != 0:
                        # the process will be go back RR queue
                        tmp_PCB1 = CPU_PCB
                        # and PCB will become empty
                        CPU_PCB = None
                        # and a new temp_dl will be set
                        temp_dl = dl
                    # If the process has done its CPU Burst
                    elif CPU_PCB.Bursts[0] == 0:
                        # The empty element in Bursts will be popped
                        CPU_PCB.Bursts.pop(0)
                        # and we will check if it has other bursts
                        if CPU_PCB.Bursts:
                            # if yes then the next bursts is IO burst, so
                            # we will check if its first IO for this process
                            if CPU_PCB.First_time_IO:
                                # if yes we will put its First_time_IO_Time = clock + 1
                                # to be used for computing its Response_Time
                                CPU_PCB.First_time_IO_Time = CLK + 1
                                CPU_PCB.First_time_IO = False
                            # then we will put entered_wait = true to know it's
                            # going to IO wait queue
                            CPU_PCB.entered_wait = True
                            # and append it ot IO wait queue
                            wait.append(CPU_PCB)
                        else:
                            # but if process doesn't have any other Bursts
                            # it means it's done, and it should go back to processes Queue
                            # we also check if the process has done any Io before or not
                            # and if not it will get its First_time_IO_Time set
                            if CPU_PCB.First_time_IO:
                                # we will put its First_time_IO_Time = clock + 1
                                # to be used for computing its Response_Time
                                CPU_PCB.First_time_IO_Time = CLK + 1
                                CPU_PCB.First_time_IO = False
                            # The process exit time will be set
                            CPU_PCB.exit_Time = CLK + 1
                            # The process will be appended to processes queue
                            processes.append(CPU_PCB)
                        # PCB will become empty
                        CPU_PCB = None
                        # and a new temp_dl will be set
                        temp_dl = dl
            # If the process belongs to SJF queue it will be added to it
            elif CPU_PCB.QueueNum == 2:
                # Making sure the process CPU Burst isn't 0
                if CPU_PCB.Bursts[0] != 0:
                    # Reducing 1 from process CPU Burst for this clock in CPU/PCB
                    CPU_PCB.Bursts[0] = CPU_PCB.Bursts[0] - 1
                    # If the process has done its CPU Burst
                    if CPU_PCB.Bursts[0] == 0:
                        # The empty element in Bursts will be popped
                        CPU_PCB.Bursts.pop(0)
                        # and we will check if it has other bursts
                        if CPU_PCB.Bursts:
                            # if yes then the next bursts is IO burst, so
                            # we will check if its first IO for this process
                            if CPU_PCB.First_time_IO:
                                # if yes we will put its First_time_IO_Time = clock + 1
                                # to be used for computing its Response_Time
                                CPU_PCB.First_time_IO_Time = CLK + 1
                                CPU_PCB.First_time_IO = False
                            # then we will put entered_wait = true to know it's
                            # going to IO wait queue
                            CPU_PCB.entered_wait = True
                            # and append it ot IO wait queue
                            wait.append(CPU_PCB)
                        else:
                            # but if process doesn't have any other Bursts
                            # it means it's done, and it should go back to processes Queue
                            # we also check if the process has done any Io before or not
                            # and if not it will get its First_time_IO_Time set
                            if CPU_PCB.First_time_IO:
                                # if yes we will put its First_time_IO_Time = clock + 1
                                # to be used for computing its Response_Time
                                CPU_PCB.First_time_IO_Time = CLK + 1
                                CPU_PCB.First_time_IO = False
                            # The process exit time will be set
                            CPU_PCB.exit_Time = CLK + 1
                            # The process will be appended to processes queue
                            processes.append(CPU_PCB)
                        # PCB will become empty
                        CPU_PCB = None
                        # and a new temp_dl will be set
                        temp_dl = dl

        # but if Dispatcher is active
        else:
            # The dl will be added to chart
            if gc:
                chart.append("dl")
                gc = False
            # temp_dl will decrease by 1 for the clock that has been passed
            temp_dl -= 1
            # over_all_idle will decrease by 1 for the clock that has been passed
            over_all_idle += 1
    # if PCB is empty it means system is in idle
    else:
        # The idle will be added to chart
        if gc:
            chart.append("de")
            gc = False
        # if while idle temp_dl isn't zero it will decrease by 1 for the clock that has been passed
        if temp_dl != 0:
            temp_dl -= 1
        idle += 1
        # over_all_idle will decrease by 1 for the clock that has been passed
        over_all_idle += 1

    # Adding 1 to Clock to go to the next Clock
    CLK = CLK + 1

    # Putt gc == True for the new Clock
    gc = True

    # Checking if the Queues are all empty and system needs to go to HLT state
    if not RR:
        if not SJF:
            if not wait:
                if not CPU_PCB:
                    # For each process in processes we will check if it has any
                    # Bursts left, if there isn't any process in processes
                    # with Bursts then the system will go to HLT state.
                    for p in processes:
                        if not p.Bursts:
                            HLT = True
                        # If we find any process in processes with Bursts
                        # the system shouldn't go to HLT state
                        else:
                            break


processes.sort(key=lambda x: x.PID_Num)
print(f"CLK = {CLK}")
print(f"idle = {idle}")
print(f"over_all_idle = {over_all_idle}")

for ans_proc in processes:
    ans_proc.Response_Time = ans_proc.First_time_IO_Time - ans_proc.ArrivalTime

for ans_proc in processes:
    print(f"{ans_proc.PID} : ", end='')
    print(f"QueueNum = {ans_proc.QueueNum}, ", end='')
    print(f"ArrivalTime = {ans_proc.ArrivalTime}, ", end='')
    print(f"Turnaround_Time = {ans_proc.Turnaround_Time}, ", end='')
    print(f"Waiting_Time = {ans_proc.Waiting_Time}, ", end='')
    print(f"First_time_IO_Time = {ans_proc.First_time_IO_Time}, ", end='')
    print(f"Response_Time = {ans_proc.Response_Time}, ", end='')
    print(f"exit_Time = {ans_proc.exit_Time}, ", end='')
    print('[', end='')
    for b1 in ans_proc.Bursts:
        print(str(b1) + ', ', end='')
    print(']')


print(f"CPU Utilization = %{round(((CLK - over_all_idle) / CLK) * 100, 2)}")
print(f"Throughput = {round((len(processes)/CLK), 2)}")
Turnaround_Time = 0
Waiting_Time = 0
Response_Time = 0

for ans_proc in processes:
    Turnaround_Time = Turnaround_Time + ans_proc.Turnaround_Time
    Waiting_Time = Waiting_Time + ans_proc.Waiting_Time
    Response_Time = Response_Time + ans_proc.Response_Time

print(f"Average Turnaround Time = {round(Turnaround_Time/len(processes), 2)} s")
print(f"Average Waiting Time    = {round(Waiting_Time/len(processes), 2)} s")
print(f"Average Response Time   = {round(Response_Time/len(processes), 2)} s")

timings = [0]
tmp = chart[0]
timings_count = 0
for s in chart:
    if tmp != s:
        timings.append(timings_count)
    timings_count += 1
    tmp = s

chart_counter = len(timings) * 5 + 1
line = 0
while line < chart_counter:
    print('\u2500', end='')
    line += 1

print("")
tmp = chart[0]
print(f"\u2502 {chart[0]} ", end='')
for s in chart:
    if tmp != s:
        print(f"\u2502 {s} ", end='')
    tmp = s
print("\u2502")

line = 0
while line < chart_counter:
    print('\u2500', end='')
    line += 1

print("")
line = 0
theC = 0
while line < CLK:
    if theC < len(timings):
        if line == timings[theC]:
            sys.stdout.write(f"{line}".ljust(5))
            theC += 1
    line += 1
print(CLK)

output_file = open("output.txt", "w", encoding='utf-8')

output_file.write("\n")

line = 0
while line < chart_counter:
    output_file.write('\u2500')
    line += 1

output_file.write("\n")

tmp = chart[0]
output_file.write(f"\u2502 {chart[0]} ")
for s in chart:
    if tmp != s:
        output_file.write(f"\u2502 {s} ")
    tmp = s
output_file.write("\u2502")

output_file.write("\n")
line = 0
while line < chart_counter:
    output_file.write('\u2500')
    line += 1

output_file.write("\n")
line = 0
theC = 0
while line < CLK:
    if theC < len(timings):
        if line == timings[theC]:
            output_file.write(f"{line}".ljust(5))
            theC += 1
    line += 1

output_file.write(f"{CLK}")

output_file.write("\n\n")
output_file.write(f"CPU Utilization = %{round(((CLK - over_all_idle) / CLK) * 100, 2)}")
output_file.write("\n")
output_file.write(f"Throughput = {round((len(processes)/CLK), 2)}")
output_file.write("\n")
Turnaround_Time = 0
Waiting_Time = 0
Response_Time = 0

for ans_proc in processes:
    Turnaround_Time = Turnaround_Time + ans_proc.Turnaround_Time
    Waiting_Time = Waiting_Time + ans_proc.Waiting_Time
    Response_Time = Response_Time + ans_proc.Response_Time

output_file.write(f"Average Turnaround Time = {round(Turnaround_Time/len(processes), 2)} s")
output_file.write("\n")
output_file.write(f"Average Waiting Time    = {round(Waiting_Time/len(processes), 2)} s")
output_file.write("\n")
output_file.write(f"Average Response Time   = {round(Response_Time/len(processes), 2)} s")
output_file.write("\n")

output_file.close()
