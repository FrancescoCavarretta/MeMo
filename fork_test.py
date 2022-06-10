import os
import time

def function():
    for i in range(2):
        #print '**********%d***********' % i
        pid = os.fork()
        if pid == 0:
            # We are in the child process.
            return "%d (child) just was created by %d." % (os.getpid(), os.getppid())
        else:
            pass
            # We are in the parent process.
            #print "%d (parent) just created %d." % (os.getpid(), pid)


print (function())
