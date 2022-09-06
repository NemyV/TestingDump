import time
import pydirectinput

Resolution = [2560, 1080]
playerMinimap = [Resolution[0] / 100 * 93.04,
                 Resolution[1] / 100 * 15.46]

MiniMCOORD = [Resolution[0] / 100 * 87.25,
              Resolution[1] / 100 * 4.17]
MiniMCOORDx = [Resolution[0] / 100 * 98.7,
              Resolution[1] / 100 * 27]
panchor = [round(Resolution[0] / 2),
           round(Resolution[1] / 2)]
movementarray = []
movementarray.append(Resolution)
movementarray.append(playerMinimap)
movementarray.append(MiniMCOORD)
movementarray.append(MiniMCOORDx)
movementarray.append(panchor)
print(MiniMCOORD)
for x in movementarray:
    print(x)
    pydirectinput.moveTo(round(x[0]), round(x[1]))
    time.sleep(0.5)