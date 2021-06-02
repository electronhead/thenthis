from datetime import datetime
from pydantic import BaseModel
from whendo.core.server import Server
import whendo.core.util as util
from whendo.sdk.client import Client


class Operations(BaseModel):
    """
    These operations are based on the existence of certain actions at a whendo server.
    """

    server: Server

    def make_client(self):
        return Client(host=self.server.host, port=self.server.port)

    def schedule_pivot(self, start: datetime, stop: datetime):
        start_stop = util.DateTime2(dt1=start, dt2=stop)
        return self.make_client().execute_action_with_rez(
            action_name="schedule_pivot_program",
            rez=util.Rez(flds={"start_stop": start_stop}),
        )

    def unschedule_pivot(self):
        return self.make_client().execute_action(action_name="unschedule_pivot_program")

    def schedule_toggle(self, start: datetime, stop: datetime):
        start_stop = util.DateTime2(dt1=start, dt2=stop)
        return self.make_client().execute_action_with_rez(
            action_name="schedule_toggle_program",
            rez=util.Rez(flds={"start_stop": start_stop}),
        )

    def unschedule_toggle(self):
        return self.make_client().execute_action(
            action_name="unschedule_toggle_program"
        )

    def schedule_notify(self, start: datetime, stop: datetime):
        start_stop = util.DateTime2(dt1=start, dt2=stop)
        return self.make_client().execute_action_with_rez(
            action_name="schedule_notify_program",
            rez=util.Rez(flds={"start_stop": start_stop}),
        )

    def unschedule_notify(self):
        return self.make_client().execute_action(
            action_name="unschedule_notify_program"
        )

    def show_pin_states(self):
        return self.make_client().execute_action(action_name="pin_state")

    def show_system_info(self):
        return self.make_client().execute_action("system_info")

    def show_scheduling(self):
        return self.make_client().execute_action("scheduling_info")

    def show_dispatcher_info(self):
        return self.make_client().execute_action("dispatcher_info")
