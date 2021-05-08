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


pinA = 18
pinB = 17
actions = {}
actions["pinA_on"] = gpio_x.SetPin(pin=pinA, on=True)
actions["pinA_off"] = gpio_x.SetPin(pin=pinA, on=False)
actions["pinA_state"] = gpio_x.PinState(pin=pinA)
actions["pinA_toggle"] = gpio_x.TogglePin(pin=pinA)
actions["pinB_on"] = gpio_x.SetPin(pin=pinB, on=True)
actions["pinB_off"] = gpio_x.SetPin(pin=pinB, on=False)
actions["pinB_state"] = gpio_x.PinState(pin=pinB)
actions["pinB_toggle"] = gpio_x.TogglePin(pin=pinB)
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

actions["toggle_toggle"] = list_x.All(actions=[actions["pinA_toggle"], actions["pinB_toggle"]])
actions["schedule_toggle_program"] = disp_x.ScheduleProgram(program_name="toggle_program")
actions["toggle_pivots"] = disp_x.ExecKeyTags(
    action_name="schedule_toggle_program", key_tags={"roles": ["pivot"]}
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
schedulers["quickly"] = sched_x.Timely(
    interval=1
)
schedulers["immediately"] = Immediately()


programs = {}
programs["pivot_program"] = (
    prog_x.PBEProgram()
    .prologue("start_pivot")
    .epilogue("pause_gpio_clear")
    .body_element("timely", "pinA_on")
)
programs["toggle_program"] = (
    prog_x.PBEProgram()
    .body_element("quickly", "toggle_toggle")
    .epilogue("pause_gpio_clear")
)

servers = {}
servers["ups"] = Server(
    host="192.168.1.94", port=8000, tags={"server_name": ["ups"], "roles": ["hub"]}
)
servers["remotepi"] = Server(
    host="192.168.1.214", port=8000, tags={"server_name":["remotepi"],"roles":["pivot"]}
)

ups = servers["ups"]
remotepi = servers["remotepi"]
