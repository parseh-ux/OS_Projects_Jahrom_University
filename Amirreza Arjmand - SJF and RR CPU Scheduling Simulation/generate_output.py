def counter(l):
    """
    Receives a list of what's happening at each clock cycle 
    and returns an array of ordered pairs consisting of 
    what's happening and how much time it has taken.
    """
    if len(l) == 0:
        return []

    # Compare each element of the list with the following element. if they were the 
    # same increment count by 1 to designate the count of current element.
    # otherwise append the element with its count to the `results` list 
    # and reset count to 1 for the next element.  
    count = 1
    current_element = l[0]
    results = []
    for p in l[1:]:
        if p == current_element:
            count += 1
        else:
            results.append((current_element, count))
            current_element = p
            count = 1

    results.append((current_element, count))
    return results



def generate_output(cycles, process_count, time, total_waiting_time,
                    avg_turnaround_time, avg_waiting_time, avg_response_time):

    """
    Generates a gantt chart and all of the scheduling criteria for our 
    scheduling algorithm.
    """
    output = ""
    cycles_count = counter(cycles)

    dashes = 0
    gantt = ""
    timings = ""
    current_time = 0


    # Create gantt chart and timings with proper spacing and formatting.
    for p in cycles_count:
        dashes += 9
        gantt += f"{p[0].center(8)}|"
        current_time += p[1]
        timings += f"{current_time:9}"

    # Number of dashes that is needed for top and bottom of the gantt chart.
    output += "-" * dashes + "\n"
    output += gantt[:-1] + "\n"
    output += "-" * dashes + "\n"
    output += timings + "\n"

    output += "\n"

    # Different scheduling criteria.
    output += f"Utilization: {(time - total_waiting_time) / time * 100:.2f}%" + "\n"
    output += f"Throughput: {process_count / time:.2f}(process count per clock cycle)" + "\n"
    output += f"Average turnaround time: {avg_turnaround_time:.2f}" + "\n"
    output += f"Average waiting time: {avg_waiting_time:.2f}" + "\n"
    output += f"Average response time: {avg_response_time:.2f}" + "\n"

    return output