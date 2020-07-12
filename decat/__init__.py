from decat.models.decat import Decat


_decat = Decat()


def decat(text):
	results = []
	try:
		_decat.load_text(text)
		results = _decat.extractor()
	except Exception as e:
		print(f'Decat Failed: {e}')
	return results