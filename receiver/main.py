import pika
import sys
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import exc, sessionmaker  
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    'postgresql://postgres:mysecretpassword@localhost:5432/postgres',
    echo=True)

session = sessionmaker(bind=engine)


class Fib(Base):
    __tablename__ = 'fibnumbers'
    id = Column(Integer, primary_key=True)
    fib = Column(String)
    read = Column(Boolean, unique=False, default=False)

    def add(_fib):
        newFib = Fib(fib=_fib)
        session.add(newFib)
        try:
            session.commit()
        except exc.IntegrityError as ex:
            session.rollback()
            return ex
        return None


def main():
    connection = pika.BlockingConnection(
                 pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        Fib.add(body.decode())
        print(" [x] Received %r inserted to db" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback,
                          auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        Base.metadata.create_all(engine)
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
