import thenthis.actions as act
import thenthis.schedulers as sch


class Program(BaseModel):
    """
    A Program encapsulates a start time, stop time, and actions being scheduled to execute
    during this period of time.
    """
    start:datetime
    stop:datetime

    def initialize(self):
        pass

    def schedule_actions(self, start:datetime, stop:datetime):
        pass

    def pause_actions(self):
        pass

    def resume_actions(self):
        pass

    def unschedule_actions(self):
        pass

class StandardProgram(Program):
    """
    A StandardProgram is a Program commonly run on pivots.
    """
    def initialize(self, client:Client):
        for action_name in ["red_on", "gpio_clear", "start_pivot"]:
            client.add_action(action_name, act.actions)
        for scheduler_name in ["immediately", "heartbeat"]:
            client.add_scheduler(scheduler_name, sch.schedulers)

    def schedule_actions(self, client, start:datetime, stop:datetime):
        delta_20 = timedelta(seconds=20)
        dt1 = start + timedelta(seconds=10)
        dt2 = stop + timedelta(minutes=3)
        dt1_plus = dt1 + delta_20
        dt2_minus = dt2 - delta_20
        client.defer_action("immediately", "start_pivot", util.DateTime(date_time=dt1))
        client.defer_action("heartbeat", "red_on", util.DateTime(date_time=dt1_plus))
        client.expire_action("heartbeat", "red_on", util.DateTime(date_time=dt2_minus))
        client.defer_action("immediately", "gpio_clear", util.DateTime(date_time=dt2))
    
    def pause_actions(self, client:Client):
        client.stop_jobs()
        client.execute_action("gpio_clear")
    
    def resume_actions(self, client:Client):
        client.run_jobs()

    def unschedule_actions(self, client:Client):
        client.unschedule_scheduler_action("heartbeat", "red_on")
        client.unschedule_scheduler_action("immediately", "gpio_clear")
        client.execute_action("gpio_clear")
