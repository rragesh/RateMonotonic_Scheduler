# ------------------------------------------
# RM_scheduling.py: Rate Monotonic Scheduler
# Author: Ragesh RAMACHANDRAN
# ------------------------------------------

import json
import copy
from sys import *
from math import gcd
from collections import OrderedDict

tasks = dict()
T = []
C = []
U = []


def Read_data():

	# Reading number of tasks to be scheduled
	global n
	global hp
	n = int(input("\n \t\tEnter number of Tasks:"))

	#  Storing data in a dictionary
	for i in range(n):
		tasks[i] = {}
		print("\n\n\n Enter Period of task T",i,":")
		p = input()
		tasks[i]["Period"] = int(p)
		print("Enter the WCET of task C",i,":") 
		w = input() 
		tasks[i]["WCET"] = int(w)

	# Writing the dictionary into a JSON file
	with open('/home/ragesh/SCHEDULING/tasks.json','w') as outfile:
		json.dump(tasks,outfile,indent = 4)


def Hyperperiod():

	# Calculation of Hyper period
	temp = []
	for i in range(n):	
		temp.append(tasks[i]["Period"])
	HP = temp[0]
	for i in temp[1:]:
		HP = HP*i//gcd(HP, i)
	print ("\n Hyperperiod:",HP)
	return HP

def Schedulablity():

	# Calculation of utilization factor
	for i in range(n):
		T.append(int(tasks[i]["Period"]))
		C.append(int(tasks[i]["WCET"]))
		u = int(C[i])/int(T[i])
		U.append(u)

	U_factor = sum(U)
	print("\nUtilization factor: ",U_factor)
	sched_util = n*(2**(1/n)-1)
	print("Checking condition: ",sched_util)

	# Checking the schedulablity condition
	if U_factor <= sched_util:
		print("\n\tTasks are schedulable!")
		return True
	else:
		print("\n\tTasks are not schedulable!")
		return False


def Exact_schedulablity():
	# For the time being this is not required	
	return False
def estimatePriority(RealTime_task):
	lessPeriod = hp	
	P = -1
	for i in RealTime_task.keys():
		if (RealTime_task[i]["WCET"] != 0):
			if (lessPeriod > RealTime_task[i]["Period"]):
				P = i
				lessPeriod = RealTime_task[i]["Period"]
	return P


def Simulation(hp):
	# Real time scheduling are carried out in RealTime_task
	RealTime_task = dict(tasks)		
	print(RealTime_task)
	
	
	for t in range(hp):

		# validation of schedulablity neessary condition	
		for i in RealTime_task.keys():
			if (RealTime_task[i]["WCET"] > RealTime_task[i]["Period"]):
				print(" \n\t The task can not be cmopleted in the specified time ! ", i )

		# Determine the priority of the given tasks
		priority = estimatePriority(RealTime_task)
		if (priority != -1):
			print("\nt{}-->t{} :TASK{}".format(t,t+1,priority))
		else:
			print("\nt{}-->t{} :IDLE".format(t,t+1))			

		# Update WCET time after execution 
		RealTime_task[priority]["WCET"] -= 1

		# Update period time
		for i in RealTime_task.keys():
			RealTime_task[i]["Period"] -= 1
			if (RealTime_task[i]["Period"] == 0):
				RealTime_task = dict(tasks)



if __name__ == '__main__':
	
	Read_data()
	sched_res = Schedulablity()
	hp = Hyperperiod()
	if sched_res == True:
		Simulation(hp)
	else:
		Simulation(hp)
		# Exact_schedulablity()
