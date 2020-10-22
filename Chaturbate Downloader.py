#importing
import time
import requests
import youtube_dl
from threading import Thread
import os
import datetime



#copyright
print('Chaturbate Downloader Created by : Nikolaos Allamanis')
print ('Copyright © Nikolaos Allamanis all rights reserved.')




#This commands finds the dir where the file is saved (The current directory).
current_directory = os.getcwd()

#creating Data folder and logs subfolder
dir = current_directory+'\\Data\\Logs'
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
	print('"Models.txt" file is empty, make sure you add some models.')
	

#for example if there are 5 models in models.txt, then there should be one boolean (for each model) which declares if
#the model is live or not. Storing these variables in a list is very convenient. So here i am appending False to 
#models_online_boolean_list once, for each model
for i in range(len(models_list)):
	models_online_boolean_list.append(False)
	#doing the same thing for another list too
	models_online_list.append('')
	
	#also replacing space with _ in order to prevent youtube-dl errors
	models_list[i] = models_list[i].replace(" ","_")
	
	

	
	

print('Loading Menu..')
time.sleep(1)





#creating main class
class main_class():
	
	
	def __init__(self):
		self.menu_choice = ''
		self.models_list = models_list
		self.model_name = ''
		self.user_decides = True
		self.chaturbate_url = 'https://en.chaturbate.com/'
		self.response = 0
		
		#youtube-dl options
		self.ydl_opts = {'quiet': True,
		'no_warnings':True,
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
		}
		
		
		self.keep_checking = False
		self.checking = ''
		self.models_online_boolean_list = models_online_boolean_list
		self.models_online_list = models_online_list
		self.models_online_str = ''
		self.t1 = Thread(target = self.check_and_download)
		self.t2 = Thread(target = self.stop)
		self.stop_input = ''
		self.keep_asking = False
		self.already_started = False
		self.exit = False
		self.user_choice = ''
		self.user_downloading = False
		self.video_title = ''
		self.now = ''
		


	#creating menu def
	def menu(self):
		print('========================================================================================================')
		print('[1] Start Checking ')
		print ('[2] Add Models to Models.txt')
		print('[3] Help')
		print('[4] About')
		print('[5] Exit')
		print('========================================================================================================')
		self.menu_choice = int(input('Please choose a number : '))
		
		while self.user_decides == True:
			if self.menu_choice == 1:
				self.user_decides = False
				
				
				#we need this check, because if user returns to menu he/she will try to start a thread a 2nd time
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
							
							#writing to txt file
							file = open('Models.txt','a')
							file.write(self.model_name+'\n')
							file.close()
							print('Model successfully added to "Models.txt"')
						
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
				
			
			
			elif self.menu_choice ==3:
				print('---------------------Help--------------------')
				print('help works!')
				print('---------------------Help--------------------')
				proceed = input('Press enter to return to menu : ')
				print('Returning to menu..')
				time.sleep(1)
				self.return_to_menu()
				
				
			elif self.menu_choice==4:
				print('---------------------About--------------------')
				print ('Copyright © Nikolaos Allamanis all rights reserved.')
				print('Developer : Nikolaos Allamanis')
				print('Current Version : 1.0')
				print('---------------------About--------------------')
				proceed = input('Press enter to return to menu : ')
				print('Returning to menu..')
				time.sleep(1)
				self.return_to_menu()
				
				
				
			
			
			elif self.menu_choice == 5:
				self.exit = True
				print('Exiting..')
				time.sleep(1)
				exit()
			
			else:
				print('Value not valid, please try again')
				print('Returning to menu..')
				time.sleep(1)
				self.return_to_menu()
			
	
	
	def return_to_menu(self):
		#reseting variables and then returning to menu
		#these variables have to be reset, otherwise the program doesn't work properly
		self.menu_choice = ''
		self.model_name = ''
		self.user_decides = True
		self.chaturbate_url = 'https://en.chaturbate.com/'
		self.response = 0
		self.keep_asking = False
		self.keep_checking = False
		self.user_downloading = False
		self.menu()
	
	
	
	
	def stop(self):
		self.keep_asking = True
		while self.exit == False:
			if self.keep_asking == True and len(self.models_list) > 0:
				self.stop_input = input('Press enter when you want the checker to stop : ')
				if self.stop_input == '':
					self.keep_asking = False
					self.keep_checking = False
					
					
					#flashing console
					print('', flush=True)
					#show results (if there are any)
					if len(self.models_online_list) > 0:
						print('=====================Download=========================================')
						for i in range (len(self.models_online_list)):
							if self.models_online_list[i] != "''" and len(self.models_online_list[i]) > 0:
								print ('[',i,'] ',self.models_online_list[i])
						print('=====================Download=========================================')
						
						
						
						self.user_downloading = True
						while self.user_downloading == True:
							self.user_choice = input('Type the number of the model, whom stream you want to download, if you want to return to the menu, just press enter : ')
							if self.user_choice == '':
								print('Returning to menu..')
								time.sleep(1)
								self.return_to_menu()
							
							else:
								try:
									if (int(self.user_choice) >0) and (int(self.user_choice) < len(self.models_online_list)):
										self.user_downloading = False
										print('Downloading')
										self.chaturbate_url = 'https://en.chaturbate.com/' + self.models_online_list[int(self.user_choice)] + '/'
										print('URL : ',self.chaturbate_url)
										print('You might have to run this program again, if you want to use it again')
										print('Download Starting..')
										self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
										self.video_title = str(self.models_online_list[int(self.user_choice)]) + str(self.now)
										#windows doesn't you to add ":" in a file's title, so we have to replace : with .
										self.video_title = self.video_title.replace(":",".")
										time.sleep(1)
										ydl_opts = {
										'outtmpl': self.video_title
										}
										with youtube_dl.YoutubeDL(ydl_opts) as ydl:
											ydl.download([self.chaturbate_url])
										
									else:
										print('Value not valid.1')

								
								except:
									old_title = self.video_title+'.part'
									new_title = self.video_title+'.mp4'
									os.rename(old_title,new_title)
									print('Returning to menu..')
									print('URL : ',self.chaturbate_url)
									print('Video Title : ',self.video_title)
									time.sleep(1)
									self.return_to_menu()
								
					
					
					
					
					else:
						print('All the models are offline at the moment, you can keep checking until someone goes online!')
					
					
					
					
					# print('Returning to menu..')
					# time.sleep(1)
					# self.return_to_menu()
				
				#if the user types something else, don't crash
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
								self.models_online_boolean_list[i] = True
								self.models_online_list[i] = self.models_list[i]
								
								
								#print('Models Online (',sum(self.models_online_boolean_list),') : ',list(filter(('').__ne__, self.models_online_list)))
								#print('URL : ',self.chaturbate_url)
								
								
								
								
						
						#if line 337 gives an error then the model is offline
						#(Disabled -> ) Even though quiet mode is enabled, youtube-dl prints a message saying that the model is offline anyway
						except:						
							self.models_online_boolean_list[i] = False
						
						
						
						
						
						#if no one is online, display a message.
						if sum(self.models_online_boolean_list) == 0:
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
			
				
				
				else:
					self.keep_checking = False
			
			
			
			else:
				self.keep_checking = False
				self.keep_asking  =False
				print('There are no models in the "Models.txt" file. Please make sure you add the models of your choice there.')
				print('For more help check the help section by typing "3"')
				proceed = input('Press enter to return to menu : ')
				print('Returning to menu..')
				time.sleep(1)
				self.return_to_menu()

			
#creating object
object = main_class()
object.menu()