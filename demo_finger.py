from game_m import EyeSnake
from finger_control import FingerControls
from cv2_daemon import CameraDaemon
import multiprocessing

if __name__ == '__main__':
	vals = multiprocessing.Manager().list()
	vals.append(0)
	
	p = multiprocessing.Process(target=EyeSnake, args=[vals])
	p2 = multiprocessing.Process(target=FingerControls, args=[vals])
	p.start()
	p2.start()
	p.join()