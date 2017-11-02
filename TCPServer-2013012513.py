from socket import *
import chardet
#import request


class Request(object):
	"A simple http request object"
	
	def __init__(self, raw_request):
		self._raw_request = raw_request
		
		self._method, self._path, self._protocol, self._headers = self.parse_request()
	
	def parse_request(self):
		"Turn basic request headers in something we can use"
		temp = [i.strip() for i in self._raw_request.splitlines()]
		
		if -1 == temp[0].find(str.encode('HTTP')):
			raise InvalidRequest('Incorrect Protocol')
		
		# Figure out our request method, path, and which version of HTTP we're using
		method, path, protocol = [i.strip() for i in temp[0].split()]
		
		# Create the headers, but only if we have a GET reqeust
		headers = {}
		if 'GET' == method:
			for k, v in [i.split(':', 1) for i in temp[1:-1]]:
				headers[k.strip()] = v.strip()
		else:
	
		return method, path, protocol, headers
	
	def __repr__(self):
		return repr({'method': self._method, 'path': self._path, 'protocol': self._protocol, 'headers': self._headers})


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',80))
serverSocket.listen(1)

print ("The server is ready to receive")

while 1:
        connectionSocket, addr = serverSocket.accept()
        print("Connection is accepted from "+ str(addr))
        sentence = connectionSocket.recv(1024)

        print(sentence)
        req = Request(sentence)
        connectionSocket.send(repr(req))

        connectionSocket.close()



