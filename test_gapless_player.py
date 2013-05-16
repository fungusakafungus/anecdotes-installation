import gapless_player
import time
import random
import itertools
vs = ["videos/P3_stefan.mov", "videos/P4_lumen.mov"]
vs = itertools.cycle(vs)
try:
    for v in vs:
        gapless_player.play(v)
        s = 1 + random.expovariate(0.3)
        print "sleeping ", s
        time.sleep(s)
finally:
    gapless_player.quit()
