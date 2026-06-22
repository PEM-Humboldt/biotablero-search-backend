import hashlib
from contextlib import asynccontextmanager
from tortoise.transactions import in_transaction


def build_advisory_lock_key(*parts: str) -> int:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], byteorder="big", signed=True)


async def acquire_advisory_xact_lock(connection, *parts: str) -> None:
    lock_key = build_advisory_lock_key(*parts)
    await connection.execute_query("SET LOCAL lock_timeout = '30s';")
    await connection.execute_query(
        f"SELECT pg_advisory_xact_lock({lock_key});"
    )


@asynccontextmanager
async def advisory_xact_lock(*parts: str):
    async with in_transaction() as connection:
        await acquire_advisory_xact_lock(connection, *parts)
        yield connection
