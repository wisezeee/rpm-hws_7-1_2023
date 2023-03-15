# Project runs up FastAPI server, which can take data from anilist and do REST API on your own server.

# How install
_$ sudo apt-get update_

_$ docker pull mongo_

_$ git clone https://github.com/Max2288/rpm-hws_7-1_2023/_


# How run
Add .env file with your data

Go to folder with project and run commands:

_$ docker run -d -p 27018:27017 mongo_

_$ python3.10 -m venv ./venv_

_$ . ./venv/bin/activate_

_$ pip install -r requirements.txt_

# After start


## anilist.co

Example of data that we recieve: 
    
    {
        "id": movie id,
        "siteUrl": link to movie,
        "title": {
            "english": title's name on english,
            "native": title's anem on native
            },
        "description": movie's description
    }

## POST request

You can post media on page /media (Postman recommended)

* Go to Postman
* Header example: _http://HOST:PORT/media?auth=TOKEN_


Example of data that we send to post: 

    {
        "id": movie id: int,
        "siteUrl": link to movie: str,
        "title": {
            "english": title's name on english: str,
            "native": title's anem on native: str
            },
        "description": movie's description: str
    }

## PUT request

You can update media on page /media (Postman recommended)

* Go to Postman
* Header example: _http://HOST:PORT/media?auth=TOKEN_


Example of data that we send to update: 

    {
        "id": movie id: int,
        "siteUrl": link to movie: str,
        "title": {
            "english": title's name on english: str,
            "native": title's anem on native: str
            },
        "description": movie's description: str
    }

## DELETE request

You can delete media from page /media (Postman recommended)

* Go to Postman
* Header example: _http://HOST:PORT/media?id=MOVIEIDTODELETE&auth=TOKEN_


# .env
## Below should be your data to project
    HOST - app and database host
    PORT - database host
    DBNAME - database name
    COLNAME - collection name
    TOKEN - token to do REST API (should be - MAX228)
    APP_PORT - application port
