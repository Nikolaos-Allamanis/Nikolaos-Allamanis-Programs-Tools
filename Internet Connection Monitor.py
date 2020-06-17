#importing
from urllib.request import urlopen
import urllib.error
import os
import datetime
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
import time
from threading import Thread
import numpy as np

#defining variables
times_checked_list = []
connection_status_list= []
status = ''
times_checked =0
connection_status =0
color = 'yellow'

#This commands finds the dir where the Internet Connection Checker.py is saved (The current directory).
current_directory = os.getcwd()


#creating a def which will be able to create folders
def createFolder(directory):
    try:
	#checking if the folder exists already or not
        if not os.path.exists(directory):
	#if it doesn't then, create it
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

#creating folder 'Logs' in current directory
createFolder('Logs')


class main_class(tk.Tk):
	def __init__(self):
		
		#defining variables
		self.program_running = True
		self.status = status
		self.times_checked_list = times_checked_list
		self.connection_status_list = connection_status_list
		self.times_checked =times_checked
		self.connection_status = connection_status
		self.color = color
		self.current_directory = current_directory
		self.thread_alive = False
		self.graph_showing = False
		self.t2 = Thread(target=self.graph_checker)
		self.figure_number = 'a number'
		self.graph_created = False
		self.t2_started = False
		self.graph_interrupted = False
		self.checking = True
		
		
		#creating parent tkinter window
		self.window = tk.Tk()
		self.window.title("Internet Connection Checker by Nikolaos Allamanis")
		self.window.geometry("250x200")
		self.window.configure(background='grey')
		self.start_button = Button(self.window,text = "Start",command =self.start, activebackground = 'green',bg='white',height = 5,width = 11)
		self.start_button.place(x = 3, y = 0)
		
		
		#buttons
		#show graph button
		self.show_graph_button = Button(self.window,text = "Show Graph",command=self.show_graph, activebackground = 'orange',bg='white',height = 5,width = 10)
		self.show_graph_button.place(x=90,y=0)
		
		#hide graph button (will get placed later)
		self.hide_graph_button = Button(self.window,text = "Hide Graph",command=self.hide_graph, activebackground = 'orange',bg='white',height = 5,width = 10)
		
		#save figure button
		self.save_figure_button = Button(self.window,text='Save Graph',command=self.save_figure,height = 5, width = 10)
		self.save_figure_button.place(x=170,y=0)
		
		#exit button
		self.exit_button = Button(self.window,text='Exit',command=self.exit,width = 35,height=1,bg='red')
		self.exit_button.place(x=0,y=85)
		
		#times_checked labels
		self.times_checked_var = IntVar()
		self.times_checked_var.set(self.times_checked)
		self.times_checked_label = Label(self.window,text = 'Times Checked : ',bg = 'blue',fg='yellow',height = 2,width = 12)
		self.times_checked_label.place(x =0,y=120)
		self.times_checked_label2 = Label(self.window,textvariable=self.times_checked_var,height= 2,bg='#C99314',fg='white',width = 12)
		self.times_checked_label2.place(x =93,y=120)
		
		#color vars
		self.color_var = StringVar()
		self.color_var.set(self.color)
		
		#status labels
		self.status_var = StringVar()
		self.status_var.set(self.status)	
		self.status_label = Label(self.window,text = 'Status : ',bg='black',fg='white',height = 2,width = 12)
		self.status_label.place(x =0,y=160)
		self.status_label2 = Label(self.window,textvariable =self.status_var,bg='Green',fg=self.color_var.get(),height = 2,width = 12)
		self.status_label2.place(x =93,y=160)
		self.stop_button = Button(self.window,text='Pause',command=self.pause,bg='white',height = 5,width = 11)
		
		messagebox.showinfo("Copyright :", "Copyright © Nikolaos Allamanis 2020 All Rights Reserved.")
		self.window.mainloop()
		
	
	#this def saves a screenshot of the graph in the current directory
	def save_figure(self):
		
		if self.times_checked<= 1:
			messagebox.showinfo("Error", "There is no graph to save, click on the start button to make one.")
		
		elif self.graph_showing == False:
			messagebox.showinfo("Error", "You must first click on the show graph button and then you can click save.")
		
		
		else:
			fig1 =plt.gcf()
			graph_name = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +'.jpg'
			graph_name = graph_name.replace(':', '.') 
			fig1.savefig(graph_name, dpi=300)
			messagebox.showinfo("Success!", "Save Successfull!!!")
	
	
	#this def is supposed to tell the user to close the graph and to stop the checker in order to prevent some
	#errors
	def exit(self):
		
		if self.thread_alive == True:
			messagebox.showinfo("Error", "Make sure you pause the checker before exiting.")
			
		if self.graph_showing == True:
			messagebox.showinfo("Error", "Make sure you close the graph before exiting.")
		
		elif self.thread_alive == False and self.graph_showing == False:
			
			#destroying parent window
			self.window.destroy()
			#exiting console
			exit()
	
	
