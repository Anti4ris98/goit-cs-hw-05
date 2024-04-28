import os
import asyncio
from aiopath import AsyncPath

async def sort_files(source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    files = os.listdir(source_dir)

    tasks = [asyncio.create_task(move_file(file, source_dir, destination_dir)) for file in files]

    await asyncio.gather(*tasks)

async def move_file(file, source_dir, destination_dir):
    _, ext = os.path.splitext(file)

    ext_dir = os.path.join(destination_dir, ext[1:])
    if not os.path.exists(ext_dir):
        os.makedirs(ext_dir)

    await AsyncPath(os.path.join(source_dir, file)).rename(os.path.join(ext_dir, file))

asyncio.run(sort_files('files', 'Folder'))
