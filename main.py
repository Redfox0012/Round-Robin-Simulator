from queue import Queue
from operator import itemgetter
from queue import LifoQueue


def calc_waiting_time(arr_process: list, has_arrival_time: bool):
    """
        Calcula tempo de espera de cada processo e tempo medio de espera

        :param arr_process: list
        :param has_arrival_time: bool

        :return arr_process: list and avarage float
    """
    sum = 0
    quantity_process = len(arr_process)
    if has_arrival_time:
        for i, process in enumerate(arr_process):
            process['waitingTime'] = process['lastTimeIn'] - (process['count']-1) - process['arrivalTime']
            sum+= process['waitingTime']
    else:
        for i, process in enumerate(arr_process):
            process['waitingTime'] = process['lastTimeIn'] - (process['count']-1) - 0
            sum += process['waitingTime']
    return arr_process, (sum/quantity_process)

def count_process_executed(process_id: int, arr_process: list):
    """
        Conta quantas vezes o processo foi executado

        :param process_id: int
        :param arr_process: list

        :return arr_process: list
    """
    for i, process in enumerate(arr_process):
        if process['id'] == process_id:
            process['count'] += 1
    return arr_process

def last_time_in(process_id: int, arr_process: list, time: int):
    """
        Salva no proprio arr_process o tempo da ultima vez que entrou para execução

        :param process_id: int
        :param arr_process: list
        :param time: int

        :return arr_process: list
    """
    for i, process in enumerate(arr_process):
        if process['id'] == process_id:
            process['lastTimeIn'] = time

    return arr_process

def add_process_to_ready_queue_by_time(ready_queue: Queue, process_stack: LifoQueue, time: int):
    """
        Adiciona o processo na fila e remove da pilha se o tempo for igual a arrival time

        :param ready_queue: Queue
        :param process_stack: LifoQueue
        :param time: int

        :return void
    """
    flag = True
    while flag:
        if not process_stack.empty():
            process = process_stack.get()
        else:
            break

        if process['arrivalTime'] == time:
            ready_queue.put(process)
        else:
            process_stack.put(process)
            flag = False


def short_list_by_arrival_time(list_process):
    """
        Returns a list of dict sorted by arrivalTime

        :param list_process: list

        :return a Queue
    """
    sorted_list = sorted(list_process, key=itemgetter('arrivalTime'))
    return sorted_list


def initialize(list_process: list, has_arrival_time: bool = False):
    """
        Returns the ready queue, or return process stack

        :param list_process: list

        :param has_arrival_time: bool

        :return if has_arrival_time == true LifoQueue else Queue
    """
    ready_queue = Queue()
    for process in list_process:
        ready_queue.put(process)

    if not has_arrival_time:
        return ready_queue

    process_stack = LifoQueue()
    list_process = short_list_by_arrival_time(list_process)
    list_process.reverse()
    for process in list_process:
        process_stack.put(process)

    return process_stack

def copy_arr(arr):
    newArr = []
    for i in arr:
        newArr.append(i.copy())
    return newArr

if __name__ == '__main__':
    quantum = 1
    has_arrival_time = False

    arr_process = [
        {'id': 1, 'arrivalTime': 5, 'burstTime': 10, 'color': 41, 'lastTimeIn': 0, 'count': 0, 'waitingTime': 0},
        {'id': 2, 'arrivalTime': 3, 'burstTime': 1, 'color': 42, 'lastTimeIn': 0, 'count': 0, 'waitingTime': 0},
        {'id': 3, 'arrivalTime': 1, 'burstTime': 2, 'color': 43, 'lastTimeIn': 0, 'count': 0, 'waitingTime': 0},
        {'id': 4, 'arrivalTime': 8, 'burstTime': 1, 'color': 44, 'lastTimeIn': 0, 'count': 0, 'waitingTime': 0},
        {'id': 5, 'arrivalTime': 5, 'burstTime': 5, 'color': 45, 'lastTimeIn': 0, 'count': 0, 'waitingTime': 0},
    ]
    aux_last_time_in = 0
    time = 0
    num_process_ready = 0
    process_queue_or_stack = initialize(arr_process, has_arrival_time)
    ready_queue = Queue()
    process_stack = LifoQueue()
    # Se não considerar arrival time ready_queue é o proprio retorno da função initialize
    if not has_arrival_time:
        ready_queue = process_queue_or_stack
    # Se considerar arrival time pega apenas o primeiro elemento da pilha
    else:
        process_stack = process_queue_or_stack
        first_process = process_stack.get()
        time = first_process['arrivalTime']
        ready_queue.put(first_process)
        add_process_to_ready_queue_by_time(ready_queue, process_stack, time)
    while (not ready_queue.empty()) or (not process_stack.empty()):
        if not ready_queue.empty():
            process = ready_queue.get()

            for q in range(quantum):
                print(f"\033[1;30;{process['color']}mP{str(process['id'])}", end="")
                process['burstTime'] -= 1
                #count_process_executed(process['id'], arr_process)
                if process['id'] != aux_last_time_in:
                    arr_process = last_time_in(process['id'], arr_process, time)
                    arr_process = count_process_executed(process['id'], arr_process)
                    aux_last_time_in = process['id']
                time += 1
                if has_arrival_time:
                    add_process_to_ready_queue_by_time(ready_queue, process_stack, time)
                if process['burstTime'] == 0:
                    break

            if process['burstTime'] > 0:
                ready_queue.put(process)
        else:
            time += 1
            print(f"\033[0;0m-", end="")
            add_process_to_ready_queue_by_time(ready_queue, process_stack, time)

print("\033[0;0m")
arr_process, avarage = calc_waiting_time(arr_process, has_arrival_time)
print()
for process in arr_process:
    print(f"Processo: \033[1;30;{process['color']}mP{str(process['id'])}\033[0;0m")
    print(f"id: {process['id']}")
    print(f"Tempo de espera: {process['waitingTime']}")
    print('---' * 50)

print(f'Tempo médio de espera: {avarage}')

