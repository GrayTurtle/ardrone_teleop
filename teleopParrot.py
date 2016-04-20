#!/usr/bin/env python
# Import the ROS libraries
import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class Actions:
	def droneTakeoff(self,takeoff):
		r=rospy.Rate(10) #e.g., r=rospy.Rate(50) is 50 Hz, adjust argument to desired frequency.
		msg=Empty()
		str = '%s' % rospy.get_time()
		rospy.loginfo(str)
		takeoff.publish(msg)
		rospy.loginfo(msg)
		r.sleep()

	def droneHover(self,hover):
		r=rospy.Rate(10) #e.g., r=rospy.Rate(50) is 50 Hz, adjust argument to desired frequency.
		msg=Twist()
		msg.linear.x=0
		msg.linear.y=0
		msg.linear.z=0
		msg.angular.x=0
		msg.angular.y=0
		msg.angular.z=0
		str = '%s' % rospy.get_time()
		rospy.loginfo(str)
		hover.publish(msg)
		rospy.loginfo(msg)
		r.sleep()

	def droneMovement(self,movement,state):
		##					##
		x_vel=state[0];y_vel=state[1];z_vel=state[2]
		x_angvel=state[3];y_angvel=state[4];z_angvel=state[5]
		## 					##
		r=rospy.Rate(10) #e.g., r=rospy.Rate(50) is 50 Hz, adjust argument to desired frequency.
		msg=Twist()
		msg.linear.x=x_vel
		msg.linear.y=y_vel
		msg.linear.z=z_vel
		msg.angular.x=x_angvel
		msg.angular.y=y_angvel
		msg.angular.z=z_angvel
		str = '%s' % rospy.get_time()
		rospy.loginfo(str)

		movement.publish(msg)
		rospy.loginfo(msg)
		r.sleep()

	def droneLand(self,land):
		r=rospy.Rate(10) #e.g., r=rospy.Rate(50) is 50 Hz, adjust argument to desired frequency.
		msg=Empty()
		str = '%s' % rospy.get_time()
		rospy.loginfo(str)
		land.publish(msg)
		rospy.loginfo(msg)
		r.sleep()

	def droneReset(self,reset):
		r=rospy.Rate(100) #e.g., r=rospy.Rate(50) is 50 Hz, adjust argument to desired frequency.
		msg=Empty()
		str = '%s' % rospy.get_time()
		rospy.loginfo(str)
		reset.publish(msg)
		rospy.loginfo(msg)
		r.sleep()

class Mine:
	def __init__(self):
		self.xgain = 1
		self.ygain = 1
		self.zgain = .3
		self.AR = Actions()
	def callback(self,data):
		msg=Twist()
		if data.buttons[0] == 1:
			self.AR.droneTakeoff(self.takeoff)
		elif data.buttons[7] == 1:
			self.AR.droneReset(self.reset)
		elif data.buttons[1] == 1:
			self.AR.droneLand(self.land)
		elif data.buttons[4] == 1:
			msg.angular.z = self.zgain
		elif data.buttons[5] == 1:
			msg.angular.z = -self.zgain
		else:
			msg.angular.z = 0	
		print data.axes[3:5]
		msg.linear.x=data.axes[4]*self.xgain
		msg.linear.y=data.axes[3]*self.ygain
		msg.linear.z=0
		msg.angular.x=0
		msg.angular.y=0
		self.pub.publish(msg)
		rospy.loginfo(msg)
	def listener(self):
		self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		self.takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
		self.land = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
		self.reset = rospy.Publisher('/ardrone/reset', Empty, queue_size=1)

if __name__=='__main__':
	
	me = Mine()
	me.listener()
	rospy.init_node("ARDroneTeleop_Joy", anonymous = True)
	rospy.Subscriber("/joy",Joy,me.callback)	
	rospy.spin()

