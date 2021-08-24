import pika
import asyncio
import sys
import os

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

queue = asyncio.Queue()
sleepFor = 1


class Send():
    async def rabbitmqSending(queue):
        while True:
            print('send')
            print(queue)
            body = await queue.get()
            channel.basic_publish(exchange='',
                                  routing_key='hello',
                                  body=body)
            print('Sent ', body)
            await asyncio.sleep(sleepFor)


class FibonacciGen():
    async def gen(timeToSleep, queue):
        n1, n2 = 0, 1
        while True:
            await queue.put(str(n1))
            print(queue)
            nth = n1 + n2
            n1 = n2
            n2 = nth
            await asyncio.sleep(sleepFor)


async def main():
    await asyncio.gather(
        FibonacciGen.gen(sleepFor, queue),
        Send.rabbitmqSending(queue),
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
