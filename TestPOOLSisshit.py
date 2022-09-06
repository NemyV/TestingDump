import multiprocessing
import os
import signal
import time

work = (["A", 5], ["B", 2], ["C", 7],
        ["D", 11], ["E", 12], ["F", 20])

manager = multiprocessing.Manager()
process_dict = manager.dict()

Skillsdict = {'s': 4,
              'q': 5,
              'e': 6,
              'f': 7,
              'd': 3,
              'r': 11}


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def skills(key):
    # minutes = 5
    # numbofskills = round(minutes * 60 / Skillsdict[key])
    print("child: %s" % os.getpid())
    print("SKILLS COOLDOWN", Skillsdict[key])
    for i in range(0, 2, 1):
        # time.sleep(0.4)
        print(key)
        time.sleep(Skillsdict[key])


def work_log(work_data):
    print("child: %s" % os.getpid())
    ## ATtempt at appending PID to dictionary PID : PID
    process_dict[os.getpid()] = os.getpid()
    print(process_dict)
    print(" Process %s waiting %s seconds" % (work_data[0], work_data[1]))
    time.sleep(int(work_data[1]))
    print(" Process %s Finished." % work_data[0])


def reset( *args):

    time.sleep(1)
    # mainx.run("self")
    normal_processes = np
    combat_processes = cp
    # mainx.np = self.normal_processes
    # mainx.cp = self.combat_processes
    print("killing normal :", normal_processes)
    for process in normal_processes:
        process.terminate()
        process.join()
    time.sleep(1)
    print("killing combat :", combat_processes)
    for process in combat_processes:
        process.terminate()
        process.join()


def statecheck():
    # print("i was here")
    print("doing some sheesh")
    reset()
    time.sleep(10)
    skills()
    time.sleep(20)


def main():
    pool = multiprocessing.Pool(6, init_worker)

    try:
        results = []
        print("Starting jobs")
        for x in work:
            results.append(pool.apply_async(work_log, args=(x,)))

        for key in Skillsdict:
            results.append(pool.apply_async(skills, args=(key,)))

        # process = process_dict.pop(pid)
        # process.terminate()

        #time.sleep(2)
        pool.close()
        # pool.join()
        print([x.get() for x in results])
    except KeyboardInterrupt:
        global process_dict
        print("Caught KeyboardInterrupt, terminating workers")
        print(process_dict)
        pool.terminate()
        pool.join()


if __name__ == "__main__":
    main()