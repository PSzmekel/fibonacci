from flask import Flask, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:'\
                                        'mysecretpassword@localhost'\
                                        ':5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Fib(db.Model):
    __tablename__ = 'fibnumbers'
    id = db.Column(db.Integer, primary_key=True)
    fib = db.Column(db.String)
    read = db.Column(db.Boolean, unique=False, default=False)

    def json(self):
        return {'id': self.id, 'fib': self.fib}

    def get():
        fib = Fib.query.filter(Fib.read.is_(False)).order_by(
              Fib.id.asc()).first()
        if fib is None:
            return None
        fib.read = True
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
        return fib.json()


@app.route('/next', methods=['GET'])
def getNext():
    json = Fib.get()
    if json is None:
        return Response("no more data", status=404,
                        mimetype='application/json')
    return jsonify({'fib': json})


if __name__ == "__main__":
    app.run(port='5000', debug=True)
