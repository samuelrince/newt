from fastapi import FastAPI
from pydantic import BaseModel


class Article(BaseModel):
    url: str
    title: str = None
    description: str = None


app = FastAPI()


@app.post("/post/")
async def post_article(article: Article):
    return article
