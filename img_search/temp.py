from tqdm import tqdm
import os
import shutil


names = ['laptop']

for data in tqdm(names):
    for i in range(1,21):
        # old = f"dataset/{data}/{i}.jpg"
        # new = f"Data/{data}_{i}.jpg"
        # os.rename(old, new)
        shutil.move(f"dataset/{data}/{i}.jpg", f"Data/{data}_{i}.jpg")
