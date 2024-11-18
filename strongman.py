import asyncio

async def start_strongman(name, power):  # аснхронная функция выступления силача
    print(f'Силач {name} начал соревнование')
    for i in range(1, 6):
        await asyncio.sleep(1/power)
        print(f'Силач {name} поднял шар {str(i)}')
    print(f'Силач {name} закончил соревнование')

async def start_tournament():  # асинхронная функция соревнований силачей
    tasc1 = asyncio.create_task(start_strongman('Олег', 10))
    tasc2 = asyncio.create_task(start_strongman('Саша', 5))
    tasc3 = asyncio.create_task(start_strongman('Андрей', 20))
    await tasc1
    await tasc2
    await tasc3

asyncio.run(start_tournament())  # запуск функции соревнований