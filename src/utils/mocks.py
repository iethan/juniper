from time import sleep

__all__ = ["MockIter"]

class MockIter:
    def __init__(self,stop_iter_num=None,sleep=10):
        self._stop_iter_num = stop_iter_num
        self._iter_cnt = 0
        self._sleep = sleep

    def __iter__(self):  

        return self 

    def __next__(self):
        '''Will iter infinitely if not given stop_iter_num'''

        if not self._stop_iter_num:
            sleep(self._sleep)
            return self

        elif self._stop_iter_num and (self._iter_cnt < self._stop_iter_num):

            sleep(self._sleep)
            self._iter_cnt += 1

            return self     
        else:
            raise StopIteration()