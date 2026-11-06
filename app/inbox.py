from sqlalchemy.dialects.postgresql import insert

from app.models import InboxEvent


async def register_event(
    session,
    event_id,
    event_type,
) -> bool:
    statement = (
        insert(InboxEvent)
        .values(
            event_id=event_id,
            event_type=event_type,
        )
        .on_conflict_do_nothing(
            index_elements=["event_id"]
        )
        .returning(InboxEvent.event_id)
    )

    result = await session.execute(statement)

    return result.scalar_one_or_none() is not None