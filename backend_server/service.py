import operations
import pyjsonrpc

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

class RequestHandler(pyjsonrpc.HttpRequestHandler):
	"Test Method"
	@pyjsonrpc.rpcmethod
	def add(self, a, b):
		print "add is called with %d and %d" %(a,b)
		return a + b


	@pyjsonrpc.rpcmethod
	def getNewsSummariesForUser(self, user_id, page_num):
		return operations.getNewsSummariesForUser(user_id, page_num)
	@pyjsonrpc.rpcmethod
	def logNewsClickForUser(self, user_id, news_id):
		print 123445;
		return operations.logNewsClickForUser(user_id, news_id)

http_server = pyjsonrpc.ThreadingHttpServer(
	server_address = (SERVER_HOST, SERVER_PORT),
	RequestHandlerClass = RequestHandler
)

print "Starting Http server on %s: %d" %(SERVER_HOST, SERVER_PORT)
http_server.serve_forever()
