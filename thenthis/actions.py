import whendo.core.actions.file_action as file_x
import whendo.core.actions.logic_action as logic_x
import whendo.core.actions.gpio_action as gpio_x
import whendo.core.actions.sys_action as sys_x

actions = {}
actions["green_on"] = gpio_x.SetPin(pin=27, on=True)
actions["green_off"] = gpio_x.SetPin(pin=27, on=False)
actions["green_toggle"] = gpio_x.TogglePin(pin=27)
actions["red_on"] = gpio_x.SetPin(pin=25, on=True)
actions["red_off"] = gpio_x.SetPin(pin=25, on=False)
actions["red_toggle"] = gpio_x.TogglePin(pin=25)
actions["gpio_clear"] = gpio_x.Cleanup()
actions["toggle_toggle"] = logic_x.All(action_list=[green_toggle, red_toggle])
actions["on_on"] = logic_x.All(action_list=[green_on, red_on])
actions["off_off"] = logic_x.All(action_list=[green_off, red_off])
actions["file_heartbeat"] = file_x.FileHeartbeat(file="gpio_beat.txt")
actions["system_info"] = sys_x.SysInfo()
actions["pause1"] = sys_x.Pause()
actions["pause2"] = sys_x.Pause(seconds=2)
actions["start_pivot"] = logic_x.All(action_list=[
    actions["red_on"], actions["green_on"], actions["pause1"], actions["green_off"]])