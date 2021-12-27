from utils import get_album_description
import time

if __name__ == '__main__':
    for _ in range(100):
        t_start = time.monotonic()
        get_album_description("Valve", "Half-Life2")
        t_stop = time.monotonic()

        t_run = t_stop - t_start
        
        print("Время текущего запроса = ", t_run, "s")