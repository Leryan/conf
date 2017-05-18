import sys
import time

from  multiprocessing import Process, Pipe

import zmq
 
ITERS = 1000
MSG = "MESSAGE"

def pipe_worker(q):
    while not q.closed:
        message = q.recv()
  
def pipe_main(recv_q):
    for num in range(ITERS):
        recv_q.send(MSG)

def zmq_worker():
    context = zmq.Context()
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://127.0.0.1:5557")
 
    for task_nbr in range(ITERS):
        message = work_receiver.recv()
 
def zmq_main():
    context = zmq.Context()
    ventilator_send = context.socket(zmq.PUSH)
    ventilator_send.bind("tcp://127.0.0.1:5557")

    for num in range(ITERS):
        ventilator_send.send_string(MSG)

def test_zmq(benchmark):
    p = Process(target=zmq_worker, args=())
    p.start()

    result = benchmark(zmq_main)

    p.terminate()

def test_pipe(benchmark):
    sys.stderr.write('coucou\n')
    send_q, recv_q = Pipe(duplex=False)
    p = Process(target=pipe_worker, args=(send_q,))
    p.start()

    result = benchmark.pedantic(pipe_main, args=(recv_q,))
    recv_q.close()

    p.terminate()
