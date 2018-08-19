squeeze_app
=============

#### To activate virtual environment
```
$ workon squeeze_app
```

#### To deactivate virtual environment
```
$ deactivate
```

#### To install the required packages
Make sure your virtual environment is activated, then run:
```
$ pip install -r requirements.txt
```

#### To start the server
Go to the `squeeze_app` directory containing `api.py`, then run:
```
$ python api.py
```

#### To create `users` table
Run this query in whichever postgres db you're using.
```
-- DDL generated by Postico 1.4.2
-- Not all database features are supported. Do not use for backup.

-- Table Definition ----------------------------------------------

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username character varying(50) NOT NULL UNIQUE,
    password character varying(50) NOT NULL,
    email character varying(355) NOT NULL UNIQUE,
    first_name character varying(50),
    last_name character varying(50),
    created_on timestamp without time zone NOT NULL DEFAULT now(),
    updated_on timestamp without time zone,
    last_login timestamp without time zone
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX users_pkey ON users(user_id int4_ops);
CREATE UNIQUE INDEX users_username_key ON users(username text_ops);
CREATE UNIQUE INDEX users_email_key ON users(email text_ops);
```
