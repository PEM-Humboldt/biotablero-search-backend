from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "area_type" (
    "id" VARCHAR(50) NOT NULL  PRIMARY KEY,
    "label" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "collection" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "updated_at" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "metric" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "operation_type" VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "metric_collection" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_primary" BOOL NOT NULL,
    "collection_id" INT NOT NULL REFERENCES "collection" ("id") ON DELETE CASCADE,
    "metric_id" INT NOT NULL REFERENCES "metric" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "polygon" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "hash" VARCHAR(255)  UNIQUE,
    "geometry" JSONB NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "area" DOUBLE PRECISION NOT NULL,
    "official_code" VARCHAR(100)  UNIQUE,
    "area_type_id" VARCHAR(50) REFERENCES "area_type" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_polygon_hash_e7f306" ON "polygon" ("hash");
CREATE TABLE IF NOT EXISTS "polygon_metric" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "values" JSONB NOT NULL,
    "metric_id" INT NOT NULL REFERENCES "metric" ("id") ON DELETE CASCADE,
    "polygon_id" INT NOT NULL REFERENCES "polygon" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "polygon_metric_item" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "layer_url" VARCHAR(255) NOT NULL,
    "category" INT NOT NULL,
    "item_id" VARCHAR(100) NOT NULL,
    "metric_id" INT NOT NULL REFERENCES "metric" ("id") ON DELETE CASCADE,
    "polygon_id" INT NOT NULL REFERENCES "polygon" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_polygon_met_polygon_e8fb9d" UNIQUE ("polygon_id", "metric_id", "category", "item_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztW21v4jgQ/itRPnWl3qrlyu6Kb0CpllsKFaV3p62qyCQmWHXs1DHXRXv97yc7CXHeaM"
    "KlbbLNJ2AyE9sP45lnxslPfckNDwJmro3l/cc+g2CxdaHe037qBDjiS47GsaYD101eF2IO"
    "llgaAgaBwUPlpccZMLne01YAe/BY0y3omQy5HFGi9zSywVgIqelxhogdiTYEPWygwakN+R"
    "oyvafd3h1rOiIW/AG98Kd7b6wQxFZs7sgSY0u5P5Oepg/XgF1ITTHc0jAp3jgk0na3fE3J"
    "Tt3jTEhtSCADHFrKAsT8gsWGIn+uek/jbAN3k7QigQVXYIO5suCCKJiUCAQR4Z5cogN+GB"
    "gSm6/1ntY9efIXEy3V1xIr+LM/H37tz4+6Jx/0J6kHOPA1JXoRXBgsIS6D2M6gGtBCQYRa"
    "5CsvAVun2y2AW6fbFcAJJ1vdK7gJwRKY94+AWUbsSoSoS/HWpsRLgzoILC++zSEGch1pHG"
    "N778q/VwFgA197RVyfQs8IpcEsJGq0Q/NgS19yOk5SAgiw5azF2GKkGCxDijE0gwnnhC1F"
    "p0DgMuPatYlcY8JLBC7xJyRcJfCLN41bthjlt87p2eezL79/OvtyrOlyJjvJ5z1bcjxdPB"
    "PC5GeJCBbqNzHqn54UCfunJ0Hcj0DauJZYlAF4GqpzwCFHDsyGK26ZAM0KTD+GX+qZA/Zg"
    "thhfjq4X/csrMXPH8x6whKS/GIkrHSndJqRHnz4IOWXA9MPH7ibaX+PFV0381L7PpiOJGP"
    "W4zeSIkd7iuy7mBDacGoQ+GsBSlx2KQ9FhiciBnCGzkjx0KW8VD6m1/ZffIiP5AOVno+B6"
    "gUzkRJptFmqz0K+VhagrVoXC9ZaAK23ZzPqjFHQHhf2IyrahH8a8L6jMjAoTY1CgReG9od"
    "D4kBiIQ6d6XMYcOg3D5rUYQ5FKNmsHFmMRRlvWNpdQIM9wGXIA22ZsSEoxBCQHw5hhcpdS"
    "imu9F7PAGsxmk1h5Nhgv4gXY9OZyMJofncq6zHvAiEMV5azsaJRyzJTd8z5aD1ircdN0pi"
    "gDXszmPQGXInBJHNMgXlAGkU2+wa3Eckw8DoiZxXhzCsz6IZmXZY81nYHHXcqIuwklhgUx"
    "9PfxsH897J+P9JytXBmKTaW5SSRT0Sobzfxy4uX5T3i0kUt7lLOP59iOq6i+JMe51dfAW+"
    "t3LdepmOtIWEt0A0L9g3oAyaOy1+2dlDqAVMOdDakIkBls8I/r2TQbJ9Um2blHJtf+1TDy"
    "app/96AkFhzjg9MQt8v+34nW/HQ4mQ2SfXhxg0EC37dt4NX6HFyFSTzikZFvMQU5YS40SO"
    "C0Ehb1RGoPMOezm8FkpF3NR8Px9Tjwwt3xkLwYr0Dmo/4k2QRdrZCJADZMapXrgSYNGxj+"
    "Dm4d7x4tyiw98kFL2lWC2Wvv1hIP++wpOWJPZ1XCl9Vnw2oHYVGynPSQGFe+Hi206c1kso"
    "8sv8iRa9tZbjvL/6uyeu5IOuVgBassoz2hbmaR9Q/AG5ixB/PLh8iiLR72Fw9tV/TAdnIY"
    "VEohFzd6T9DtYXdKE6wSblf82eMapdckt4t7yvM95bYrf0hXvgZ9ZIUPFmM8IXUsx3okj6"
    "2e+tyquzfyQRNwaFO/fScGFn/CXUuTXpYmYbCFzNiwkm/FKEbvrCOoemnR03TF5D2lbxW2"
    "cEOXeVstMmmmjx3c/Wv5dcuvW35dP3LY8utfnV/3IUPmes/r4f71Ii+HR5pt37BmcW9v3x"
    "AyL/Mhq3yiopg0k6gcfjzuuqVOJ331ZoJ0MJszKeGQZLyJmt+KVkzaXnS6F13iTaHqU8bT"
    "f7Z6QDM="
)
