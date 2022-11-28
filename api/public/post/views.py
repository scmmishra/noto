from fastapi import APIRouter, Depends, Query
from typing import List
from sqlmodel import Session

from database import get_session
from api.public.post.crud import (
    create_post,
    delete_post,
    read_post,
    read_posts,
    update_post,
)
from api.public.post.models import (
    ChangelogPostCreate,
    ChangelogPostRead,
    ChangelogPostUpdate,
)

router = APIRouter()


@router.post("", response_model=ChangelogPostRead)
def create_a_post(post: ChangelogPostCreate, db: Session = Depends(get_session)):
    """Create a team."""
    return create_post(post=post, db=db)


@router.get("", response_model=List[ChangelogPostRead])
def get_posts(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    """Get all teams."""
    return read_posts(offset=offset, limit=limit, db=db)


@router.patch("/{team_id}/{post_slug}", response_model=ChangelogPostRead)
def update_a_post(
    team_id: int,
    post_slug: str,
    post: ChangelogPostUpdate,
    db: Session = Depends(get_session),
):
    """Update a team."""
    return update_post(slug=post_slug, team=team_id, post=post, db=db)


@router.get("/{team_id}/{post_slug}", response_model=ChangelogPostRead)
def get_a_post(team_id: int, post_slug: str, db: Session = Depends(get_session)):
    """Get a team by id."""
    return read_post(slug=post_slug, team=team_id, db=db)


@router.delete("/{team_id}/{post_slug}")
def delete_a_post(team_id: int, post_slug: str, db: Session = Depends(get_session)):
    """Delete a team by id."""
    return delete_post(slug=post_slug, team=team_id, db=db)
