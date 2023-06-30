from Process import Process

def load_data(fname):
    with open(fname) as f:
        # Read the first two lines of the input file as time quantum and dispatch latency.
        q = int(f.readline())
        dl = int(f.readline())

        processes = []

        # After the first two lines, read each of the following lines and store them in the
        # `processes` list as a `Process` object.
        for line in f:
            processes.append(Process.from_string(line))

        return (q, dl, processes)
