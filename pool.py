import sys
import warnings
from multiprocessing.dummy import Pool as ThreadPool

class CommonPool(object):
    def map(self, func, args):
        return list(map(func, args))

class AutoPool(object):
    def __init__(self, mode, processes):
        if mode == 'multithreading':
            self.pool = ThreadPool(processes=processes)
        else:  # common
            self.pool = CommonPool()

    def map(self, func, args):
        return self.pool.map(func, args)
