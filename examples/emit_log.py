import pika
import sys
import postman

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymus.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

postman = postman.PostMan("localhost", "topic_logs")
postman.publish(routing_key, message)