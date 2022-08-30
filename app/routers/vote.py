from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.oauth2 import get_current_user

from .. import schemas, models
from ..database import get_db

router = APIRouter(
    prefix='/vote',
    tags=['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(get_db), user: schemas.UserResponse = Depends(get_current_user)):

    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {vote.post_id} does not exit')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==user.id)

    vote_found = vote_query.first()

    if vote_found:
        # check if current user already voted
        if vote.dir == schemas.VoteDir.upvote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="vote already registerd")
        else:
            vote_query.delete()
            db.commit()
            return {"message": "vote deleted successfully"}
    else:
        new_vote = models.Vote(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added successfully"}
