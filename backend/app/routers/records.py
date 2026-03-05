"""
Records router — all CRUD endpoints for health records.
Business logic lives here; DB access goes through the db context manager.
"""

from fastapi import APIRouter, HTTPException, status
from app.db import get_db
from app.models import RecordCreate, RecordUpdate, RecordResponse

router = APIRouter(prefix="/records", tags=["records"])


def _row_or_404(conn, record_id: int) -> dict:
    """Fetch a record by id or raise 404."""
    row = conn.execute(
        "SELECT * FROM records WHERE id = ?", (record_id,)
    ).fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record {record_id} not found",
        )
    return dict(row)


@router.get("/", response_model=list[RecordResponse], summary="List all records")
def list_records():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM records ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


@router.get("/{record_id}", response_model=RecordResponse, summary="Get a single record")
def get_record(record_id: int):
    with get_db() as conn:
        return _row_or_404(conn, record_id)


@router.post(
    "/",
    response_model=RecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new record",
)
def create_record(payload: RecordCreate):
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO records (firstname, lastname, age, sex, health)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload.firstname,
                payload.lastname,
                payload.age,
                payload.sex,
                payload.health,
            ),
        )
        new_id = cursor.lastrowid
        return dict(conn.execute(
            "SELECT * FROM records WHERE id = ?", (new_id,)
        ).fetchone())


@router.put("/{record_id}", response_model=RecordResponse, summary="Update a record")
def update_record(record_id: int, payload: RecordUpdate):
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}

    with get_db() as conn:
        _row_or_404(conn, record_id)

        set_clause = ", ".join(f"{col} = ?" for col in updates)
        values = list(updates.values()) + [record_id]
        conn.execute(
            f"UPDATE records SET {set_clause} WHERE id = ?", values
        )
        return dict(conn.execute(
            "SELECT * FROM records WHERE id = ?", (record_id,)
        ).fetchone())


@router.delete(
    "/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a record",
)
def delete_record(record_id: int):
    with get_db() as conn:
        _row_or_404(conn, record_id)
        conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
