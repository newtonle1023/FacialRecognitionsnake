from game import EyeSnake
from cv2_daemon import CameraDaemon
import multiprocessing

if __name__ == '__main__':
	vals = multiprocessing.Manager().list()
	vals.append(True)
	
	p = multiprocessing.Process(target=EyeSnake, args=[vals])
	p2 = multiprocessing.Process(target=CameraDaemon, args=[vals])
	p.start()
	p2.start()
	p.join()
	p2.join()