from datetime import time, timedelta
import whendo.core.actions.file_action as file_x
import whendo.core.actions.dispatch_action as disp_x
import whendo.core.actions.list_action as list_x
import whendo.core.actions.sys_action as sys_x
import whendo.core.util as util
import whendo_gpio.action as gpio_x

import whendo.core.schedulers.timed_scheduler as sched_x
from whendo.core.scheduler import Immediately
from whendo.core.server import Server

import whendo.core.programs.simple_program as prog_x


actions = {}
actions["pinA_on"] = gpio_x.SetPin(pin=25, on=True)
actions["pinA_off"] = gpio_x.SetPin(pin=25, on=False)
actions["pinA_state"] = gpio_x.PinState(pin=25)
actions["pinB_on"] = gpio_x.SetPin(pin=27, on=True)
actions["pinB_off"] = gpio_x.SetPin(pin=27, on=False)
actions["pinB_state"] = gpio_x.PinState(pin=27)
actions["gpio_clear"] = gpio_x.CleanupPins()
actions["file_heartbeat"] = file_x.FileAppend(file="gpio_beat.txt")
actions["file_append"] = file_x.FileAppend()
actions["system_info"] = sys_x.SysInfo()
actions["mini_info"] = sys_x.MiniInfo()
actions["pause1"] = sys_x.Pause()
actions["pause2"] = sys_x.Pause(seconds=2)
actions["start_pivot"] = list_x.ListAction(
    op_mode=list_x.ListOpMode.ALL,
    actions=[
        actions["pinA_on"],
        actions["pinB_on"],
        actions["pause1"],
        actions["pinB_off"],
    ],
)
actions["pause_gpio_clear"] = list_x.ListAction(
    op_mode=list_x.ListOpMode.ALL, actions=[actions["pause2"], actions["gpio_clear"]]
)
actions["schedule_pivot_program"] = disp_x.ScheduleProgram(program_name="pivot_program")
actions["schedule_pivots"] = disp_x.ExecKeyTags(
    action_name="schedule_pivot_program", key_tags={"roles": ["pivot"]}
)
actions["notify_at_hub"] = list_x.All(
    actions=[
        list_x.Vals(vals={"file": "pin_state.txt"}),
        actions["pinA_state"],
        disp_x.ExecKeyTags(key_tags={"roles": ["hub"]}, action_name="file_append"),
    ]
)
actions["schedule_notifications"] = disp_x.ScheduleAction(
    scheduler_name="timely", action_name="notify_at_hub"
)
actions["schedule_pivot_notifications"] = disp_x.ExecKeyTags(
    key_tags={"roles": ["pivot"]}, action_name="schedule_notifications"
)


schedulers = {}
schedulers["timely"] = sched_x.Timely(
    interval=10
)  # , start=time(6,0,0), stop=time(20,0,0))
schedulers["immediately"] = Immediately()


programs = {}
programs["pivot_program"] = (
    prog_x.PBEProgram()
    .prologue("start_pivot")
    .epilogue("pause_gpio_clear")
    .body_element("timely", "pinA_on")
)

servers = {}
servers["pi3"] = Server(
    host="192.168.0.46", port=8000, tags={"server_name": ["pi3"], "roles": ["pivot"]}
)
pi3 = servers["pi3"]
servers["pi4"] = Server(
    host="192.168.0.45", port=8000, tags={"server_name": ["pi4"], "roles": ["pivot"]}
)
pi4 = servers["pi4"]
servers["hub"] = Server(
    host="192.168.0.26", port=8000, tags={"server_name": ["hub"], "roles": ["hub"]}
)
hub = servers["hub"]
