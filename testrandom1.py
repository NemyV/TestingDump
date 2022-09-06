import os
import multiprocessing

tld = [os.path.join("/", f) for f in os.walk("/").next()[1]]
manager = multiprocessing.Manager()

files = manager.list()
def get_files(x):
    for root, dir, file in os.walk(x):
        for name in file:
            files.append(os.path.join(root, name))

pool = multiprocessing.Pool(processes=len(tld)) # Instantiate the pool here

pool.map(get_files, [x for x in tld])
pool.close()
pool.join()
print (len(files))
