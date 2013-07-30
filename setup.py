from distutils.core import setup

setup(
    name='postman',
    version='0.1.0',
    author='Denis Volokh',
    author_email='denis.volokh@gmail.com',
    packages=['aamnotifs'],
    url='http://github.com/denisvolokh/postman',
    description='Publish/monitor implementation with RabbitMQ using pika.',
    install_requires=[
        "pika",
    ],
)