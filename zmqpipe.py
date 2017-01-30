import sys
import time

from  multiprocessing import Process, Pipe

import zmq
 
ITERS = 10000000
MSG = "MESSAGE"

def pipe_worker(q):
    while not q.closed:
        message = q.recv()
    sys.exit(1)
  
def pipe_main():
    send_q, recv_q = Pipe(duplex=False)
    Process(target=pipe_worker, args=(send_q,)).start()
    for num in range(ITERS):
        recv_q.send(MSG)
    recv_q.close()

def pipe_test():
    start_time = time.time()
    pipe_main()
    end_time = time.time()
    duration = end_time - start_time
    msg_per_sec = ITERS / duration
 
    print "Duration: %s" % duration
    print "Messages Per Second: %s" % msg_per_sec

 
def zmq_worker():
    context = zmq.Context()
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://127.0.0.1:5557")
 
    for task_nbr in range(ITERS):
        message = work_receiver.recv()
 
    sys.exit(1)
 
def zmq_main():
    Process(target=zmq_worker, args=()).start()
    context = zmq.Context()
    ventilator_send = context.socket(zmq.PUSH)
    ventilator_send.bind("tcp://127.0.0.1:5557")
    for num in range(ITERS):
        ventilator_send.send(MSG)
 
def zmq_test():
    start_time = time.time()
    t = Process(target=zmq_main)
    t.start()
    t.join()
    end_time = time.time()
    duration = end_time - start_time
    msg_per_sec = ITERS / duration
 
    print "Duration: %s" % duration
    print "Messages Per Second: %s" % msg_per_sec
 
if __name__ == "__main__":
    zmq_test()
    pipe_test()
