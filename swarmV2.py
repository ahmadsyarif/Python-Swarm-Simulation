"""program to simulate swarm dynamics"""

from graphics import *
import time
import math
import threading
from random import randint

class robot(object):
	"""class for defining robot"""
	def __init__(self,size=20,robot_id=0,window=None,center = None):
		"""constructor"""
		super(robot,self).__init__()
		if window == None:
			if center==None:
				self.center = Point(randint(0,200),randint(0,200)) #get random center of the robot
			else:
				self.center = center
		else:
			if center == None:
				self.center = Point(randint(0,window.getWidth()),randint(0,window.getHeight())) #get random center of the robot according to window size
			else:
				self.center = center

		self.text = Text(self.center,robot_id) #create text that will be place in the center of the robot
		self.main = Circle(self.center,size) #create main body of the robot
		self.main.setFill('red') #set the fill of robot to be red
		self.outer = Circle(self.center,5*size) #create outer of sensor for the robot
		self.main_radius = size
		self.outer_radius = size*5
		self.id = robot_id

	def draw(self,window):
		"""draw the robot and its property to window"""
		self.main.draw(window) 
		self.outer.draw(window)
		self.text.draw(window)
		self.window = window
	def move(self,x,y):
		"""move the robot and its property to x,y"""
		self.main.move(x,y)
		self.outer.move(x,y)
		self.text.move(x,y)
		self.center = self.main.getCenter()
	def get_center(self):
		"""get the center point of robot"""
		x = self.center.getX()
		y = self.center.getY()
		return x,y
	def get_robot_size(self):
		return self.main_radius
	def change_robot_size(self,size):
		"""change robot size into new radius size"""
		self.main.undraw()
		self.outer.undraw()
		self.main = Circle(self.center,size)
		self.main.setFill('red')
		self.outer = Circle(self.center,5*size)
		self.main_radius = size
		self.outer_radius = 5*size
	def change_outer_size(self,k):
		"""change robot outer to k times of robot size"""
		self.outer.undraw()
		self.outer = Circle(self.center,k*self.main_radius)
		self.outer_radius= k*self.main_radius
		pass	

class swarm(object):
	"""class for defining  swarm"""
	def __init__(self,number,window):
		"""constructor"""
		super(swarm, self).__init__()
		self.number = number #set the number of robots in swarm
		self.robots = [] #set list of the robots
		for n in xrange(0,number):
			self.robots.append(robot(robot_id=n,window = window)) #create instance of robot
			pass

	def set_robot_size(self,size):
		for robot in self.robots:
			robot.change_robot_size(size)
		pass

	def set_outer_size(self,k):
		for robot in self.robots:
			robot.change_outer_size(k)
		pass

	def draw(self,window):
		"""draw all the robots in swarm in to window"""
		for robot in self.robots:
			robot.draw(window)
			pass
		
	def get_robot(self,index):
		"""return robot with index"""
		if index<self.number:
			return self.robots[index]
		else:
			return 0
	def get_robots(self):
		"""return the list of robot"""
		return self.robots
		pass

	def get_number(self):
		return self.number
	def add_robot(self,robot):
		self.robots.append(robot)
		self.number+=1

class meeting_point_dynamics(object):
	"""docstring for meeting_point_dynamics"""
	def __init__(self,  number, use_radius=False):
		"""constructor"""
		super(meeting_point_dynamics, self).__init__()
		self.window = GraphWin('meeting point dynamics',1000,600)
		self.swarm = swarm(number,self.window)
		self.use_radius = use_radius
		self.swarm.set_robot_size(40)
		self.swarm.set_outer_size(2)
		self.robot_size = 40
		self.robot_outer_size = 2
	def run(self):
		self.swarm.draw(self.window)
		worker = threading.Thread(target=self.dynamics,args=())
		worker.setDaemon(True)
		worker2 = threading.Thread(target=self.add_robot,args=())
		worker2.setDaemon(True)
		self.window.getMouse()
		worker.start()
		worker2.start()
		pass
	def dynamics(self):
		while True:
			for robot in self.swarm.get_robots():
				x, y = distance_to_all(robot,self.swarm,self.use_radius)
				v_x = x/40.0
				v_y = y/40.0
				robot.move(v_x,v_y)
			time.sleep(0.1)
	def add_robot(self):
		while True:
			p = self.window.getMouse()
			r = robot(size=self.robot_size,robot_id=self.swarm.get_number(),center=p)
			r.change_outer_size(self.robot_outer_size)
			r.draw(self.window)
			self.swarm.add_robot(r)
			pass

