from pydantic import BaseModel
from typing import Dict
from whendo.core.action import Action
from whendo.core.scheduler import Scheduler
from whendo.core.program import Program
from whendo.core.server import Server
import whendo.core.actions.file_action as file_x
import whendo.core.actions.dispatch_action as disp_x
import whendo.core.actions.list_action as list_x
import whendo.core.actions.sys_action as sys_x
import whendo.core.util as util
import whendo_gpio.action as gpio_x

import whendo.core.schedulers.timed_scheduler as sched_x
from whendo.core.scheduler import Immediately

import whendo.core.programs.simple_program as prog_x


class Inventory(BaseModel):
    pinA: int
    pinB: int
    actions: Dict[str, Action] = {}
    schedulers: Dict[str, Scheduler] = {}
    programs: Dict[str, Program] = {}
    servers: Dict[str, Server] = {}

    def create_actions(self):
        self.actions["pinA_on"] = gpio_x.SetPin(pin=self.pinA, on=True)
        self.actions["pinA_off"] = gpio_x.SetPin(pin=self.pinA, on=False)
        self.actions["pinA_state"] = gpio_x.PinState(pin=self.pinA)
        self.actions["pinA_state_no_setup"] = gpio_x.PinState(pin=self.pinA, setup=False)
        self.actions["pinA_toggle"] = gpio_x.TogglePin(pin=self.pinA)
        self.actions["pinB_on"] = gpio_x.SetPin(pin=self.pinB, on=True)
        self.actions["pinB_off"] = gpio_x.SetPin(pin=self.pinB, on=False)
        self.actions["pinB_state"] = gpio_x.PinState(pin=self.pinB)
        self.actions["pinB_state_no_setup"] = gpio_x.PinState(pin=self.pinB, setup=False)
        self.actions["pinB_toggle"] = gpio_x.TogglePin(pin=self.pinB)
        self.actions["gpio_clear"] = gpio_x.CleanupPins()
        self.actions["file_append"] = file_x.FileAppend()
        self.actions["system_info"] = sys_x.SysInfo()
        self.actions["mini_info"] = sys_x.MiniInfo()
        self.actions["pause1"] = sys_x.Pause()
        self.actions["pause2"] = sys_x.Pause(seconds=2)

        self.actions["start_pivot"] = list_x.All(
            actions=[
                self.actions["pinA_on"],
                self.actions["pinB_on"],
                self.actions["pause1"],
                self.actions["pinB_off"],
            ]
        )
        self.actions["toggle_toggle"] = list_x.All(
            actions=[self.actions["pinA_toggle"], self.actions["pinB_toggle"]]
        )
        self.actions["pause_gpio_clear"] = list_x.All(
            actions=[self.actions["pause2"], self.actions["gpio_clear"]]
        )
        self.actions["notify_at_hub"] = list_x.All(
            actions=[
                list_x.Vals(vals={"file": "pin_state.txt"}),
                self.actions["pinA_state_no_setup"],
                disp_x.ExecKeyTags(
                    key_tags={"roles": ["hub"]}, action_name="file_append"
                ),
            ]
        )

        self.actions["schedule_notifications"] = disp_x.ScheduleAction(
            scheduler_name="randomly", action_name="notify_at_hub"
        )

        self.actions["unschedule_notifications"] = disp_x.UnscheduleSchedulerAction(
            scheduler_name="randomly", action_name="notify_at_hub"
        )

        self.actions["schedule_pivot_program"] = disp_x.ScheduleProgram(
            program_name="pivot_program"
        )
        self.actions["schedule_toggle_program"] = disp_x.ScheduleProgram(
            program_name="toggle_program"
        )

        self.actions["schedule_pivots"] = disp_x.ExecKeyTags(
            action_name="schedule_pivot_program", key_tags={"roles": ["pivot"]}
        )
        self.actions["toggle_pivots"] = disp_x.ExecKeyTags(
            action_name="schedule_toggle_program", key_tags={"roles": ["pivot"]}
        )
        self.actions["schedule_pivot_notifications"] = disp_x.ExecKeyTags(
            key_tags={"roles": ["pivot"]}, action_name="schedule_notifications"
        )
        self.actions["unschedule_pivot_notifications"] = disp_x.ExecKeyTags(
            key_tags={"roles": ["pivot"]}, action_name="unschedule_notifications"
        )
        self.actions["clear_all_scheduling"] = disp_x.ExecSuppliedKeyTags(
            key_tags={"roles": ["pivot"]}, action=disp_x.ClearAllScheduling()
        )
        self.actions["clear_gpio_pivots"] = disp_x.ExecKeyTags(
            key_tags={"roles": ["pivot"]}, action_name="gpio_clear"
        )
        return self

    def put_action(self, name: str, obj: Action):
        self.actions[name] = obj
        return self

    def create_schedulers(self):
        self.schedulers["timely"] = sched_x.Timely(interval=10)
        self.schedulers["quickly"] = sched_x.Timely(interval=1)
        self.schedulers["immediately"] = Immediately()
        self.schedulers["randomly"] = sched_x.Randomly(low=3, high=7)
        return self

    def put_scheduler(self, name: str, obj: Scheduler):
        self.schedulers[name] = obj
        return self

    def create_programs(self):
        self.programs["pivot_program"] = (
            prog_x.PBEProgram()
            .prologue("start_pivot")
            .epilogue("pause_gpio_clear")
            .body_element("timely", "pinA_on")
        )
        self.programs["toggle_program"] = (
            prog_x.PBEProgram()
            .body_element("quickly", "toggle_toggle")
            .epilogue("pause_gpio_clear")
        )
        return self

    def put_program(self, name: str, obj: Program):
        self.programs[name] = obj
        return self

    def put_server(self, name: str, obj: Server):
        self.servers[name] = obj
        return self