#this def is supposed to check if the user closes the graph window by clicking the x button on the
#top right, instead of clicking the hide graph button
#if this happens then this def will replace the hide graph button with the show graph button and reset some
#booleans as well
	def graph_checker(self):
		while self.program_running == True:
			#we need time.sleep(1) in order to prevent this thread from running too many times and using too much
			#cpu power or ram memory
			time.sleep(1)
			
			#so basically this checks if the user has clicked on the show graph button
			if self.graph_showing == True and self.graph_created == True:
				#and then checks if the graph exists
				if plt.fignum_exists(self.figure_number):
					#if it does, then nothing happens
					pass
					
				
				
				#if it doesn't exist then user closed the graph window by clicking the x button
				#so we should replace the buttons and reset the booleans
				else:
					self.graph_showing = False
					self.graph_created = False
					#hiding hide button
					self.hide_graph_button.place_forget()
					#placing show graph button
					self.show_graph_button.place(x=90,y=0)
					self.graph_interrupted = True
				
				
				
			else:
				self.program_running = True
	
	
	
	
	
	
	#this def is supposed to close the graph window
	def hide_graph (self):
		#the graph window is supposed to close, so this boolean should change to False
		self.graph_showing = False
		
		#hiding hide button
		self.hide_graph_button.place_forget()
		
		#placing show graph button
		self.show_graph_button.place(x=90,y=0)
		
		
		
		#closing graph window
		plt.close()
		
		
		
	
	#this def is supposed to run some checks and determine if the graph should be shown
	def show_graph(self):
		
		if self.t2_started == False:
			self.t2_started = True
			self.t2.start()
			
		#when this boolean is set to true then we know that the user has clicked the show graph button	
		self.graph_showing = True
		
		#if the user clicks the start button then the buttons should be replaced
		#also if the graph gets interupted then the self.graph_interrupted boolean must set back to False
		if self.times_checked > 0 or self.graph_interrupted == True :
			self.graph_interrupted = False
			#hiding show graph button
			self.show_graph_button.place_forget()
			#placing hide graph button
			self.hide_graph_button.place(x=90,y=0)
			
		
		#if self.times_checked < 1 1 then the user hasn't clicked the start button yet, so there's no data 
		#to make a graph
		if self.times_checked < 1:
			messagebox.showinfo("Error :", "There is no data to create a graph, please click on the start button.")
				
		#if everything is ok, then show the graph		
		else:
			messagebox.showinfo("Info","If the graph window gets on top of all the other programs/windows, then click on the minimize button which is located on the top right side of the window.")
			self.graph_showing = True
			self.graph_shower()
			
			
			
	#this def creates a graph
	def graph_shower(self):
		while self.graph_showing == True:
			self.figure_number = plt.gcf().number
			plt.xlabel('Times Checked')
			plt.ylabel('Connection Status')
			plt.plot(np.array(self.times_checked_list),np.array(self.connection_status_list))
			self.graph_created = True
			plt.pause(2)
		
	#this def will start the first thread
	#thread is required because tkinter crashes when a def includes time.sleep() in main gui
	def start(self):

		#hiding start button
		self.start_button.place_forget()
		#placing pause button
		self.stop_button.place(x = 3, y = 0)
		
		
		self.t1 = Thread(target = self.internet_checker)
		
		#setting these booleans to false in order to make sure that the thread is not already running
		self.thread_alive = False
		self.checking = False
		
		
		
		#setting some booleans to True in order to start the thread
		self.thread_alive = True
		self.checking = True
		self.t1.start()
		self.thread_alive = True
		self.checking = True
		
		
	#this def will pause the checker		
	def pause(self):
		self.t1 = Thread(target = self.internet_checker)
		#hiding pause button
		self.stop_button.place_forget()
		
		#placing start button
		self.start_button.place(x = 3,y = 0)
	

		#stopping the thread
		self.thread_alive = False
		self.checking = False
		
		
		
	#this is the def which determines if the user is connected to the internet by contacting a google server
	def internet_checker(self):
		while self.thread_alive == True:
			while self.checking == True:
				#updating self.times_checked_var
				self.times_checked_var.set(self.times_checked)
				now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				
				#trying to contact A Google server
				#http://216.58.206.206 is the ip of the google server 
				try:
						
						connection_check = urlopen('http://216.58.206.206',timeout = 3)
						#writing connection status and connection date/time to Successfuly_Connected_Log.txt
						text = open(self.current_directory+'\\Logs\\Successfully_Connected_Log.txt','a')
						str1 = 'Succesfully Connected : '+str(now)
						text.write(str1)
						text.write("\n")
						text.close()
						#closing the connection to prevent the program from crashing in future socket timeouts
						connection_check.close()
						
						# self.times_checked_list is the x axis of the graph, so every time we call internet_checker we must add 1
						self.times_checked += 1
						self.times_checked_list.append(self.times_checked)
						
						#if the user is connected, then the graph should be stable
						self.connection_status = 1
						self.connection_status_list.append(self.connection_status)
						
						#changing label's color to yellow if connected
						self.color = 'yellow'
						self.color_var.set(self.color)
						self.status_label2.config(fg=self.color_var.get())
						
						#changing self.status to connected
						self.status = 'Connected'
						self.status_var.set(self.status)
			
			
			
				except urllib.error.URLError as err: 
						#writing connection status and connection date/time to Lost_Connection_Log.txt
						text = open(self.current_directory+'\\Logs\\Lost_Connection_Log.txt','a')
						str2 = 'Connection Lost : '+str(now)
						text.write(str2)
						text.write("\n")
						text.close()
						
						# self.times_checked is the x axis of the graph, so every time we call internet_checker we must add 1
						self.times_checked += 1
						self.times_checked_list.append(self.times_checked)
						
						#if the user is not connected, then the graph should be going down
						self.connection_status = 0
						self.connection_status_list.append(self.connection_status)
						
						#changing label's color to red if not connected
						self.color = '#e75d5c'
						self.color_var.set(self.color)
						self.status_label2.config(fg=self.color_var.get())
						
						#changing self.status to not connected
						self.status = 'Not Connected'
						self.status_var.set(self.status)
		
				#checking every 1 second
				time.sleep(1)



call = main_class()
call()