class safe_distance_dynamics(object):
	"""docstring for safe_distance_dynamics"""
	def __init__(self,number):
		super(safe_distance_dynamics, self).__init__()
		self.window = GraphWin('safe distance dynamics',1000,600)
		self.swarm = swarm(number,self.window)
		self.swarm.set_robot_size(20)
		self.swarm.set_outer_size(4)
		self.robot_size = 20
		self.robot_outer_size = 4
	def run(self):
		self.swarm.draw(self.window)
		worker = threading.Thread(target=self.dynamics,args=())
		worker.setDaemon(True)
		worker2 = threading.Thread(target=self.add_robot,args=())
		worker2.setDaemon(True)
		self.window.getMouse()
		worker.start()
		worker2.start()
		pass
	def dynamics(self):
		while True:
			for robot in self.swarm.get_robots():
				fx,fy = force_to_all(robot,self.swarm)
				v_x = 20*fx
				v_y = 20*fy
				robot.move(v_x,v_y)
			time.sleep(0.1)
	def add_robot(self):
		while True:
			try:
				p = self.window.getMouse()
				r = robot(size=self.robot_size,robot_id=self.swarm.get_number(),center=p)
				r.change_outer_size(self.robot_outer_size)
				r.draw(self.window)
				self.swarm.add_robot(r)
			except:
				return
			pass

"""function for vector operation"""
def distance(v1,v2):
	"""return distance between two point in vector"""
	x1,y1 = v1.get_center()
	x2,y2 = v2.get_center()
	x = x1-x2
	y = y1-y2
	return x,y

def magnitude(x,y):
	"""return magnitude of a vector"""
	return math.sqrt(x*x+y*y)

def angle(x,y,degree=False):
	"""return angle of a vector, set deg=True to get angle in degree, otherwise it's radian"""
	if x != 0 and y !=0:
		ang = math.atan2(y,x)
	elif x==0 and y!=0:
		if y>0:
			ang =math.pi/2.0
		elif y<0:
			ang =-math.pi/2.0
	elif x==0 and y==0:
		ang = 0
	elif x!=0 and y==0:
		if x>0:
			ang = 0.0
		elif y<0:
			ang = math.pi
	else:
		ang = 0
	if not degree:
		return ang
	elif degree:
		return math.degrees(ang)

def to_cartesian(radius,angle):
	x = radius*math.cos(angle)
	y = radius*math.sin(angle)
	return x,y

def to_polar(x,y):
	radius = magnitude(x,y)
	ang = angle(x,y)
	return radius,ang

"""spesific function using in swarm dynamics"""
def distance_to_all(robot,swarm,use_radius = False):
	"""return sum of relative distance of robot to all robots in swarm"""
	if not use_radius: 
		x_total = 0
		y_total = 0
		for r in swarm.get_robots():
			x,y = distance(r,robot)
			x_total += x
			y_total += y
		return x_total,y_total
	elif use_radius:
		x_total = 0
		y_total = 0
		for r in swarm.get_robots():
			print r
			x,y = distance(r,robot)
			if magnitude(x,y)<robot.outer_radius*2:
				x_total += x
				y_total += y
		return x_total,y_total

def force_to_all(robot,swarm):
	safe_distance = robot.outer_radius*2
	f_x =0
	f_y = 0
	for r in swarm.get_robots():
		if robot.id != r.id:
			x,y = distance(r,robot)
			try:
				dis,ang = to_polar(x,y)
				k = dis/safe_distance
				f = (math.pow(k,-3)-math.pow(k,-2))*math.exp(-k)*-k
				fx,fy = to_cartesian(f,ang)
				f_x+=fx
				f_y+=fy
			except:
				f_x =0
				f_y = 0
	return f_x,f_y

if __name__ == '__main__':
	dy = safe_distance_dynamics(2)
	#dy = meeting_point_dynamics(2)
	dy.run()
	print 'started'
	raw_input()
	
