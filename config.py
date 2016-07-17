CONFIG = {
	'Debug': True,

	'URL': 'localhost:5000',

	'Email_confirm': {
		'enable': False,
		'sender': 'confirm@Jungam.com'
	},

	'DB': {
		'url': 'localhost',
		'name': 'JUNGAM',
		'port': '5432',
		'username': 'jungam',
		'password': 'hyerim0720'
	},
	'Security': {
		'secret_key': "hyerim"
	},
	'Storage': {
		'log': 'D:\\workspace_intellij\\Flask\\OneRoom\\OneRoom\\templates\\logs',
		'img': {
			'path':'D:\\workspace_intellij\\Flask\\OneRoom\\OneRoom\\templates\\files',
			'max_size': {
				'width': 500,
				'height':500
			}
		}
	},
	'Page': {
		'max_content': 3
	}
}
