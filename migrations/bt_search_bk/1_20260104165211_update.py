from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygon" ALTER COLUMN "geometry" TYPE JSONB USING "geometry"::JSONB;
        ALTER TABLE "polygon_metric" ALTER COLUMN "values" TYPE JSONB USING "values"::JSONB;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_polygon_59bbb7" ON "polygon_metric" ("polygon_id", "metric_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_polygon_met_polygon_59bbb7";
        ALTER TABLE "polygon" ALTER COLUMN "geometry" TYPE JSONB USING "geometry"::JSONB;
        ALTER TABLE "polygon_metric" ALTER COLUMN "values" TYPE JSONB USING "values"::JSONB;"""


MODELS_STATE = (
    "eJztW21zmzgQ/isePrUzvU7qS9rOfcOOM/XVsTO2c+00k2FkkDETIVGQm3o6+e+VBBjxZo"
    "OLHbjwKfFqF6SH1e6zK/ilLKjmQeDqK23x8FZ1IZhvHKj80/mlYGDzf3I03nQU4DjJcS6m"
    "YIGEIWC6Gg2VFx51gU7ZwBIgDzKRAT3dtRxqEcykeI0QFxKdKVrYjERrbH1fQ40SE9IVdN"
    "nA3T0TW9iAP6EX/nQetKUFkRGbu2Xwewu5PxMm66+AeyU0+e0Wmk7Q2saRtrOhK4K36mw2"
    "XGpCDF1AoSEtgM8vWGwo8ufKBNRdw+0kjUhgwCVYIyotuCAKOsEcQQtTTyzRBj81BLFJV+"
    "znxdmTv5hoqb4WX8F/6rT/SZ2+ujh7rTwJPUCBrynQi+Biq4GoDGJbg2pACwURapGvHAO2"
    "7sVFAdyYFgeOO9nyQcKNCxZAf3gErqHFRiJEHYI2JptCGtReYHn1eQoREOtI4xjbezf+tQ"
    "oAG/jaCXF9Cj0jlAazEKiRLsmDLT1kd+2kBGBgilnze/M7xWDpE4SgHkw4J2xJOgUClx7X"
    "rk3kGmJaInDxh5BwlcAvnjVumfwuf3XfnX84//j3+/OPTEXMZCv5sGNLDsfzPSFM/C0RwU"
    "L9Jkb9d2dFwj7T8uN+BNLaMfiiNEDTUF2yEWrZMBuuuGUCNCMwfRv+U88csAOz+fB6MJur"
    "1zd85rbnfUcCEnU+4CNdId0kpK/ev+ZywmKEHz62F+l8Gc4/dfjPzrfJeCAQIx41XXHHSG"
    "/+TeFzAmtKNEweNWDIyw7FoeiwRGRDBopeSR66FpeKh9TaPuXnyEg+QPnZKBgvkInsSLPN"
    "Qm0W+n9lIeLwVVnhekvAlbZsZv1RCrqDwn5EZdvQD2PeF1RmWoWJMSjQovDeUGh8SDSLQr"
    "t6XIbsqg3D5lSMoUglm7UDi7EIrS1rm0soLE9zXMsG7iZjQxKCIMA5GMYMk7uUWdZ6L2aB"
    "1ZtMRrHyrDecxwuw8e11b8DypqjLmBILZDLKWdlRK+WYKbv9PloPWKtx03SmKANezOYlAZ"
    "cicEkc0yBeERdaJv4MNwLLIZsTwHoW480pMOuHZF6WZWIXPG5TRtxN2EINiKC/j/vqrK9e"
    "DpScrVwZik2luUkkU9EqG838cuL4/Cc82silPdLZxz6240iqx+Q4d8oKeCvlvuU6FXMdAW"
    "sKufxuQKh/UA8geVR22t5JqQNIOdyZkPAAmcEG/51Nxtk4yTYJrG4xW8adYen0TQdZHr2v"
    "dcTLwoovO8YKxyF61+rXRIN+3B9NesluPL9AL4Hy87bxan0aLsPEX/TIyLqIgJxgFxokcF"
    "pyi3oitQOYy8ltbzTo3EwH/eFsGHjh9pBIDMbrkOlAHSVboculpVsAMYyMcp3QpGEDg+DB"
    "DeTtC0aZBUg+aEm7SjA79W4t8crPjsIj9o5WJaxZfkOsdhAWpcxJD4kx5tlg3hnfjka7KP"
    "NRDl7b/nLbX/6j+mrfwXTKwQrWWtqxzqnv5GouuMl922s+bv31A6A1zNiY+ZVFZNHWFUXq"
    "irZtemC/OYw3pZCLG70k6HYQPymuVkL7ir+cXKPMm6R9cU/Z33Ru2/aHtO1r0GiWqGIxMh"
    "SyynKESFDc07Ai/sSYw5jE7+/xG/OH0JKlI5MlBDbQ1dZuyc9mJKMX1iyUvbTocbtk8pLS"
    "twxbuKFLeJlk0kwfO7gx2PLrll+3/Lp+5LDl138MYc35tQrZ7FZK/vfj/ngBJg0izfZN1Z"
    "rFvV2E+Ad0vcy3sPKJimTSTKJy+Mk52wQlgArUmwnSwWyOXZVCnPGpan5DWjJpO9J5HekS"
    "HxRVnziefgO89U4+"
)
