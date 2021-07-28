#importing
import time
import requests
import youtube_dl
from threading import Thread
import os
import datetime
import webbrowser
from plyer import notification 


#copyright
print ('Copyright © Nikolaos Allamanis all rights reserved.')
print('Chaturbate Downloader Created by : Nikolaos Allamanis')
print('NOTE : THIS PROGRAM IS NOT COMPLETED YET. THERE ARE MORE FEATURES I WOULD LIKE TO ADD IN THE FUTURE AND ALSO A LOT OF WAYS TO IMPROVE THE CODING!')




#This command finds the dir where the file is saved (The current directory).
current_directory = os.getcwd()

#creating Data folder and logs subfolder
dir = current_directory+'\\Chaturbate Downloader Data\\Logs\\'
try:
	os.makedirs(dir)
except:
	pass #path already exists
		



#defining variables.
#boolean which determines if the "Models.txt" file exists.
file_doesnt_exist = False
#A list for every model
models_list = []
#A list with booleans, which represents their broadcoasting status: Live = True, Offline = False
models_online_boolean_list = []
#A list for the models who are Live
models_online_list = []

#A list whom stream is available to download
models_download_list = []





#checking if Models.txt already exists, if not, it gets created.
try:
	file = open('Models.txt')
	file.close()
	#importing models to list
	with open('Models.txt', 'r') as file:
		models_list = file.readlines()
	#file.close()
	print('Sucessfully imported "Models.txt"')
	
except:
	print('Failed to import "Models.txt", file does not exist')
	file_doesnt_exist = True


#creating file	
if file_doesnt_exist == True:
	print('Creating "Models.txt" file (at current directory), please do NOT delete it.')
	time.sleep(1)
	file = open('Models.txt','a')
	file.close()
	print('File Created Successfully!')
	

if len(models_list) ==0:
	print('"Models.txt" is empty, make sure you add some models.')
	

#for example if there are 5 models in models.txt, then there should be one boolean (for each model) which declares if
#the model is live or not. Storing these variables in a list is very convenient. So here i am appending False to 
#models_online_boolean_list once, for each model
for i in range(len(models_list)):
	models_online_boolean_list.append(False)
	#doing the same thing for another list too
	models_online_list.append('')
	
	#also replacing space with _ in order to prevent youtube-dl errors
	models_list[i] = models_list[i].replace(" ","_")
	
	models_download_list.append('')

	

print('Loading Menu..')
time.sleep(1)


#creating a folder for each model
if len(models_list) > 0:
	for i in range (len(models_list)):
		#creating Data folder and logs subfolder
		dir = current_directory+'\\Chaturbate Downloader Data\\Logs\\' + models_list[i].replace("\n","")
		try:
			os.makedirs(dir)
			if i == (len(models_list))-1:
				print('Log files have been successfully created!')
		except:
			pass #path already exists
			
			

