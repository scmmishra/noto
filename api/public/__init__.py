from fastapi import APIRouter

from api.public.team import views as teams
from api.public.post import views as posts

api = APIRouter()

api.include_router(teams.router, prefix="/teams", tags=["Teams"])
api.include_router(posts.router, prefix="/posts", tags=["Posts"])
