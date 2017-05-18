import requests

input_str = 'how are you?'
ret = requests.get('http://127.0.0.1:5000/?q={}'.format(input_str) )

print(ret.text)
