# squeeze_app api
import sys

from flask import Flask, request
from flask_restful import Resource, Api

from datetime import datetime
import psycopg2 as pg2, psycopg2.extras as pg2_extras
import ipdb


app = Flask(__name__)
api = Api(app)

# db credentials passed as variables at runtime
HOST = sys.argv[1]
PORT = int(sys.argv[2])
DBNAME = sys.argv[3]
USER = sys.argv[4]

# To be deleted
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
        conn = pg2.connect(host=HOST, port=PORT, dbname=DBNAME, user=USER)
        cur = conn.cursor(cursor_factory=pg2_extras.DictCursor)
        
        cur.execute('''
        		select user_id, username, email, first_name, last_name, created_on
        		from users
        		where user_id = {}'''.format(user_id))

        user_data = cur.fetchone()
        
        cur.close()
        conn.close()

        if user_data is None:
        	return {'error_msg': 'user not found'}, 404
        else:
	        return {
	        	'user_id': user_data['user_id'],
	        	'username': user_data['username'],
	        	'email': user_data['email'],
	        	'first_name': user_data['first_name'],
	        	'last_name': user_data['last_name'],
	        	'created_on': user_data['created_on'].timestamp(), # convert datetime to epoch
	        }
        
        # return {'hi': 'bro'},
        # return users.get(user_id)

    def put(self, user_id):
    	ipdb.set_trace()
    	users[user_id] = request.form['data']
    	return {user_id: users[user_id]}


api.add_resource(User, '/user/<int:user_id>')


if __name__ == '__main__':
    app.run(debug=True)