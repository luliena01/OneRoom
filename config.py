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
		'img': 'D:\\workspace_intellij\\Flask\\OneRoom\\OneRoom\\templates\\files'
	},
	'Page': {
		'max_content': 3
	}
}
