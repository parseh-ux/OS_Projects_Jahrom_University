def sjf_sort(sjf):
    n = len(sjf)

    for i in range(n - 1):    
        for j in range(i + 1, n):
            swap = sjf[i].bursts[0] < sjf[j].bursts[0] or \
            (sjf[i].bursts[0] == sjf[j].bursts[0] and sjf[i].arrival_time < sjf[j].arrival_time) or \
            (
                sjf[i].bursts[0] == sjf[j].bursts[0] and sjf[i].arrival_time == sjf[j].arrival_time and
                sjf[i].pname < sjf[j].pname
            )

            if swap:
                sjf[i], sjf[j] =  sjf[j], sjf[i]
            


def proc_insert(proc, rr, sjf):
    """Insert each of the processes into their respective queue."""
    if proc.queue_num == 1:
        rr.insert(0, proc)
    else:
        sjf.append(proc)
        sjf_sort(sjf)
