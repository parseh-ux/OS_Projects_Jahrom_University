# CPU Scheduling Simulation using Round Robin and SJF Queues

## General explanation

This project is written as an assignment for the operating systems course. It simulates how processes are scheduled in an operating system that utilizes a multilevel queue consisting of a Round Robin queue and an SJF queue.

The input is given as a command line argument e.g. `python main.py input4.txt`. Serval samples are included in the `inputs` directory. It contains information about each process along with other data inside it in the following format:

```
3
1
P1: 1, 0, 4, 3, 2
P2: 2, 0, 4
```

First line signifies the time quantum dedicated to each process in case that process is in the RR queue. Second line denotes the dispatch latency i.e. how much time is required by the operating system to switch the context of the CPU and load in another process. After these two lines information about each individual process is provided in each line. From left to right: The first one is the label of the process; This can be any combination of letters and digits but must be a unique value. It can be compared to the process id in many major operating systems. The process label comes with a trailing column. After the column, the first number indicates which queue is the process gonna go in, 1 is associated to the RR queue and 2 to the SJF. This is a multilevel queue not a MLFQ, meaning that processes are gonna stay in the queue they were put in from the beginning. The number after that is the arrival time, and all of the numbers after the arrival time are the CPU/IO bursts. All of the numbers except for the process label are separated with commas, and must be integers.

The output is printed to the stdout by default. Additionally, a file name could be given to the program as the second command line argument, in which the output is gonna be written as well. The output consists of a Gantt chart, showing how each process is handled by the operating system. Sevral lines of information such as the CPU utilization, average response time, average turnaround time, etc. are given below the Gantt chart to evaluate the overall performance of the system. The following is an instance of the program's output for the above input:

```
---------------------------------------------------------------
   P1   |   dl   |   P1   |   dl   |   P2   |   dl   |   P1    
---------------------------------------------------------------
        3        4        5        6       10       11       13

Utilization: 76.92%
Throughput: 0.15(process count per clock cycle)
Average turnaround time: 11.50
Average waiting time: 3.50
Average response time: 7.50
```

## Implementation Details

There are several source files written in Python for this project. Each process is stored in the format of an object of type `Process` in `Process.py` file. Then there are `load_data.py` and `generate_output.py` files which as their names suggest handle reading in the data and formatting the output respectively. There is also a `utils.py` file which contains the general functions that are used throughout the program, such as sorting the SJF queue and inserting a process into its respective queue. The central part of the program lies within `main.py`. This is the program that must be called to simulate the CPU scheduling. It essentially works by simulating what is happening in each clock cycle in a loop, each iteration of this loop decides what to do with current running process and what process should we load in next, and it halts where no process is left in both queues.
