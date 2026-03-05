from time import sleep
from multiprocessing import shared_memory

sl = shared_memory.ShareableList(name="test_list")
while True:
    sleep(2)
    print(sl)

sl.close()