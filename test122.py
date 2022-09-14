import logging
import threading
import time
def thread_function():
  # Use threading.get_ident() to show the Thread ID
  logging.info("%d : Thread in action", threading.get_ident())
  time.sleep(2)
if __name__=="__main__" :
  # Set up the default handler
  logging.basicConfig(format="%(message)s ", level=logging.INFO)
  # Creating the threads
  logging.info("main : Creating the threads")
  t1= threading.Thread(target=thread_function)
  t2= threading.Thread(target=thread_function)
  # print(str(threading.get_ident())+"123")
  print(r'Temp_files/Screenshot[T:' + str(threading.get_ident()) + 'Fn:' + filename + '].jpg')
  # Run the threads
  logging.info("main : Calling the threads")
  t1.start()
  t2.start()
  logging.info("main  : Completed executing threads")