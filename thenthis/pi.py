
import whendo.core.actions.file_action as file_x
import whendo.core.actions.list_action as list_x
import whendo.core.actions.sys_action as sys_x
import whendo_gpio.action as gpio_x

import whendo.core.schedulers.timed_scheduler as sched_x
from whendo.core.scheduler import Immediately

import whendo.core.programs.simple_program as prog_x


def compute_actions():
    actions = {}
    actions["pinA_on"] = gpio_x.SetPin(pin=27, on=True)
    actions["pinA_off"] = gpio_x.SetPin(pin=27, on=False)
    actions["pinA_state"] = gpio_x.SetPin(pin=27, on=False)
    actions["pinB_on"] = gpio_x.SetPin(pin=25, on=True)
    actions["pinB_off"] = gpio_x.SetPin(pin=25, on=False)
    actions["pinB_state"] = gpio_x.SetPin(pin=25, on=False)
    actions["gpio_clear"] = gpio_x.CleanupPins()
    actions["file_heartbeat"] = file_x.FileAppendP(file="gpio_beat.txt")
    actions["system_info"] = sys_x.SysInfo()
    actions["pause1"] = sys_x.Pause()
    actions["pause2"] = sys_x.Pause(seconds=2)
    actions["start_pivot"] = list_x.All(
        actions=[
            actions["pinA_on"],
            actions["pinB_on"],
            actions["pause1"],
            actions["pinB_off"],
        ]
    )
    actions["pause_gpio_clear"] = list_x.All(
        actions=[actions["pause2"], actions["gpio_clear"]]
    )
    return actions


def compute_schedulers():
    schedulers = {}
    schedulers["timely"] = sched_x.Timely(interval=10)
    schedulers["immediately"] = Immediately()
    return schedulers


def compute_programs():
    programs = {}
    programs["pivot_program"] = (
        prog_x.PBEProgram()
        .prologue("start_pivot")
        .epilogue("pause_gpio_clear")
        .body_element("timely", "pinA_on")
    )
    return programs

