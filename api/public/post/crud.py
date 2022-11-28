from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime
from database import get_session
from api.public.post.models import (
    ChangelogPost,
    ChangelogPostCreate,
    ChangelogPostUpdate,
)


def create_post(post: ChangelogPostCreate, db: Session = Depends(get_session)):
    """Create a new changelog entry"""
    post_to_create = ChangelogPost.from_orm(post)

    post_to_create.created_on = datetime.now()
    post_to_create.updated_on = datetime.now()

    db.add(post_to_create)
    db.commit()
    db.refresh(post_to_create)

    return post_to_create


def read_posts(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    """Read all posts"""
    posts = db.exec(select(ChangelogPost).offset(offset).limit(limit)).all()
    return posts


def read_post(slug: str, team: int, db: Session = Depends(get_session)):
    """Read a post by slug and team id"""
    query = (
        select(ChangelogPost)
        .where(ChangelogPost.slug == slug)
        .where(ChangelogPost.for_team_id == team)
    )

    post = db.exec(query).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with slug {slug} in team {team}",
        )

    return post


def update_post(
    slug: str, team: int, post: ChangelogPostUpdate, db: Session = Depends(get_session)
):
    """Update a team by slug and team id"""
    post_to_update = read_post(slug, team, db)

    post_data = post.dict(exclude_unset=True)

    for key, value in post_data.items():
        setattr(post_to_update, key, value)

    post_to_update.updated_on = datetime.now()

    db.add(post_to_update)
    db.commit()
    db.refresh(post_to_update)

    return post_to_update


def delete_post(slug: str, team: int, db: Session = Depends(get_session)):
    """Delete a post by slug and team id"""
    post_to_delete = read_post(slug, team, db)

    db.delete(post_to_delete)
    db.commit()

    return {"ok": True}
