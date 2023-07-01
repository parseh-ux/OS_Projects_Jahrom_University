# OS_RR_SJF
Implementation of Round Robin and Shortest Job First (SJF) CPU scheduling algorithms in python.
Format of input file should be like this:

10
2
P1:1,5,15,10

10 (Time quantum for round robin)
2 (Dispatcher latency)
(
  P1: Process ID,
  1:  Queue number, 1 for RR and 2 for SJF,
  5:  CPU burst time,
  15: IO CPU burst time,
  10: CPU burst time
)
