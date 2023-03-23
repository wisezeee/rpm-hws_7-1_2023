from fastapi import HTTPException, status
from config import TOKEN


def check_auth(auth: str):
    if auth != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="WRONG AUTH TOKEN",
        )


def check_title(titiles: list):
    for element in titiles:
        if element['title'].get('english') is None:
            element['title']['english'] = ''
    return titiles
