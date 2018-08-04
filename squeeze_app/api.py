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


@app.route('/')
def index():
    return 'Welcome to the Squeeze App API\n'


class UserList(Resource):
    def get(self):
        conn = pg2.connect(host=HOST, port=PORT, dbname=DBNAME, user=USER)
        cur = conn.cursor(cursor_factory=pg2_extras.DictCursor)        

        cur.execute('''
            SELECT user_id, username, email, first_name, last_name, created_on
            from users
            order by user_id
        '''
        )

        users = cur.fetchall()
        
        cur.close()
        conn.close()

        if users:
            return [
                {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'created_on': user['created_on'].timestamp(), # convert datetime to epoch
                } 
                for user in users
            ], 200
        else:
            return {'error_msg': 'no users :('}, 404

    def post(self):
        conn = pg2.connect(host=HOST, port=PORT, dbname=DBNAME, user=USER)
        cur = conn.cursor(cursor_factory=pg2_extras.DictCursor)
        
        if request.form:
            data = request.form
        elif request.json:
            data = request.json

        current_time = datetime.now()

        cur.execute(
            ''' INSERT INTO users (username, password, email, first_name, last_name, created_on, updated_on)
                VALUES (%(username)s, %(password)s, %(email)s, %(first_name)s, %(last_name)s, %(created_on)s, %(updated_on)s)
                RETURNING user_id;
            ''',
            {
                'username': data.get('username'),
                'password': data.get('password'),
                'email': data.get('email'),
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'created_on': current_time,
                'updated_on': current_time,
            }
        )

        user_id = cur.fetchone()['user_id']
        
        conn.commit()
        cur.close()
        conn.close()        

        return self.get()


class User(Resource):
    def get(self, user_id):
        conn = pg2.connect(host=HOST, port=PORT, dbname=DBNAME, user=USER)
        cur = conn.cursor(cursor_factory=pg2_extras.DictCursor)
        
        cur.execute('''
            SELECT user_id, username, email, first_name, last_name, created_on
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
            }, 200


    def put(self, user_id):
        conn = pg2.connect(host=HOST, port=PORT, dbname=DBNAME, user=USER)
        cur = conn.cursor(cursor_factory=pg2_extras.DictCursor)

        if request.form:
            data = request.form
        elif request.json:
            data = request.json
        
        current_data, response_code = self.get(user_id)
        current_time = datetime.now()

        #If the user doesn't exist, create the user. If the user does exist, update the user.        
        if response_code == 404:
            cur.execute(
                ''' INSERT INTO users (user_id, username, password, email, first_name, last_name, created_on, updated_on)
                    VALUES (%(user_id)s, %(username)s, %(password)s, %(email)s, %(first_name)s, %(last_name)s, %(created_on)s, %(updated_on)s)
                ''',
                {
                    'user_id': user_id,
                    'username': data.get('username'),
                    'password': data.get('password'),
                    'email': data.get('email'),
                    'first_name': data.get('first_name'),
                    'last_name': data.get('last_name'),
                    'created_on': current_time,
                    'updated_on': current_time,
                }
            )            
        elif response_code == 200:
            cur.execute(
                '''UPDATE users SET (username, email, first_name, last_name, updated_on) = 
                    (%(username)s, %(email)s, %(first_name)s, %(last_name)s, %(updated_on)s)
                    WHERE user_id = %(user_id)s
                ''', 
                {
                    'user_id': user_id,
                    'username': data.get('username', current_data['username']),
                    'email': data.get('email', current_data['email']),
                    'first_name': data.get('first_name', current_data['first_name']),
                    'last_name': data.get('last_name', current_data['last_name']),
                    'updated_on': current_time,
                }
            )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return self.get(user_id)


api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<int:user_id>')


if __name__ == '__main__':
    app.run(debug=True)