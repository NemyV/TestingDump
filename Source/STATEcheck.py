from METHODS_OLD_BACKUP import searchimageinarea
import threading
import time
Resolution = [2560, 1080]
MiniMCOORD = [Resolution[0] / 100 * 86,
              Resolution[1] / 100 * 4.17,
              Resolution[0] / 100 * 98.7,
              Resolution[1] / 100 * 30.28]

earchfor = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\RedEnem123y.png"
portal = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\PORTAL.png"
elite = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\ELITE123.png"
boss = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Boss432.png"
tower = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\TOWE123R.png"

NumberofTrackers = 4

TrackEnemy = 0
TrackPortal = 0
TrackElite = 0
TrackBoss = 0

#RedTest.png
def debugging():
    r_thread = threading.Thread(target=lambda: searchimageinarea(earchfor, "Enemy",
                                                                 MiniMCOORD[0],
                                                                 MiniMCOORD[1],
                                                                 MiniMCOORD[2],
                                                                 MiniMCOORD[3], count=True, precision=0.70))
    r_thread.daemon = True
    r_thread.start()

    p_thread = threading.Thread(target=lambda: searchimageinarea(portal, "Portal",
                                                                 MiniMCOORD[0],
                                                                 MiniMCOORD[1],
                                                                 MiniMCOORD[2],
                                                                 MiniMCOORD[3], count=True))
    p_thread.daemon = True
    p_thread.start()

    e_thread = threading.Thread(target=lambda: searchimageinarea(elite, "Elite",
                                                                 MiniMCOORD[0],MiniMCOORD[1],
                                                                 MiniMCOORD[2],MiniMCOORD[3],
                                                                 count=True, precision=0.6))
    e_thread.daemon = True
    e_thread.start()

    b_thread = threading.Thread(target=lambda: searchimageinarea(boss, "Boss",
                                                                 MiniMCOORD[0], MiniMCOORD[1],
                                                                 MiniMCOORD[2], MiniMCOORD[3],
                                                                 count=True, precision=0.7))
    b_thread.daemon = True
    b_thread.start()

    t_thread = threading.Thread(target=lambda: searchimageinarea(tower, "Tower",
                                                                 MiniMCOORD[0], MiniMCOORD[1],
                                                                 MiniMCOORD[2], MiniMCOORD[3],
                                                                 count=True, precision=0.7))
    t_thread.daemon = True
    t_thread.start()

    # waiting for both threadings to be completed
    e_thread.join()
    p_thread.join()
    e_thread.join()
    b_thread.join()
    t_thread.join()
