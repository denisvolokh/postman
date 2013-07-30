import pika 
import sys
import postman

def print_received_messages(message):
	print "Message received: {0}".format(message)	

routing_keys = sys.argv[1:]
if not routing_keys:
	print >> sys.stderr, "Usage: %s [routing_key]" % \
                         (sys.argv[0],)
	sys.exit(1)

postman = postman.PostMan("localhost", "topic_logs")	
postman.monitor(routing_keys, print_received_messages)