from fastapi import APIRouter, Depends, status, HTTPException
from app.database import get_db
from app.schemas.notes import NoteResponse, NoteCreate, NoteUpdate
from sqlalchemy.orm import Session
from app.models.notes import Note
from app.core.dependencies import get_current_user

notes_router = APIRouter(
    prefix='/notes',
    tags=['Notes']
)

@notes_router.get(
    "/",
    response_model=list[NoteResponse]
)
def get_notes(
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    notes = (
        db.query(Note)
        .filter(
            Note.user_id == current_user.id
        )
        .all()
    )
    return notes

@notes_router.get(
    "/{note_id}",
    response_model=NoteResponse
)
def get_note(
    note_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note introuvable"
        )

    return note

@notes_router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED
)
def create_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    note = Note(
        **note_data.model_dump(),
        user_id=current_user.id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@notes_router.patch(
    "/{note_id}",
    response_model=NoteResponse
)
def patch_note(
    note_id: int,
    note_update: NoteUpdate,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note introuvable"
        )

    update_data = note_update.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)
    return note


@notes_router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_note(
    note_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note introuvable"
        )
    db.delete(note)
    db.commit()
    
@notes_router.patch(
    "/{note_id}/pin",
    response_model=NoteResponse
)
def toggle_pin_note(
    note_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note introuvable"
        )

    note.is_pinned = not note.is_pinned

    db.commit()
    db.refresh(note)
    return note
    
    

