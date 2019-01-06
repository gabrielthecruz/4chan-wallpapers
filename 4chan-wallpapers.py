from sys import argv as args
import requests
import json
import os

"""
Checks the resolution of a post image.
"""
def check_post(post, resolution, limit):
	if 'filename' not in post.keys() or limit not in ['max', 'min', 'equal']  and post['ext'] != 'jpg':
		return False

	results = {
		'equal': (post['w'], post['h']) == resolution,
		'max'  : post['w'] <= resolution[0] and post['h'] <= resolution[1],
		'min'  : post['w'] >= resolution[0] and post['h'] >= resolution[1]
	}

	return results[limit]

configs = {
	'resolution': tuple(map(int, args[2].split('x'))),
	'limit'     : args[3],
	'folder'    : (args[4] if args[4].endswith('/') else args[4] + '/') + '%s',
	'api_urls'  : 'https://a.4cdn.org/%s/' % args[1]
}

if not os.path.exists(configs['folder'][:-2]):
	os.makedirs(configs['folder'][:-2])

pages   = json.loads(requests.get(configs['api_urls'] + 'threads.json').text)
threads = [thread['no'] for threads in pages for thread in threads['threads']]
images_saved = 0

for thread in threads:
	posts = json.loads(requests.get(configs['api_urls'] + 'thread/%d.json' % thread).text)['posts']

	for post in filter(lambda post: check_post(post, configs['resolution'], configs['limit']), posts):
		filename = str(post['tim']) + post['ext']

		with open(configs['folder'] % filename, 'wb') as file:
			file.write(requests.get('https://i.4cdn.org/%s/%s' % (args[1], filename)).content)

		images_saved += 1

print('Found %d wallpapers on /%s/!' % (images_saved, args[1]))