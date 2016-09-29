import multiprocessing as mp
import platform

def sysinfo():
    print 'Python version  : ', platform.python_version()
    print 'Compiler        : ', platform.python_compiler() 
    print 'System          : ', platform.system()
    print 'Release         : ', platform.release()
    print 'Machine         : ', platform.machine()
    print 'Processor       : ', platform.processor()
    print 'CPU count       : ', mp.cpu_count()
    print 'Interpreter     : ', platform.architecture()[0], '\n'

if __name__ == '__main__':
    sysinfo()
