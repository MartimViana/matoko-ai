from ai import *

def loadActions():
	return [
		CheckTime(['time']),
		DownloadVideoFromYoutube(['get','video','from','youtube']),
		RunCommand(['run']),
		GetIPInfo(['probe', 'ip']),
		OpenNotion(['open','notion']),
		OpenTheTrove(['open','thetrove']),
		OpenMessenger(['open', 'messenger']),
		OpenDiscord(['open', 'discord']),
		DownloadAudioPlaylistFromYoutube(['get', 'audio', 'from', 'youtube', 'file']),
		DownloadAudioFromYoutube(['get','audio','from','youtube']),
	]

if __name__=='__main__':
	print("Matoko AI")
	actions = loadActions()
	helper = Helper('Matoko', actions)
	helper.greet()
	helper.start()
