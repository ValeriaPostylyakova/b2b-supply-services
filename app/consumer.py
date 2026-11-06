import asyncio
import json
import uuid

import aio_pika

from app.core.config import settings
from app.core.database import async_session_maker
from app.inbox import register_event


async def handle_order_created(session, event):
    """
    Здесь размещается бизнес-логика Notification Service.

    Например:
    - получить данные заказа;
    - подготовить уведомление;
    - создать запись уведомления в своей БД.

    Внешнюю отправку email лучше вынести в отдельный
    надёжный процесс, а не выполнять внутри транзакции.
    """
    print("Creating notification for order:", event["order_id"])


async def process_message(message):
    event_id = uuid.UUID(message.message_id)
    event_type = message.type

    event = json.loads(message.body.decode("utf-8"))

    async with async_session_maker() as session:
        async with session.begin():
            is_new = await register_event(
                session,
                event_id,
                event_type,
            )

            if not is_new:
                print("Duplicate event skipped:", event_id)
            elif event_type == "order.created":
                await handle_order_created(session, event)
            else:
                print("Unsupported event:", event_type)

    await message.ack()


async def main():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        exchange = await channel.declare_exchange(
             settings.EXCHANGE_NAME,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        queue = await channel.declare_queue(
           settings.QUEUE_NAME,
            durable=True,
        )

        await queue.bind(exchange, routing_key="order.#")

        print("Notification Service started")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                try:
                    await process_message(message)

                except Exception as exc:
                    print("Consumer error:", exc)
                    if not message.processed:
                        await message.reject(requeue=False)


if __name__ == "__main__":
    asyncio.run(main())