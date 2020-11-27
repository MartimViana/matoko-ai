import os
import socket

class Action():
	def __init__(self, input):
		self.input = input

	def run(self, input):
		args = self.getArgs(input)
		self.execute(args)

	def execute(self, args):
		print("DEFAULT ACTION EXECUTION")

	def match(self, input):
		for i in range(min(len(self.input), len(input))):
			if self.input[i] != input[i]:
				return False
		return True

	def getArgs(self, input):
		return input[len(self.input):]

	def getInput(self):
		result = ''
		for word in self.input:
			result += word + ' '
		return result

'''
	Checks current system time.
'''
from datetime import datetime
class CheckTime(Action):
	def __init__(self, input):
		super().__init__(input)

	def execute(self, args):
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print("It's", current_time)

'''
	Download video from youtube.
'''
import youtube_dl
class DownloadVideoFromYoutube(Action):
	def __init__(self, input):
		super().__init__(input)

	def execute(self, args):
		print('Downloading video '+args[0])
		ydl_opts = {
		    'prefer_ffmpeg': True,
		    'keepvideo': True
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([args[0]])

'''
	Download audio from youtube.
'''
import youtube_dl
class DownloadAudioFromYoutube(Action):
	def __init__(self, input):
		super().__init__(input)

	def execute(self, args):
		print('Downloading audio '+args[0])
		ydl_opts = {
			'writethumbnail':True,
		    'format': 'bestaudio/best',
		    'postprocessors': [{
		        'key': 'FFmpegExtractAudio',
		        'preferredcodec': 'mp3',
		        'preferredquality': '192',
		        #'id3v2_version' : 3,
		    },
		    {'key': 'EmbedThumbnail',},],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([args[0]])

class DownloadAudioPlaylistFromYoutube(Action):
	def __init__(self, input):
		super().__init__(input)
		self.path = '/home/martim/Desktop'	# setup path here

	def execute(self, args):
		runCommand = RunCommand('')
		currentDir = ''
		cnt = 1
		with open(args[0], 'r') as f:
			line = f.readline()
			print("{}: {}".format(cnt, line))
			while line:
				if line.startswith('#'):
					currentDir = line[1:]
					#runCommand.execute('mkdir '+line[1:])

				elif line != '' and line != '\n':
					self.downloadLink(line, currentDir)
				line = f.readline()
				cnt += 1

	def downloadLink(self, link, dirname):
		print('Downloading audio '+link)
		ydl_opts = {
			'writethumbnail':True,
		    'format': 'bestaudio/best',
		    'yes-playlist': True,
		    'postprocessors': [{
		        'key': 'FFmpegExtractAudio',
		        'preferredcodec': 'mp3',
		        'preferredquality': '192',
		        #'id3v2_version' : 3,
		        }],
		    'outtmpl': dirname+'/%(playlist_index)s - %(title)s.%(ext)s'
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			try:
				ydl.download([link])
			except:
				print("Couldn't download link "+link)


'''
	Executes linux command
'''
class RunCommand(Action):
	def __init__(self, input):
		super().__init__(input)
		#self.previous_command = []

	def execute(self, args):
		# get command in executable shape
		cmd = ''
		for a in args:
			cmd+=a+' '
		#self.previous_command.append(cmd)

		# in order to conserve consistency, run all previous commands
		#for c in self.previous_command:
		#	os.system(c)
		os.system(cmd)

'''
	Get information about IP
'''
import ipinfo
class GetIPInfo(Action):
	def __init__(self, input):
		super().__init__(input)
		access_token = '8b9ced379b102b' # my ipinfo.io access token
		self.handler = ipinfo.getHandler(access_token)


	def execute(self, args):
		for ip in args:
			details = self.handler.getDetails(ip)
			self.printDetails(ip, details.all)
			self.printOpenPorts(ip)

	def printDetails(self, ip, details):
		printDictLayer(0, details)

	def printOpenPorts(self, ip):
		decision = input('Check for open ports? (y/n) ')
		if decision == 'y':
			maxRange = int(input('Maximum port to be attempted: '))
			getOpenPorts(ip, maxRange)
			print('Done.')

'''
	open firefox on the notion website
'''
class OpenNotion(Action):
	def __init__(self, input):
		super().__init__(input)

	def execute(self, args):
		rc = RunCommand([])
		rc.execute(['firefox','-new-tab','"notion.so"','&'])

'''
	open firefox on the thetrove website
'''
class OpenTheTrove(Action):
	def __init__(self, input):
		super().__init__(input)

	def execute(self, args):
		rc = RunCommand([])
		rc.execute(['firefox','-new-tab','"thetrove.net/Books/"','&'])

'''
	open the facebook messenger CLI
'''
class OpenMessenger(Action):
	def __init__(self, input):
		super().__init__(input)

	def execute(self, args):
		rc = RunCommand([])
		rc.execute(['fb-messenger-cli'])

'''
	open the discord messenger CLI
'''
class OpenDiscord(Action):
	def __init__(self, input):
		super().__init__(input)

	def execute(self, args):
		rc = RunCommand([])
		rc.execute(['cordless'])

## FUNCTIONS
def layerToTab(layer):
	str = ''
	for i in range(layer):
		str+='\t'
	return str

'''
	This function allows to print a nested dictionary in multiple layers.
'''
def printDictLayer(layer, d):
	for name in d:
		output = layerToTab(layer)+name+':'
		value = d.get(name)
		if type(value) is dict:
			print(output)
			printDictLayer(layer+1,value)
		else: 
			output+=' '+str(value)
			print(output)

'''
	Checks if a specific ip has any open ports by attempting to connect to
	the ip by the attempted port.
'''
from contextlib import closing
def getOpenPorts(ip, maxRange):
	result = []
	for port in range(maxRange):
		with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
			if sock.connect_ex((ip, port)) == 0:
				print('Port '+str(port)+' is open')
				result.append(port)
	return result