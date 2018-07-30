# squeeze_app api
from flask import Flask, request
from flask_restful import Resource, Api

from datetime import datetime
import ipdb

app = Flask(__name__)
api = Api(app)

users = {
	1: {'id': 1,
		'first_name': 'Wilson',
		'last_name': 'Zhen',
		'email': 'wilson@gmail.com',
		'created_at': datetime(2018,7,28).strftime('%Y-%m-%d'),
		'updated_at': datetime(2018,7,28).strftime('%Y-%m-%d'),
	},
	2: {'id': 2,
		'first_name': 'Jun',
		'last_name': 'Chen',
		'email': 'jun@gmail.com',
		'created_at': datetime(2018,7,28).strftime('%Y-%m-%d'),
		'updated_at': datetime(2018,7,28).strftime('%Y-%m-%d'),
	},
}

@app.route('/')
def index():
	return 'Welcome to the Squeeze App API\n'


class User(Resource):
    def get(self, user_id):
        # return {'hi': 'bro'},
        return users.get(user_id)

    def put(self, user_id):
    	ipdb.set_trace()
    	users[user_id] = request.form['data']
    	return {user_id: users[user_id]}


api.add_resource(User, '/user/<int:user_id>')


if __name__ == '__main__':
    app.run(debug=True)