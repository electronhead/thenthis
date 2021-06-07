import whendo.core.actions.list_action as list_x
import whendo_gpio.action as gpio_x
import thenthis.configuration as conf_x
import whendo.core.actions.dispatch_action as disp_x
import whendo.core.programs.simple_program as prog_x


class ConfigurationAB(conf_x.Configuration):
    pinA: int
    pinB: int

    def define_inventory(self):
        super().define_inventory()
        self.actions["gpio_clear"] = gpio_x.CleanupPins()
        self.actions["pinA_on"] = gpio_x.SetPin(pin=self.pinA, on=True)
        self.actions["pinA_off"] = gpio_x.SetPin(pin=self.pinA, on=False)
        self.actions["pinA_state"] = gpio_x.PinState(pin=self.pinA)
        self.actions["pinA_state_no_setup"] = gpio_x.PinState(
            pin=self.pinA, setup=False
        )
        self.actions["pinA_toggle"] = gpio_x.TogglePin(pin=self.pinA)
        self.actions["pinB_on"] = gpio_x.SetPin(pin=self.pinB, on=True)
        self.actions["pinB_off"] = gpio_x.SetPin(pin=self.pinB, on=False)
        self.actions["pinB_state"] = gpio_x.PinState(pin=self.pinB)
        self.actions["pinB_state_no_setup"] = gpio_x.PinState(
            pin=self.pinB, setup=False
        )
        self.actions["pinB_toggle"] = gpio_x.TogglePin(pin=self.pinB)

        # implementations of 'abstract' actions
        self.actions["start_pivot"] = list_x.All(
            actions=[
                self.actions["pinA_on"],
                self.actions["pinB_on"],
                self.actions["pause1"],
                self.actions["pinB_off"],
            ]
        )
        self.actions["maintain_pivot"] = self.actions["pinA_on"]
        self.actions["toggle_pivot"] = list_x.All(
            actions=[self.actions["pinA_toggle"], self.actions["pinB_toggle"]]
        )
        self.actions["pin_state"] = list_x.All(
            actions=[
                self.actions["pinA_state_no_setup"],
                self.actions["pinB_state_no_setup"],
            ]
        )
        self.actions["reset"] = list_x.All(
            actions=[self.actions["pause2"], self.actions["gpio_clear"]])
        
        
        self.actions["notify_at_hub"] = list_x.All(
            actions=[
                list_x.Vals(vals={"file": "pin_state.txt"}),
                self.actions["mini_info"],
                self.actions["pin_state"],
                self.actions["fmt"],
                disp_x.ExecKeyTags(
                    key_tags={"roles": ["hub"]}, action_name="file_append"
                ),
            ]
        )

        def actions_for_program(self, program_name: str):
            self.actions[f"schedule_{program_name}"] = disp_x.ScheduleProgram(
                program_name=program_name
            )
            self.actions[f"unschedule_{program_name}"] = list_x.All(
                actions=[
                    disp_x.UnscheduleActiveProgram(program_name=program_name),
                    disp_x.UnscheduleProgram(program_name=program_name),
                    self.actions["reset"]
                ]
            )

        actions_for_program(self, program_name="pivot_program")
        actions_for_program(self, program_name="toggle_program")
        actions_for_program(self, program_name="notify_program")
        
        """
        programs
        """
        self.programs["pivot_program"] = (
            prog_x.PBEProgram()
            .prologue("start_pivot")
            .body_element("timely", "maintain_pivot")
            .body_element("timely", "notify_at_hub")
            .epilogue("reset")
        )
        self.programs["toggle_program"] = (
            prog_x.PBEProgram()
            .body_element("timely", "toggle_pivot")
            .body_element("timely", "notify_at_hub")
            .epilogue("reset")
        )
        self.programs["notify_program"] = prog_x.PBEProgram().body_element(
            "quickly", "notify_at_hub"
        )

        return self
