'''
Scraping Reddit for pictures and videos and uploading their urls to a MongoDB database.
'''

import praw
import time
from pymongo import MongoClient
#from imgurpython import ImgurClient

subreddit = 'Subreddit_to_scrap'
title = 'Name_in_DB'

def redditContent(doc):
	r = praw.Reddit('webapi:scraper:v0.0.1 (by /u/shim2k)github.com/shim2k')
	r.login('testUser', 'testPass')
	posts = []
	subreddit = doc
	submissions = r.get_subreddit(subreddit).get_hot(limit=500)
	if submissions:
		for sub in submissions:
			if sub:
				print sub.id
				if sub.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.apng', '.gifv')):
					item = { "title" : title,
							 "description": sub.title,
							 "date": time.strftime("%D %H:%M", time.localtime(int(sub.created_utc))),
							 "url": sub.url,
							 "tag": subreddit,
							 "vid": isVideo(sub.title)}
					posts.append(item)
		return posts

def isVideo(string):
	if "gif" in string.lower():
		return "true"
	else:
		return "false"

def insertToDatabase():
	client = MongoClient('mongodb://NAME:test@ds061631.mongolab.com:61631/NAME')
	db = client['NAME']
	posts = db.posts
	titles = db.titles

	item = { "title": title, "tag": subreddit }

	#bool(db.titles.find_one({ 'title': 't' }))
	result = posts.insert_many(redditContent(subreddit))
	result = titles.insert_one(item).inserted_id

insertToDatabase()

'''
def imgurContent():
	client_id = 'CLIENT_NAME'
	client_secret = 'CLIENT_SECRET'

	client = ImgurClient(client_id, client_secret)

	for album in client.get_account_albums('ALBUM-NAME'):
		album_title = album.title if album.title else 'Untitled'
		print('Album: {0} ({1})'.format(album_title, album.id))

		for image in client.get_album_images(album.id):
		    image_title = image.title if image.title else 'Untitled'
		    print('\t{0}: {1}'.format(image_title, image.link))
'''
