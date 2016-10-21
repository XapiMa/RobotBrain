from multiprocessing import Process
import os

def f(num):
    print "Number:",num
    print 'parent process:',os.getppid()
    print 'process id', os.getpid()

if __name__ == '__main__':
    for num in range(10):
        p = Process(target =f,args=(num,))
        p.start()
        p.join()
