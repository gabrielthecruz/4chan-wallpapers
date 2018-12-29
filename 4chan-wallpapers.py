import requests
import json
from sys import argv as args

board, width, height, limit, folder = args[1:] or ['wg', '1920', '1080', '-1', './Wallpapers']

limit = int(limit)
resolution = (int(width), int(height))
folder = (folder if folder.endswith('/') else folder + '/') + '%s'

t_api_url  = 'https://a.4cdn.org/%s/' % board
i_api_url  = 'https://i.4cdn.org/%s/' % board
resolution = (str(width), str(height))

pages = json.loads(requests.get(t_api_url + 'threads.json').text)
threads = [val['no'] for sublist in pages for val in sublist['threads']]

for thread in threads:
	print('Searching in thread no.%d' % thread)
	posts = json.loads(requests.get(t_api_url + 'thread/%d.json' % thread).text)['posts']

	for post in filter(lambda post: 'filename' in post.keys() and (post['w'], post['h']) == resolution, posts):
		filename = str(post['tim']) + post['ext']

		image_request = requests.get(i_api_url + filename, 'wb')
		with open(folder % filename, 'wb') as image_file:
			image_file.write(image_request.content)

		print('\tSaved ' + filename)
