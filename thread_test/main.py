from multiprocessing import shared_memory
from time import sleep

def main():
    sl = shared_memory.ShareableList(sequence=[None], name="test_list")
    a=0
    while a<99999:
        sl[0] = a
        sleep(0.001)
        a+=1
    sl.close()
    sl.unlink()

main()
