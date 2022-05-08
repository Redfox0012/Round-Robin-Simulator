from queue import Queue


def add_process_to_ready_queue(list_process: list, has_arrival_time: bool = False):
    """
        Returns the ready queue regardless of arrival time

        :param list_process: list

        :param has_arrival_time: bool

        :return a Queue
    """
    ready_queue = Queue()
    for process in list_process:
        ready_queue.put(process)

    return ready_queue


if __name__ == '__main__':
    quantum = 1
    arr_process = [
        {'id': 1, 'arrivalTime': 0, 'burstTime': 10, 'color': 41},
        {'id': 2, 'arrivalTime': 0, 'burstTime': 1, 'color': 42},
        {'id': 3, 'arrivalTime': 0, 'burstTime': 2, 'color': 43},
        {'id': 4, 'arrivalTime': 0, 'burstTime': 1, 'color': 44},
        {'id': 5, 'arrivalTime': 0, 'burstTime': 5, 'color': 45},
    ]

    time = 0
    num_process_ready = 0

    ready_queue = add_process_to_ready_queue(arr_process)

    while not ready_queue.empty():
        process = ready_queue.get()
        for q in range(quantum):
            print(f"\033[1;30;{process['color']}mP{str(process['id'])}", end="")
            process['burstTime'] -= 1
            if process['burstTime'] == 0:
                break
        if process['burstTime'] > 0:
            ready_queue.put(process)

        time += 1

