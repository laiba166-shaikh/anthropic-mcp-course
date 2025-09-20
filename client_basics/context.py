from contextlib import asynccontextmanager, AsyncExitStack
import asyncio

# 1ST Approcah: contextmanager decorator
# @asynccontextmanager
# async def makeconnection(name: str):
#     print(f'Connecting... {name}')
#     yield name
#     print(f'Connected {name}')


# async def main():
#     async with makeconnection('Learning') as c:
#         print(f'Using Connection... {c}')

    
# asyncio.run(main())

# output:
# Connecting... Learning
# Using Connection... Learning
# Connected Learning
    

# =====================================================
# 2ND Approach

async def get_connection(name):
    class Ctx():
        async def __aenter__(self):
            print(f'ENTER: {name}')
            return name
        
        async def __aexit__(self, a, b, c):
            print(f'EXIT: {name}')
            return name
    return Ctx()

async def main():
    async with await get_connection('A') as a:
        print(f"Using connection {a}")
        async with await get_connection('B') as b:
            print(f"Using connection {b}")

async def main1():
    async with await get_connection('A') as a:
        async with await get_connection('B') as b:
            print(f"Using connection {a} and {b}")

# We cant write nested async with block 

# Output main()
# ENTER: A
# Using connection A
# ENTER: B
# Using connection B
# EXIT: B
# EXIT: A

# Output main1()
# ENTER: A
# ENTER: B
# Using connection A and B
# EXIT: B
# EXIT: A


# asyncio.run(main())
# asyncio.run(main1())

# =====================================================
# 3RD Approach
async def main3():
    async with AsyncExitStack() as stack:
        a = await stack.enter_async_context(await get_connection('A'))
        b = await stack.enter_async_context(await get_connection('B'))
        print(f"Using Connection {a} and {b}")

# Output main3
# ENTER: A
# ENTER: B
# Using Connection A and B
# EXIT: B
# EXIT: A
# asyncio.run(main3())

async def main4():
    async with AsyncExitStack() as stack:
        a = await stack.enter_async_context(await get_connection('A'))
        if a == 'A':
            b = await stack.enter_async_context(await get_connection('B'))
            print(f"Using Connection {a} and {b}")

        async def customCleanup():
            print('Clean up function callled')

        stack.push_async_callback(customCleanup)
        print(f'Doing work with {a} and maybe {locals().get('b')}')
        await asyncio.sleep(2)

asyncio.run(main4())

# Output main4
# ENTER: A
# ENTER: B
# Using Connection A and B
# Doing work with A and maybe B
# Clean up function callled
# EXIT: B
# EXIT: A

    