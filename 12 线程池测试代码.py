
import threading
import time
from queue import Queue


class CustomThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.__queue = queue

    def run(self):
        while True:
            q_method = self.__queue.get()   #阻塞取出队列
            q_method()                      #执行取出的队列元素
            #print(q_method())
            self.__queue.task_done()        #发送任务执行完毕信号

def moyu():
    print(" 开始摸鱼 %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

def queue_pool():           #创建线程池
    queue = Queue(5)        #创建容量为5的队列
    print(queue)
    for i in range(queue.maxsize):
        t = CustomThread(queue)
        t.setDaemon(True)   #设置守护线程
        t.start()           #开始执行线程

    for i in range(20):
        queue.put(moyu)     #阻塞放入队列
    queue.join()            #等待线程结束

if __name__ == '__main__':
    queue_pool()