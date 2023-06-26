import asyncio
import asyncpg
from string import ascii_lowercase
from random import sample, randint
from datetime import datetime


CREATE_BRAND_TABLE = (
    'CREATE TABLE IF NOT EXISTS brand('
        'id SERIAL PRIMARY KEY,'
        'name TEXT NOT NULL'
    ');'
)

CREATE_PRODUCT_TABLE = (
    'CREATE TABLE IF NOT EXISTS product('
        'id SERIAL PRIMARY KEY,'
        'name TEXT NOT NULL,'
        'brand_id INT NOT NULL,'

        'FOREIGN KEY (brand_id) REFERENCES brand(id)'
    ');'
)

CREATE_PRODUCT_COLOR_TABLE = (
    'CREATE TABLE IF NOT EXISTS product_color('
        'id SERIAL PRIMARY KEY,'
        'name TEXT NOT NULL'
    ');'
)

CREATE_PRODUCT_SIZE_TABLE = (
    'CREATE TABLE IF NOT EXISTS product_size('
        'id SERIAL PRIMARY KEY,'
        'name TEXT NOT NULL'
    ');'
)

CREATE_PRODUCT_SIZE_TABLE = (
    'CREATE TABLE IF NOT EXISTS product_size('
        'id SERIAL PRIMARY KEY,'
        'name TEXT NOT NULL'
    ');'
)

CREATE_SKU_TABLE = (
    'CREATE TABLE IF NOT EXISTS sku('
        'id SERIAL PRIMARY KEY,'
        'product_id INT NOT NULL,'
        'product_size_id INT NOT NULL,'
        'product_color_id INT NOT NULL,'

        'FOREIGN KEY (product_id) REFERENCES product(id),'
        'FOREIGN KEY (product_size_id) REFERENCES product_size(id),'
        'FOREIGN KEY (product_color_id) REFERENCES product_color(id)'
    ');'
)



select_query = (
    'select '
        's.id,'
        'p.name,'
        'pc.name,'
        'ps.name '
    'from sku s '
    'join product p on s.product_id = p.id '
    'join product_color pc on s.product_color_id = pc.id '
    'join product_size ps on s.product_size_id = ps.id '
    'where p.id = 100 '
)


async def query_product(pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow(select_query)


async def main():
    connection = await asyncpg.connect(
        host='localhost',
        port=5432,
        user='mrtedn',
        database='products',
        password='123',
    )

    d1 = datetime.now()

    cnt = 0
    async with connection.transaction():
        async for sku in connection.cursor('select * from sku', prefetch=100_000):
            a = sku['product_id']
            cnt += 1


    d2 = datetime.now()
    print((d2-d1).total_seconds())
    print(f'cnt: {cnt / 1000}')

    await connection.close()

if __name__ == '__main__':
    asyncio.run(main())

