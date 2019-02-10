from urllib import request
from sys import argv
import os
import json

def check_image(resolution, operator):
	"""Creates a function to validate the image resolution."""
	return eval('lambda r: r %s resolution' % operator)

board, resolution, operator, directory = argv[1:] + [''] * 4
image_filter = check_image(tuple(map(int, resolution.split('x'))), operator)

if not os.path.exists(directory):
	os.makedirs(directory)

req = request.urlopen('https://a.4cdn.org/%s/threads.json' % board)
pages = json.loads(req.read().decode())
threads = [thread['no'] for threads in pages for thread in threads['threads']]
images_saved = 0

for thread in threads:
	req = request.urlopen('https://a.4cdn.org/{}/thread/{}.json'.format(board, thread))
	posts = json.loads(req.read().decode())
	filenames = [str(post['tim']) + post['ext'] for post in posts['posts'] if 'w' in post and image_filter((post['w'], post['h']))]

	for filename in filenames:
		req = request.urlopen('https://i.4cdn.org/{}/{}'.format(board, filename))

		with open(os.path.join(directory, filename), 'wb') as file:
			file.write(req.read())

	images_saved += len(filenames)

print('Found {} wallpapers on /{}/!'.format(images_saved, board))