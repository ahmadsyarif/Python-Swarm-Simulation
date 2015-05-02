#this program is to simulate swarm
#written by : ahmad syarif
#last edited : May 2, 2015

from graphics import * #using library from mcsp.wartburg.edu/zelle/python/graphics.py
import time
import threading
import math
from random import randint

lock = threading.Lock()
def draw_windows(w,h):
	#create windows
	print 'create windows with name : swarm, width : ',w,', height : ',h
	return GraphWin('swarm',w,h)
	pass

def draw_swarm(n,win):
	#draw n number of robot in window win
	robot =[]
	for x in xrange(0,n):
		robot.append(Circle(Point(randint(20,win.getWidth()-20),randint(20,win.getHeight()-20)),20))
		print 'create robot with number ',x,' point x : ',x*200+40,', y : 200 , r : 20'
		robot[x].setFill('red')
		robot[x].draw(win)
		pass
	return robot
	pass

def dynamics(robot,robots):
	#dynamics of the swarm
	x_total,y_total = relative_distance(robot,robots)
	lock.acquire()
	print 'distance of robot ', robot.id, ' ',x_total,' ',y_total
	print robot.id
	lock.release()
	distance = distance_magnitude(x_total,y_total)
	while distance>0.5:
		loc_x = -x_total/40.0
		loc_y = -y_total/40.0
		lock.acquire()
		print robot.id,loc_x,loc_y,distance		
		lock.release()
		robot.move(loc_x,loc_y)
		x_total,y_total = relative_distance(robot,robots)
		distance = distance_magnitude(x_total,y_total)
		time.sleep(0.1)
		pass
	pass

def simulate(robots):
	#run simulation using multithreading
	for robot in robots:
		worker = threading.Thread(target=dynamics,args=(robot,robots))
		worker.setDaemon(True)
		worker.start() 	
		pass
	pass

def distance_vector(P1,P2):
	#calculate distance in vector between two Point
	x = P1.getX()-P2.getX()
	y = P1.getY()-P2.getY()
	return x,y
	pass

def distance_magnitude(x,y):
	#calculate magnitude of distance vector
	return math.sqrt(x*x+y*y)
	pass

def relative_distance(robot,robots):
	#calculate relative distance of a robot to all other robots
	x_total=0
	y_total=0
	for r in robots:
		x,y = distance_vector(robot.getCenter(),r.getCenter())
		x_total+=x
		y_total+=y
		pass
	return x_total,y_total
	pass

def main():
	#main program
	win = draw_windows(700,600) #draw window with width = 700 and height = 600
	robots = draw_swarm(7,win) #draw 7 swarm in win
	win.getMouse() #blocking call
	simulate(robots) #start simulation
	win.getMouse()
	pass

if __name__ == '__main__':
	main()
