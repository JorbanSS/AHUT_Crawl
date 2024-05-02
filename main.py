from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api import recent_contests, admin, rating, codeforces

description = """
python3 + FastAPI + scrapy
"""


tags_metadata = [
    {
        'name': 'recent contests',
        'description': '各大 OJ 平台近期比赛'
    }
]

app = FastAPI(
    title='AHUT OJ 爬虫专项',
    version='0.1',
    description=description,
    root_path='/api',
    openapi_tags=tags_metadata,
    redoc_url=None,
)

origins = [
    'http://localhost:8090',
    'https://localhost:8090',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recent_contests.router)
app.include_router(admin.router)
app.include_router(rating.router)
app.include_router(codeforces.router)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)
