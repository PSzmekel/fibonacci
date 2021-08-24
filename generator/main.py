import pika
import time
import sys
import os

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


class Send():
    def rabbitmqSending(body):
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=body)
        print('Sent ', body)
        time.sleep(5)


class FibonacciGen():
    n1, n2 = 0, 1

    def gen(self):
        while True:
            Send.rabbitmqSending(str(self.n1))
            nth = self.n1 + self.n2
            self.n1 = self.n2
            self.n2 = nth


def main():
    fib = FibonacciGen()
    fib.gen()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
