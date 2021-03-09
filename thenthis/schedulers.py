from datetime import time
import whendo.core.util as util
import whendo.core.scheduler as sched_x

schedulers["often"] = sched_x.Timely(interval=1)
morning, evening = time(6,0,0), time(18,0,0)
schedulers["daily_often"] = sched_x.Timely(start=morning, stop=evening, interval=1)
schedulers["nightly_often"] = sched_x.Timely(start=evening, stop=morning, interval=1)
schedulers["randomly_often"] = sched_x.Randomly(time_unit=util.TimeUnit.second, low=2, high=5)
schedulers["timely_at_00_sec"] = sched_x.Timely(interval=1, second=00)
schedulers["timely_at_30_sec"] = sched_x.Timely(interval=1, second=30)
schedulers["timely_at_10_sec"] = sched_x.Timely(interval=1, second=10)
schedulers["timely_every_10"] = sched_x.Timely(interval=10)
schedulers["timely_every_30"] = sched_x.Timely(interval=30)
schedulers["immediately"] = sched_x.Immediately()