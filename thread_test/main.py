from multiprocessing import shared_memory
from time import sleep

def main():
    sharedMainList = shared_memory.ShareableList(sequence=range(256), name="MainList")



    sl.close()
    sl.unlink()

main()
