class Process:

    def __init__(self, PID : int, QueueNum : int, ArrivalTime : int, Bursts):
        #Asserts

        self.PID = PID
        self.PID_Num = int(PID[1::])
        self.QueueNum = QueueNum
        self.ArrivalTime = ArrivalTime
        self.Bursts = Bursts
        self.Turnaround_Time = 0
        self.Waiting_Time = 0
        self.First_time_IO = True
        self.First_time_IO_Time = 0
        self.Response_Time = 0
        self.exit_Time = 0
        self.entered_wait = False



