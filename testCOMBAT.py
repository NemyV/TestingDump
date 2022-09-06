import time
from multiprocessing import Manager, Process
from multiprocessing.managers import NamespaceProxy, BaseManager
import multiprocessing
import inspect

data_dict = {'y': 4,
             'h': 5,
             'j': 6,
             'o': 7,
             'p': 3,
             'b': 11}


def combat():
    print("i am in combat")
    for i in range(0, 10, 1):
        print("key")
        time.sleep(2)
        # time.sleep(data_dict[key])


def move():
    print("Starting move2obj")
    for i in range(0, 5, 1):
        print(i)


def reset(normal_processes, combat_processes):
    print("killing normal :", normal_processes)
    for process in normal_processes:
        process.terminate()
        process.join()
    time.sleep(1)
    print("killing combat :", combat_processes)
    for process in combat_processes:
        process.terminate()
        process.join()


def statecheck(np, cp, switch):
    while True:
        if 'On' in switch:
            time.sleep(2)
            print("still alive switch is:", switch)
        else:
            print("statecheck RESTARTING ")
            time.sleep(2)
            reset(np, cp)
            time.sleep(5)
            switch.append("On")
            print("APPENDING ON   ", switch)


class ObjProxy(NamespaceProxy):
    """Returns a proxy instance for any user defined data-type. The proxy instance will have the namespace and
    functions of the data-type (except private/protected callables/attributes). Furthermore, the proxy will be
    pickable and can its state can be shared among different processes. """

    @classmethod
    def populate_obj_attributes(cls, real_cls):
        DISALLOWED = set(dir(cls))
        ALLOWED = ['__sizeof__', '__eq__', '__ne__', '__le__', '__repr__', '__dict__', '__lt__',
                   '__gt__']
        DISALLOWED.add('__class__')
        new_dict = {}
        for (attr, value) in inspect.getmembers(real_cls, callable):
            if attr not in DISALLOWED or attr in ALLOWED:
                new_dict[attr] = cls._proxy_wrap(attr)
        return new_dict

    @staticmethod
    def _proxy_wrap(attr):
        """ This method creates function that calls the proxified object's method."""

        def f(self, *args, **kwargs):
            return self._callmethod(attr, args, kwargs)

        return f


attributes = ObjProxy.populate_obj_attributes(Process)
ProcessProxy = type("ProcessProxy", (ObjProxy,), attributes)

def a():
    time.sleep(4)
    print('done')


if __name__ == "__main__":
    listmanager = Manager()
    normal_processes = listmanager.list()
    combat_processes = listmanager.list()
    all_processes = listmanager.list()
    switch = listmanager.list()

    BaseManager.register('Process', Process, ProcessProxy, exposed=tuple(dir(ProcessProxy)))
    manager = BaseManager()
    manager.start()

    proc_state_check = manager.Process(target=statecheck,
                                       args=(normal_processes, combat_processes, switch))
    proc_move = manager.Process(target=move)

    all_processes.append(proc_state_check)
    combat_processes.append(proc_move)

    proc_state_check.start()
    proc_move.start()

    # proc_state_check.join()
    # proc_move.join()

    while True:
        print("Switch is :", switch)
        time.sleep(3)
        if 'On' in switch:
            print("SWITCH IS", switch, "RESTARTING COMBAT", normal_processes)
            proc_combat = manager.Process(target=combat)
            combat_processes.append(proc_combat)
            proc_combat.start()
            switch[:] = []
            proc_combat.join()
