import time
import asyncio

# def get_data_from_database(query: str):
#     print(f'Получен запрос {query}')
#     if query == 'Анапа':
#         time.sleep(4)
#     elif query == 'Москва':
#         time.sleep(2)
#     print(f'Получены ответ {query}')
#
# get_data_from_database('Анапа')
# get_data_from_database('Москва')


async def get_data_from_database_async(query: str):
    print(f'Получен запрос {query}')
    if query == 'Анапа':
        await asyncio.sleep(4)
    elif query == 'Москва':
        await asyncio.sleep(2)
    print(f'Получены ответ {query}')
    print('Results')

async def main():
    await asyncio.gather(
        get_data_from_database_async('Анапа'),
        get_data_from_database_async('Москва'),
    )

asyncio.run(main())