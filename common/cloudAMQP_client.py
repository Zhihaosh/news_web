import json
import pika

class CloudAMQPClient:
    def __init__(self, clound_ampq_url, queue_name):
        self.clound_ampq_url = clound_ampq_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(clound_ampq_url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def sendMessage(self, message):
        self.channel.basic_publish(exchange="",
                                    routing_key=self.queue_name,
                                    body=json.dumps(message)) #stringfy json
        print "%s:%s" %(self.queue_name,message)
        return

    def getMessage(self):
        method_frame, header_frame, body=self.channel.basic_get(self.queue_name)
        if method_frame is not None:
            print "[O] Received message from %s: %s" %(self.queue_name,body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print "no message returned"
            return None

    def sleep(self, second):
        self.connection.sleep(second)
