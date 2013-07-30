
import pika
import time

class PostMan(object):

	def __init__(self, url, exchange):
		pika.log.setup(color=True)
		self.url = url
		self.exchange = exchange
		self.connect(url)

	
	def connect(self):
		try:
			self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.url))
			self.channel = self.connection.channel()
			self.channel.exchange_declare(exchange=self.exchange, type="topic")
		except Exception, e:
			pika.log.error("Error on Connect: {0}".format(e))
			pika.log.info("[*] Trying to re-connect in 2 seconds...")
			time.sleep(2)
			self.connect(self.url)	

	
	def publish(self, routing, message):
		try:
			self.channel.basic_publish(exchange=self.exchange,
									   routing_key=routing,
									   body=message)
		except Exception, e:
			pika.log.error("Error on Publish: {0}".format(e))
			pika.log.info("[*] Trying to publish again in 2 seconds...")
			time.sleep(2)
			self.connect(self.url)
			self.publish(routing, message)
		finally:	
			self.connection.close()	


	def monitor(self, routings, callback):
		if type(routings) == str:
			routings = [routings]

		def _callback(channel, method, properties, body):
			callback(body)

		try:
			result = self.channel.queue_declare(exclusive=True)
			self.queue_name = result.method.queue
			
			for routing_key in routings:
				self.channel.queue_bind(exchange=self.exchange,
										queue=self.queue_name,
										routing_key=routing_key)

			self.channel.basic_consume(_callback, 
									   queue=self.queue_name,
									   no_ack=True)
			self.channel.start_consuming()						   	
		except Exception, e:
			pika.log.error("Error on Monitor: {0}".format(e))
			pika.log.info("[*] Another attempt to monitor in 2 seconds...")
			time.sleep(2)
			self.connect(self.url)
			self.monitor(routings, callback)		
		


