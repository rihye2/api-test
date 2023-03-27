import multiprocessing
from multiprocessing import Pool
import time

def func(num):
    c_proc = multiprocessing.current_process()
    print("running on process", c_proc.name, "PID", c_proc.pid)
    time.sleep(1)
    print("ended", num, "process", c_proc.name)
    return num

def mul(x,y):
    c_proc = multiprocessing.current_process()
    print("Running on Process",c_proc.name,"PID",c_proc.pid)
    time.sleep(1)
    print("Ended",x,"*",y,"Process",c_proc.name)
    return x*y


if __name__ == '__main__':
    p = Pool(4)
    start = time.time()
    
    # ret1 = p.apply_async(func, [1,])
    # ret2 = p.apply_async(func, [2,])
    # ret3 = p.apply_async(func, [3,])
    # ret4 = p.apply_async(func, [4,])
    
    # print(ret1.get(), ret2.get(), ret3.get(), ret4.get())
    
    ret = p.starmap_async(mul, [[1, 2], [3, 4], [5, 6]])
    print(ret)
    
    
    delta_t = time.time() - start
    print("time:", delta_t)
    p.close()
    p.join()
    