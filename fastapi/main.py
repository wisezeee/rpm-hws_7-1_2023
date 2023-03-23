from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse, JSONResponse
from config import *
import uvicorn
import requests
from database import fill_database, get_from_db, update_db, delete_from_db
from pydantic import BaseModel
from checker import check_auth, check_title


class Media(BaseModel):
    id: int
    siteUrl: str
    title: dict
    description: str

    def to_dict(self):
        return self.__dict__


app = FastAPI()
env = Environment(loader=FileSystemLoader('templates'), autoescape=True)


@app.get("/")
async def root():
    template = env.get_template('home.html')
    content_to_user = template.render()
    return HTMLResponse(content=content_to_user)


@app.get("/media_api")
async def media_api():
    response = requests.post(URL, json={'query': QUERY})
    data_to_user = check_title(response.json()['data']['Page']['media'])
    template = env.get_template('index.html')
    content_to_user = template.render(data=data_to_user)
    return HTMLResponse(content=content_to_user)


@app.get("/media_api/{index}")
async def media_api_pages(index: int):
    response = requests.post(URL, json={'query': QUERY})
    data_to_user = check_title(response.json()['data']['Page']['media'])
    template = env.get_template('media.html')
    content_to_user = template.render(data=data_to_user[index - 1])
    return HTMLResponse(content=content_to_user)


@app.get("/media")
async def media():
    data_to_user = get_from_db(CLIENT)
    template = env.get_template('my_index.html')
    content_to_user = template.render(data=data_to_user)
    return HTMLResponse(content=content_to_user)


@app.get("/media/{index}")
async def media_pages(index: int):
    temprorary_data = [element for element in get_from_db(CLIENT) if element['_id'] == index]
    data_to_user = temprorary_data[0]
    template = env.get_template('media.html')
    content_to_user = template.render(data=data_to_user)
    return HTMLResponse(content=content_to_user)


@app.post("/media", status_code=CREATED)
async def create_media(title: Media | None = None, auth: str = None):
    check_auth(auth)
    mes = fill_database(CLIENT, title.to_dict())
    return mes if mes else MESSAGE.format('created')


@app.put("/media")
async def update_media(title: Media | None = None, auth: str = None):
    check_auth(auth)
    mes = update_db(CLIENT, title.to_dict()['id'], title.to_dict())
    if mes and not isinstance(mes, int):
        return mes
    return MESSAGE.format('updated') if mes else 'You alredy update data!'


@app.delete("/media")
async def delete_media(id_from_user: int | None = None, auth: str = None):
    check_auth(auth)
    status_rec = delete_from_db(CLIENT, id_from_user)
    if not status_rec:
        resp_content = {"message": "Item not found"}
        return JSONResponse(content=resp_content, status_code=NOT_FOUND)
    return MESSAGE.format('deleted')

if __name__ == "__main__":
    uvicorn.run(app, host=HOST)
