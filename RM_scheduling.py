#!/usr/bin/env python3
# ------------------------------------------
# RM_scheduling.py: Rate Monotonic Scheduler
# Author: Ragesh RAMACHANDRAN
# ------------------------------------------

import json
import copy
from sys import *
from math import gcd
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np

tasks = dict()
RealTime_task = dict()
d = dict()
dList = []
T = []
C = []
U = []
# For gantt chart
y_axis  = []
from_x = []
to_x = []

def Read_data():
	"""
	Reading the details of the tasks to be scheduled from the user as 
	Number of tasks n:
	Period of task P:
	Worst case excecution time WCET:
	""" 
	global n
	global hp
	global tasks

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
	with open('tasks.json','w') as outfile:
		json.dump(tasks,outfile,indent = 4)

def Hyperperiod():
	"""
	Calculates the hyper period of the tasks to be scheduled
	"""
	temp = []
	for i in range(n):
		temp.append(tasks[i]["Period"])
	HP = temp[0]
	for i in temp[1:]:
		HP = HP*i//gcd(HP, i)
	print ("\n Hyperperiod:",HP)
	return HP

def Schedulablity():
	"""
	Calculates the utilization factor of the tasks to be scheduled 
	and then checks for the schedulablity and then returns true is 
	schedulable else false.
	"""
	for i in range(n):
		T.append(int(tasks[i]["Period"]))
		C.append(int(tasks[i]["WCET"]))
		u = int(C[i])/int(T[i])
		U.append(u)

	U_factor = sum(U)
	if U_factor<=1:
		print("\nUtilization factor: ",U_factor, "underloaded tasks")

		sched_util = n*(2**(1/n)-1)
		print("Checking condition: ",sched_util)

		count = 0
		T.sort()
		for i in range(len(T)):
			if T[i]%T[0] == 0:
				count = count + 1

		# Checking the schedulablity condition
		if U_factor <= sched_util or count == len(T):
			print("\n\tTasks are schedulable by Rate Monotonic Scheduling!")
			return True
		else:
			print("\n\tTasks are not schedulable by Rate Monotonic Scheduling!")
			return False
	print("\n\tOverloaded tasks!")
	print("\n\tUtilization factor > 1")		
	return False

def estimatePriority(RealTime_task):
	"""
	Estimates the priority of tasks at each real time period during scheduling
	"""
	tempPeriod = hp
	P = -1    #idle task
	for i in RealTime_task.keys():
		if (RealTime_task[i]["WCET"] != 0):
			if (tempPeriod > RealTime_task[i]["Period"] or tempPeriod > tasks[i]["Period"]):
				tempPeriod = tasks[i]["Period"]
				P = i		
	return P

# Bug1: Not preempting tasks
def Simulation(hp): 
	"""
	The real time schedulng based on Rate Monotonic scheduling is simulated here.
	"""
	# Real time scheduling are carried out in RealTime_task
	RealTime_task = copy.deepcopy(tasks)
    # validation of schedulablity neessary condition
	for i in RealTime_task.keys():
		RealTime_task[i]["DCT"] = RealTime_task[i]["WCET"]  
		if (RealTime_task[i]["WCET"] > RealTime_task[i]["Period"]):				
			print(" \n\t The task can not be completed in the specified time ! ", i )	
	
	# main loop for simulator
	for t in range(hp):

		# Determine the priority of the given tasks
		priority = estimatePriority(RealTime_task)
		global dList

		if (priority != -1):    #processor is not idle
			print("\nt{}-->t{} :TASK{}".format(t,t+1,priority))
			# Update WCET after each clock cycle
			RealTime_task[priority]["WCET"] -= 1
			# For the calculation of the metrics
			d = dict(Task=priority, Start=t, Finish=t+1)      	
			dList.append(d.copy()) 
			# For plotting the results
			y_axis.append("TASK%d"%priority)
			from_x.append(t)
			to_x.append(t+1)

		else:    #processor is idle
			print("\nt{}-->t{} :IDLE".format(t,t+1))
			# For the calculation of the metrics
			d = dict(Task="IDLE", Start=t, Finish=t+1)
			dList.append(d.copy())
			# For plotting the results
			y_axis.append("IDLE")
			from_x.append(t)
			to_x.append(t+1)


		# Update Period after each clock cycle
		for i in RealTime_task.keys():
			RealTime_task[i]["Period"] -= 1
			if (RealTime_task[i]["Period"] == 0):
				RealTime_task[i] = copy.deepcopy(tasks[i])


def drawGantt():
	"""
	The scheduled results are displayed in the form of a 
	gantt chart for the user to get better understanding
	"""
	colors = ['red','green','blue','orange','yellow']
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax = plt.hlines(y_axis, from_x, to_x, linewidth=20, color = colors[n-1])
	plt.title('Rate Monotonic scheduling')
	plt.grid(True)
	plt.xlabel("Real-Time clock")
	plt.ylabel("HIGH------------------Priority--------------------->LOW")
	plt.xticks(np.arange(min(from_x), max(to_x)+1, 1.0))
	plt.show()

def showMetrics():
    """
    Displays the resultant metrics after scheduling such as
    average response time, the average waiting time and the 
    time of first deadline miss
    """
    print("Metrics not calculated for now")

if __name__ == '__main__':

	Read_data()
	sched_res = Schedulablity()

	if sched_res == True:
		hp = Hyperperiod()
		Simulation(hp)
		drawGantt()
	else:
		Read_data()
		sched_res = Schedulablity()