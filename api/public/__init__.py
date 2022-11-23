from fastapi import APIRouter

from api.public.team import views as teams

api = APIRouter()

api.include_router(teams.router, prefix="/teams", tags=["Teams"])
