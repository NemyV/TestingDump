import threading
import time
import pydirectinput

dictionary = {'key1': 5,
              'key2': 16,
              'key3': 8}
threads = []


def start():
    for key in dictionary:
        key = key
        print("Outer loop ", key)

        def infiniteloop1(key=key):
            while True:
                print('Inner Loop', key)
                time.sleep(5)

        thread = threading.Thread(target=infiniteloop1)
        threads.append(thread)
    for threadx in threads:
        print("startin threads", thread)
        threadx.start()
    for thread in threads:
        print("joining ", thread)
        thread.join()

thread1 = threading.Thread(target=start)
thread1.start()

# def infiniteloop1():
#     while True:
#         print('Loop 1')
#         time.sleep(16)
#
# def infiniteloop2():
#     while True:
#         print('Loop 2')
#         time.sleep(5)
#
# def infiniteloop3():
#     while True:
#         print('Loop 3')
#         time.sleep(6)


# thread1 = threading.Thread(target=infiniteloop1)
# thread1.start()
#
# thread2 = threading.Thread(target=infiniteloop2)
# thread2.start()
#
# thread2 = threading.Thread(target=infiniteloop3)
# thread2.start()
