

NPR_ROOT       = 'http://api.npr.org'
API_KEY        = 'MDAyNTU3MTA2MDEyMjk2NTE1MzEwN2U0MQ001'
LIST_URL       = NPR_ROOT + '/list?apiKey=' + API_KEY
QUERY_URL      = NPR_ROOT + '/query?numResults=20&apiKey=' + API_KEY
SEARCH_URL     = NPR_ROOT + '/query?startNum=0&sort=dateDesc&output=NPRML&numResults=20&apiKey=' + API_KEY
CACHE_INTERVAL = 600

dirs = [ ['Topics', '3002'], 
				 ['Music Genres', '3018'], 
				 ['Programs' , '3004'],
				 ['Bios' , '3007'],
				 ['Music Artists' , 'music'],
				 ['Columns' , '3003'],
				 ['Series' , '3006'] ]
				 
musicDirs = [ ['Recent Artists', '3008'],
							['All Artists', '3009'] ]

####################################################################################################

def Start():
	Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
	ObjectContainer.art = R('art-default.jpg')
	DirectoryObject.thumb = R('icon-default.jpg')

####################################################################################################
@handler('/music/npr', 'NPR', thumb='icon-default.jpg', art='art-default.jpg')
def MainMenu():
	oc = ObjectContainer()
	for name, value in dirs:
		if value == 'music':
            oc.add(DirectoryObject(key=Callback(MusicMenu), title=name))
		else:
			dir.Append(Function(DirectoryItem(SectionMenu, title=name), id=value))
            oc.add(DirectoryObject(key=Callback(SectionMenu, id=value, name=name), title=name))
    ###TODO - implement Search Service ###
	#dir.Append(Function(InputDirectoryItem(Search, title="Search...", prompt="Search NPR", thumb=R("icon-search.png"))))
	return oc

####################################################################################################
@route('/music/npr/music')
def MusicMenu():
	oc = ObjectContainer(title2="Music Artists")
	for name, value in musicDirs:
        oc.add(DirectoryObject(key=Callback(SectionMenu, id=value, name=name), title=name))
	return oc
	
####################################################################################################
@route('/music/npr/section')
def SectionMenu(id, name):
	oc = ObjectContainer(title2=name)
	maxNumToReturn = 200
	for item in XML.ElementFromURL(LIST_URL + '&id=' + id, cacheTime=CACHE_INTERVAL).xpath('//item'):
        oc.add(DirectoryObject(key=Callback(StoryMenu, id=item.get('id'), name=item.get('title')),
            title=item.get('title'), summary=item.get('additionalInfo')))
		if id == '3008':
			maxNumToReturn = maxNumToReturn - 1
			if maxNumToReturn <= 0: 
				break
	return oc

####################################################################################################

def StoryMenu(id, name):
	oc = ObjectContainer(title2=name)
	dir.Extend(ParseStories(QUERY_URL + '&id=' + id))
	if len(dir) == 0:
		return MessageContainer('No Audio', 'No audio files were found in this section.')
	return dir

####################################################################################################
def GetThumb(url):
  if url:
    try:
      data = HTTP.Request(url, cacheTime=CACHE_1MONTH).content
      return DataObject(data, 'image/jpeg')
    except:
      pass

  return Redirect(R('icon-default.jpg'))

####################################################################################################
# I think this shouldn't be necessary at all #
def S(item, attr): 
    try:
		return item.find(attr).text.replace('<em>','').replace('</em>','').replace('&mdash;','-')
	except:
		return ''

####################################################################################################
###TODO - implement Search Service ###
#def Search(sender, query):
#    dir = MediaContainer(viewGroup='Details', title2="Search: " + query)
#	url = SEARCH_URL + '&searchTerm=' + query.replace(' ', '%20')
#	dir.Extend(ParseStories(url))
#	return dir

####################################################################################################
# This will likely be handled by the new URL Service #
def PlayMusic(url):
	target = HTTP.Request(url, cacheTime=CACHE_INTERVAL).content.split('\n')[0]
	target = target.split('<', 1)[0]
	return Redirect(target)
