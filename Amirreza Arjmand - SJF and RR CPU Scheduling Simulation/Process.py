class Process:
    """Acts as a simplified PCB. Stores the data of each process."""
    def __init__(self, pname, queue_num, arrival_time, bursts):
        self.pname = pname
        self.queue_num = queue_num
        self.arrival_time = arrival_time
        self.bursts = bursts
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = None

        self.finished_q_flag = False

    def __repr__(self):
        return self.pname

    @classmethod
    def from_string(cls, line):
        """
        Creates a process object based on a string with the specific format:
        `pname: queue type, arrival time, [bursts]`
        Ignores any trailing or leading whitespaces.
        """
        pname, bursts = line.split(":")
        pname = pname.strip()
        bursts = [int(x) for x in bursts.split(",")]
        queue_num = bursts.pop(0)
        arrival_time = bursts.pop(0)

        return cls(pname, queue_num, arrival_time, bursts)