#creating main class
class main_class():
	
	
	def __init__(self):
		self.menu_choice = ''
		self.models_list = models_list
		self.model_name = ''
		self.user_decides = True
		self.chaturbate_url = 'https://en.chaturbate.com/'
		self.chaturbate_url2 = 'https://en.chaturbate.com/'
		self.response = 0
		
		#youtube-dl options
		self.ydl_opts = {'quiet': True,
		'no_warnings':True}
		#'ignoreerrors':True # i was hoping i would be able to use this in order to make the console less messy but
		#when this is set to True, it messes up the counting of the online models
		#because when a model is offline it gives an error. So when we ignore the errors, then all models appear
		#like they are online, which is false.
		#so what i did, is i went to youtube-dl files and disabled the command which prints the errors
		#lib/site-package/youtube-dl/extractor/chaturbate.py(line 36)
		#the problem is that every user who runs this program has to do the same...
		#unless i compile this
		#also there is a bug in youtube-dl, if the model's name contains a _ it prints a warning, but the file gets
		#downloaded like it should. It just makes the console messy :C
		
		
		self.keep_checking = False
		self.checking = ''
		self.models_online_boolean_list = models_online_boolean_list
		self.models_online_list = models_online_list
		self.models_online_str = ''
		self.stop_input = ''
		self.keep_asking = False
		self.already_started = False
		self.exit = False
		self.user_choice = ''
		self.user_downloading = False
		self.video_title = ''
		self.now = ''
		self.list_not_empty = False
		self.can_proceed = False
		self.models_download_list = models_download_list
		self.reset = False
		self.do_only_once = False
		self.model_online = False
		self.half_reset = False
		self.start_thread_only_once = False
		self.start = False
		self.trying_to_download = False
		self.takeover = False
		#this var is responsible for numering the online models and printing the results in a user-friendly way!
		self.model_numeration = 0
		self.enter = ''
		self.download_offline = False
		self.entered_return_to_menu = False
		self.current_directory = current_directory
		self.dir = self.current_directory+'\\Chaturbate Downloader Data\\Logs\\'
		
		#Thread Definitions
		self.t1 = Thread(target = self.check_and_download)
		self.t2 = Thread(target = self.stop)
		self.t3 = Thread(target = self.escape)
		self.t4 = Thread(target = self.remove_offline_models_from_list)
		self.t5 = Thread(target = self.recconect_or_return)
		self.donate_url = 'https://www.google.com/'
		self.notification_str =''
		self.q1 = ''
		#self.t4 = Thread(target=self.takeover_def)


	#creating menu def
	def menu(self):
		self.reset = False
		
		if self.half_reset == False:
			print('========================================================================================================')
			print('[1] Downloading streams of models who are currently online. ')
			print ('[2] Download streams of models who are offline. ')
			print ('[3] Add Models to Models.txt')
			print('[4] Help')
			print('[5] About')
			print('[6] Donate')
			print('[7] Exit')
			print('========================================================================================================')
			
			while True:
				try:
					self.menu_choice = int(input('Please choose a number : '))
					if int(self.menu_choice):
						self.user_decides = True
						break
				except:
					print('Invalid Value')
		
		while self.user_decides == True:
			if self.menu_choice == 1:
				self.user_decides = False
				
				
				#we need this check, because if the user returns to menu he/she will try to start a thread a 2nd time
				if self.already_started == False:
					#starting checking def
					self.t1.start()
					
					#starting stop def
					self.t2.start()
					
					self.already_started = True
				

				
				#if self.already_started == True then it means that the user has already run the checker at least once
				#that also means that both threads are still alive, so we can't try starting them again
				#all we got to do is set these 2 variables to True so the threads break the loop which keeps them
				#alive and start checking again
				else:
					self.keep_asking = True
					self.keep_checking = True
		
			
			elif self.menu_choice ==2:
				self.download_offline = True
				if self.start_thread_only_once == False:
					self.t3.start()
					self.start_thread_only_once = True
				
				self.download_only()

			
			
			
			
			
			
			elif self.menu_choice ==3:
				self.model_name = input("Enter model's name : ")
				if  self.model_name == '' or self.model_name ==' ' or self.model_name == '\n' :
					print("This model doesn't exist")
					#returning to menu
					proceed = input('Press enter to return to menu : ')	
					print('Returning to menu..')	
					time.sleep(1)
					self.return_to_menu()
				
				
				
				else:
						
						
					self.model_name = self.model_name.replace(" ","_")
					self.chaturbate_url += self.model_name+'/'
					
					#checking if model exists
					self.response =requests.get(self.chaturbate_url)
					
					#code 200 means that everything went okay, and the result has been returned (if any).
					if self.response.status_code ==200:
						#checking if model already exists in txt file
						if (self.model_name+'\n' not in self.models_list) and (self.model_name not in self.models_list):
							
							
							#appending to list
							self.models_list.append(self.model_name)
							
							
							#appending to boolean list
							self.models_online_boolean_list.append(False)
							
							
							#appending to models_online list
							self.models_online_list.append('')
							
							#appending to models_download_list list
							self.models_download_list.append('')
							
							#writing to txt file
							file = open('Models.txt','a')
							file.write(self.model_name+'\n')
							file.close()
							print('Model successfully added to "Models.txt"')
							
							
							#creating log files for model
							self.dir = self.current_directory+'\\Chaturbate Downloader Data\\Logs\\'
							self.dir += self.model_name
							try:
								os.makedirs(self.dir)
								print('Log files have been successfully created!')
							except:
								print('Failed to create log files for this model.')
														
						
						else:
							print('Model already exists in "Models.txt"')
							
							
							
					#code 404 means that the page was not found (model doesn't exist)
					elif self.response.status_code == 404:
						print("This model doesn't exist")
					
					
					#something else went wrong, maybe the server is down or the user is not connected to the internet etc
					else:
						print('Unknown error, please try again later.')
					


					#returning to menu
					proceed = input('Press enter to return to menu : ')	
					print('Returning to menu..')	
					time.sleep(1)
					self.return_to_menu()
				
			
			
			elif self.menu_choice ==4:
				print('---------------------Help--------------------')
				print('help works!')
				print('---------------------Help--------------------')
				proceed = input('Press enter to return to menu : ')
				print('Returning to menu..')
				time.sleep(1)
				self.return_to_menu()
				
				
			elif self.menu_choice==5:
				print('---------------------About--------------------')
				print ('Copyright © Nikolaos Allamanis all rights reserved.')
				print('Developer : Nikolaos Allamanis')
				print('Current Version : 1.0')
				print('---------------------About--------------------')
				proceed = input('Press enter to return to menu : ')
				print('Returning to menu..')
				time.sleep(1)
				self.return_to_menu()
				
				
				
			elif self.menu_choice == 6:
				webbrowser.open(self.donate_url)
				print('Thank you for supporting my work!!!')
				proceed = input('Press enter to return to menu : ')
				print('Returning to menu..')
				time.sleep(1)
				self.return_to_menu()
				
			
			
			
			elif self.menu_choice == 7:
				self.exit = True
				print('Exiting..')
				time.sleep(1)
				exit()
			
			else:
				print('Value not valid, please try again (this one)')
				print('Returning to menu..')
				time.sleep(1)
				self.return_to_menu()
				
				
				
	def escape(self):
		while self.exit == False:
			if self.start == True and self.model_online == False:
				self.enter = input('Press enter whenever you want to return to the menu : ')
				self.half_reset = False
				self.start = False
				self.takeover = True
				
				
				
				# #self.return_to_menu()
				# if self.t4.is_alive() == False:
					# self.t4.start()
	
	# def takeover_def(self):
		# while True:
			# if self.takeover == True:
				# self.return_to_menu()
			# else:
				# print('Den mpika')
				# print('self.start : ' ,self.start)
				# print('self.takeover : ' ,self.takeover)
				
				
	def download_only(self):
		#checking whether the models.txt file is empty or not
		if len(self.models_list) == 0:
			print('There are no models in the "Models.txt" file. Please make sure you add the models of your choice there.')
			print('For more help check the help section by typing "3" in the menu.')
			proceed = input('Press enter to return to menu : ')
			print('Returning to menu..')
			time.sleep(1)
			self.return_to_menu()
		
		
		
		
		elif self.do_only_once == False and self.half_reset == False and self.download_offline == True:
			self.do_only_once = True
			print ('=================================================Models=====================')
			for i in range (len(self.models_list)):
				print ('[',i+1,'] ', self.models_list[i])
			print ('=================================================Models=====================')
			while self.download_offline == True:
				self.user_choice = input('Enter the number of the model whom stream you want to download or press enter to return to the menu : ')
				try:
				#trying to int(self.user_choice) #if the command gets executed with no errors, then
				#it means that the str can be converted to int and that it's a valid value as well,
				#so we can proceed the download operation
					if self.user_choice == '':
						#returning to menu
						self.return_to_menu()
				
				
					#checking that the answer is valid
					elif  (int(self.user_choice)) > 0 and (int(self.user_choice)) < ((len(self.models_list))+1) :
						self.can_proceed = True
						break
						
					else:
						print('Invalid Value')
					
				except:
					#keep in mind that we are dealing with 4 threads here, boolean's value change frequently
					#so, this IF is neccessary
					if self.download_offline == True:
						print('Invalid Value')
				
			try:
				if self.can_proceed == True:
					#thread starts
					self.start = True
					self.half_reset = True
					self.trying_to_download = True
					while self.trying_to_download == True:
						self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						self.video_title = self.models_list[(int(self.user_choice))-1].replace("\n","") + str(self.now)+'.mp4'
						self.video_title = self.video_title.replace(":",".")
						#print('Title : ',self.video_title)
						self.chaturbate_url = 'https://en.chaturbate.com/' + self.models_list[(int(self.user_choice))-1].replace("\n","")+'/'
						#print('URL : ',self.chaturbate_url)
						ydl_opts = {
						'quiet': True
						}
						
						try:
							with youtube_dl.YoutubeDL(ydl_opts) as ydl:
								self.checking = ydl.extract_info(self.chaturbate_url, download=False)
								self.model_online = True
							
							#Models is online
							if self.model_online == True:
								
								#Notifying the user
								self.notification_str = self.models_list[(int(self.user_choice))-1].replace("\n","") + 'is now online! Download should start anytime soon!'
								notification.notify('Chaturbate Downloader 1.0',self.notification_str,app_icon = 'python_icon.ico')
								
								
								#Starting to download
								ydl_opts = {
								'outtmpl': self.video_title,
								'no_warnings':True
								}
								with youtube_dl.YoutubeDL(ydl_opts) as ydl:
									ydl.download([self.chaturbate_url])
									self.return_to_menu()
								
						
						
						
						except:
							if self.takeover == True:
								print('line 485')
								self.return_to_menu()
							
							
							#either model is offline or the user is trying to interrupt the download process.
							else:

								print('line 489')
								message = str(self.models_list[(int(self.user_choice))-1]).replace("\n","")+' is currently offline, continuing to check. '+self.now
								print(message)
								time.sleep(1)
								
						
				
			except:
				if self.trying_to_download == True:
					time.sleep(2)
					old_title = self.video_title+'.part'
					new_title = self.video_title.replace("part","")
					os.rename(old_title,new_title)
					print('Returning to menu..')
					print('URL : ',self.chaturbate_url)
					print('Video Title : ',self.video_title)
					time.sleep(1)
					self.return_to_menu()
			
	
	
		elif self.half_reset == True:
			try:
				if self.can_proceed == True:
					while True:
						self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						self.video_title = self.models_list[(int(self.user_choice))-1].replace("\n","") + str(self.now)+'.mp4'
						self.video_title = self.video_title.replace(":",".")
						#print('Title : ',self.video_title)
						self.chaturbate_url = 'https://en.chaturbate.com/' + self.models_list[(int(self.user_choice))-1].replace("\n","")+'/'
						#print('URL : ',self.chaturbate_url)
						ydl_opts = {
						'quiet': True
						}
						
						try:
							with youtube_dl.YoutubeDL(ydl_opts) as ydl:
								self.checking = ydl.extract_info(self.chaturbate_url, download=False)
								#Models is online, starting the download!
								self.model_online = True
							if self.model_online == True:
								ydl_opts = {
								'outtmpl': self.video_title,
								'no_warnings':True
								}
								with youtube_dl.YoutubeDL(ydl_opts) as ydl:
									ydl.download([self.chaturbate_url])
									self.return_to_menu()
								
						except:
							if self.takeover == True:
								self.return_to_menu()
							else:
								message = str(self.models_list[(int(self.user_choice))-1]).replace("\n","")+' is currently offline, continuing to check. '+self.now
								print(message)
								time.sleep(1)
				
			except:
				time.sleep(2)
				old_title = self.video_title+'.part'
				new_title = self.video_title.replace("part","")
				os.rename(old_title,new_title)
				print('Returning to menu..')
				print('URL : ',self.chaturbate_url)
				print('Video Title : ',self.video_title)
				time.sleep(1)
				self.return_to_menu()
			
	
	
	
	
	
	
	def recconect_or_return(self):
		while self.exit == False:
			if self.entered_return_to_menu == True and self.half_reset == True and self.takeover == False:
				#give some time to the downloader to exit
				time.sleep(2)
			
				#user is being asked whether a recconect attempt should be attempted or return to menu.
				self.q1 = input('Press enter to return to menu or a recconection attempt is going to happend in a few seconds : ')
				if len(self.q1) >=0:
					print('T5 : Returning to menu')
					self.half_reset = False
					self.takeover = False
					print('Booleans have been resetted')
					time.sleep(5)
			
			else:
				self.q1 = ''

	
	
	def return_to_menu(self):
		self.entered_return_to_menu = True
	
	
		if self.half_reset == True and self.takeover == False:
				
			print('Connection lost or model is offline.')
			print('self.half_reset : ',self.half_reset)
			print('self.takeover :',self.takeover)
			
			if self.t5.is_alive() == False:
				self.t5.start()
				
			
			#waiting for user to answer
			time.sleep(5)
			
			#a re-check is neccessary because the value of the boolean might have changed if the user answered	
			if self.half_reset == True and self.takeover == False:
				print('Connection lost, trying to recconect.')
				print('Trying to recconect in 3..')
				time.sleep(1)
				print('Trying to recconect in 2..')
				time.sleep(1)
				print('Trying to recconect in 1..')
				time.sleep(1)
				print('Recconecting..')
				time.sleep(1)
				
				#Reseting only the variables which are required in order to continue downloading offline
				self.user_decides = True
				#self.half_reset = False
				self.do_only_once = False
				self.start = False
				self.takeover = False
			
				


				# self.reset = True
				# self.response = 0
				# self.keep_checking = False
				# self.keep_asking = False
				# self.exit = False
				# self.user_downloading = False
				# self.list_not_empty = False
				# self.can_proceed = False
				# self.model_numeration = 0
				# self.do_only_once = False
				# self.model_online = False
				
				
				self.q1 = ''
				self.entered_return_to_menu = False
				print('Line 634')
				self.menu()
		
			else:
				self.q1 = ''
				self.entered_return_to_menu = False
				print('Line 640')
				self.return_to_menu()
		
		
		
		else:

			
			
			
			#Reseting all variables and then returning to menu
			#these variables have to be reset, otherwise the program doesn't work properly
			self.reset = True
			self.menu_choice = ''
			#self.models_list = []
			self.model_name = ''
			self.user_decides = False
			self.chaturbate_url = 'https://en.chaturbate.com/'
			self.chaturbate_url2 = 'https://en.chaturbate.com/'
			self.response = 0
			self.ydl_opts = {'quiet': True,
			'no_warnings':True}
			self.keep_checking = False
			self.checking = ''
			# self.models_online_boolean_list = self.models_online_boolean_list.clear()
			# self.models_online_list = self.models_online_list.clear()
			self.models_online_str = ''
			self.stop_input = ''
			self.keep_asking = False
			self.exit = False
			self.user_choice = ''
			self.user_downloading = False
			self.video_title = ''
			self.now = ''
			self.list_not_empty = False
			self.can_proceed = False
			# self.models_download_list = self.models_download_list.clear()
			self.model_numeration = 0
			self.do_only_once = False
			self.model_online = False
			self.trying_to_download = False
			self.half_reset = False
			self.takeover = False
			self.start = False
			self.download_offline = False
			
			# print('Len models list : ',len(self.models_list))
			# print('Len models online list : ',len(self.models_online_list))
			# print('Len models download list : ',len(self.models_download_list))
			# print('\n')
			# print('models list : ',self.models_list)
			# print('models download list : ',self.models_download_list)
			# print('models online list : ',self.models_online_list)
			# print('models online boolean list : ',self.models_online_boolean_list)
			
			
			
			#emptying lists
			
			
			#the length of models_online list and models_online_boolean list is the same
			for i in range(len(self.models_list)):
				self.models_online_boolean_list[i] = False
				self.models_online_list[i] = ''
				
				
			#the length of this list, is different than the others so we need a different "for" 	
			for i in range(len(self.models_download_list)):
				self.models_download_list[i] =''
				

		
			
			
			self.q1 = ''
			self.entered_return_to_menu = False
			print('Line 716')
			self.menu()
			

		
		
	def remove_offline_models_from_list(self):
		while self.exit == False:
			for i in range(len(self.models_online_list)):
				try:
					if self.models_online_list[i] != '' and len(self.models_online_list[i]) >0:
						with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
							self.chaturbate_url2 = 'https://en.chaturbate.com/' + self.models_online_list[i]+'/'
							#if the following command gets executed without any errors, then the model is online
							self.checking = ydl.extract_info(self.chaturbate_url2, download=False)
					
				
				
				
				except:
					self.models_online_list[i] = ''
					self.models_online_boolean_list[i] = False
	
	
	
	
	def stop(self):
		self.keep_asking = True
		while self.exit == False:
			if self.keep_asking == True and len(self.models_list) > 0:
				self.stop_input = input('Press enter when you want the checker to stop : ')

				
				#checking if the self.models_online_list, list is empty or not and then determining what to do
				for i in range (len(self.models_online_list)):
					if self.models_online_list[i] != "''" and len(self.models_online_list[i]) > 0:
						self.models_download_list = list(filter(('').__ne__, self.models_online_list))
						self.list_not_empty = True
						
				
				
				
				#this might get replaced in a future update
				#=================================================================================================
				
				#if the user left the checker running for way too long, there is a chance a model has gone offline
				#but appears online because so far there is no code implemented to remove a model from
				#self.models_online_list who at first was online and then went offline
				#so we need this "if" to check whether or not this has actually happend.
				#if this occurs, then the user returns to the menu.
				# if self.stop_input == '' and self.list_not_empty == True and sum(self.models_online_boolean_list) == 0:
					# self.keep_asking = False
					# self.keep_checking = False
					# print('There are no models in the "Models.txt" file. Please make sure you add the models of your choice there.')
					# print('For more help check the help section by typing "3" in the menu.')
					# proceed = input('Press enter to return to menu : ')
					# print('Returning to menu..')
					# time.sleep(1)
					# self.return_to_menu()
				#=================================================================================================
				
				
				
				
				if self.stop_input == '' and self.list_not_empty == True and sum(self.models_online_boolean_list) > 0:
					self.keep_asking = False
					self.keep_checking = False
					
					
					
					#flashing console
					print('', flush=True)
					#show results (if there are any)
					print('=====================Results=========================================')
					#printing results
					for i in range (len(self.models_download_list)):
						print('Download List : ',self.models_download_list)
						print('Online List : ',self.models_online_list)
						print('Boolean List : ',self.models_online_boolean_list)
						if len(self.models_download_list[i]) > 0 and self.models_online_boolean_list[self.models_online_list.index(self.models_download_list[i])] == True:
							print ('[',i+1,'] ',self.models_download_list[i])
					print('=====================Results=========================================')
					
						
						
					self.user_downloading = True
					while self.user_downloading == True:
						self.user_choice = input('Type the number of the model, whom stream you want to download, if you want to return to the menu, just press enter : ')
						if self.user_choice == '':
							print('Returning to menu..')
							time.sleep(1)
							self.return_to_menu()
							
						else:
							
							try:
								#trying to int(self.user_choice) #if the command gets executed with no problem, then
								#random check just to try to int the variable
								if  int(self.user_choice) :
									self.can_proceed = True
						
							except:
								print('Invalid Value')
						
						
						
						
							#the 2nd try will get executed and the download will start
							#else the except will get executed which means that the user entered an invalid value
							#we need 2 trys, because the 2nd one is repsonsible for youtube_dl
							#if an error occurs the 2nd try prevents youtube_dl from exiting the program
							try:
								if self.can_proceed == True:
									if (int(self.user_choice) >0) and (int(self.user_choice) < ((len(self.models_download_list))+1)):
										self.user_downloading = False
										print('Download List : ',self.models_download_list)
										print('Downloading')
										print('Models download list :',self.models_download_list)
										self.chaturbate_url = 'https://en.chaturbate.com/' + self.models_download_list[int(self.user_choice)-1] + '/'
										print('URL : ',self.chaturbate_url)
										#print('You might have to run this program again, if you want to use it again')
										print('Download Starting..')
										self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
										self.video_title = self.models_download_list[int(self.user_choice)-1] + str(self.now)+'.mp4'
										#windows doesn't let you to add ":" in a file's title, so we have to replace : with .
										self.video_title = self.video_title.replace(":",".")
										time.sleep(1)
										ydl_opts = {
										'outtmpl': self.video_title
										#'quiet': True
										}
										with youtube_dl.YoutubeDL(ydl_opts) as ydl:
											ydl.download([self.chaturbate_url])
										#returning to menu
										self.return_to_menu()
										
									else:
										print('Value not valid.')

								
							except:
								time.sleep(2)
								old_title = self.video_title+'.part'
								new_title = self.video_title.replace("part","")
								os.rename(old_title,new_title)
								print('Returning to menu..')
								print('URL : ',self.chaturbate_url)
								print('Video Title : ',self.video_title)
								time.sleep(1)
								self.return_to_menu()
									
						
					
					
					# else:
						# print('All models are offline at the moment, you can keep checking until someone goes online!')
					
					
					
					
					# print('Returning to menu..')
					# time.sleep(1)
					# self.return_to_menu()
				
				
				#self.models_online_list is empty, so there's nothing to download, returning to menu
				elif self.list_not_empty == False:
					print('No results to show. All models are offline at the moment, try again laster.')
					self.keep_asking = False
					self.keep_checking = False
					print('Returning to menu..')
					time.sleep(1)
					self.return_to_menu()
					
				
				
				
				#if the user types something else, don't crash/freeze
				else:
					pass
			
			else:
				self.keep_asking = False

	
	
	#this def is supposed to constantly keep checking and let the user know whenever which models are online.
	#Also the user is going to decide if he/she will be downloading any of the stream(s) or not
	def check_and_download(self):
		self.keep_checking = True
		while self.exit == False:
			if len(self.models_list) >0:
				#if the model was already in models.txt file, then there is also a "\n"
				#for example if the model's name is : test , then it's going to look like this : test\n
				#in order to check if the model is livestreaming or not, the "\n" has to get deleted
				#deleting "\n"
				for i in range(len(self.models_list)):
					self.models_list[i] = self.models_list[i].replace("\n","")
				
				
				
				
				
				
				#checking which models are online
				while self.keep_checking == True:
					for i in range(len(self.models_list)):
						try:
							with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
								self.chaturbate_url = 'https://en.chaturbate.com/' + self.models_list[i] +'/'
								#if the following commands get executed without any errors, then the model is online
								self.checking = ydl.extract_info(self.chaturbate_url, download=False)
								self.models_online_list[i] = self.models_list[i]
								self.models_online_boolean_list[i] = True
								
								
								#starting the thread which checks if the model goes offline,
								#if it does go offline, it gets deleted from the models_online_list
								if self.t4.is_alive() == False:
									self.t4.start()
								
								
								#print('Models Online (',sum(self.models_online_boolean_list),') : ',list(filter(('').__ne__, self.models_online_list)))
								#print('URL : ',self.chaturbate_url)
								
								
								
								
						
						#if line 337 gives an error then the model is offline
						#(Disabled -> ) Even though quiet mode is enabled, youtube-dl prints a message saying that the model is offline anyway
						except:
							self.models_online_boolean_list[i] = False
						
						
						
						
						
						#if no one is online, display a message.
						if sum(self.models_online_boolean_list) == 0 and self.keep_checking == True:
							print('All models are offline at the moment, continuing to check..')
							time.sleep(1)
				
						#else print how many and which models are online
						#the self.models_online_list, list contains the name of the models which are online
						#and some ''(s), so here, i am using this command : list(filter(('').__ne__, self.models_online_list)) in order to
						#remove all the ''(s)
						#i can't print the list like this : print(self.models_online_list) because i don't want to print the ''(s)
						#if i actually print it like this print(self.models_online_list)
						#the result will be something like : [example_model1,example_model2,'','','','',','','','','']
						else:
							#We need this "if" in order to prevent the program from printing extra times, after
							#self.keep_checking has already been set to False
							if self.keep_checking == True:
							
								print('Models Online (',sum(self.models_online_boolean_list),') : ',list(filter(('').__ne__, self.models_online_list)))
								print('T4 Life Status : ',self.t4.is_alive())
				
				
				else:
					self.keep_checking = False
			
			
			
			else:
				self.keep_checking = False
				self.keep_asking  =False
				print('There are no models in the "Models.txt" file. Please make sure you add the models of your choice there.')
				print('For more help check the help section by typing "4" in the menu.')
				proceed = input('Press enter to return to menu : ')
				print('Returning to menu..')
				time.sleep(1)
				self.return_to_menu()

			
#creating object
object = main_class()
object.menu()