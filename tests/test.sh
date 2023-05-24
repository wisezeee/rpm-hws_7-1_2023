#!/bin/bash

# set env variables
python3.10 tests/setup_env.py

# set up database
python3.10 tests/setup_db.py

# server start
echo "Starting the server"
python3.10 main.py &

# real tests
sleep 2

OK=200
CREATED=201

token=f9f668fc-e868-4c09-947b-6a07b3850d5c
function check_code () {
    if [[ $1 -eq $2 ]]
    then
        echo "OK"
    else
        echo "FAILED, CODE: $1"
        exit 1
    fi
}

echo "simple_GET request:"

get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8001/population`

check_code $get_code $OK

echo "POST request:"

post_code=`curl -s -o /dev/null \
    -X POST \
    -d '{"fname": "a1b2c3d4", "lname":"abcdef", "group_":"1"}' \
    -H "Authorization:admin {$token}"\
    -w %{http_code} \
    http://127.0.0.1:8001/population`

check_code $post_code $CREATED


echo "query_GET request:"

get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8001/population?name=France`

check_code $get_code $OK

echo "DELETE request:"

post_code=`curl -s -o /dev/null \
    -X DELETE \
    -H "Authorization:admin {$token}"\
    -w %{http_code} \
    http://127.0.0.1:8001/population?name=France`

check_code $post_code $OK
