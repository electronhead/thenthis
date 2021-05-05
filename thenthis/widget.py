import ipywidgets as widgets
from pydantic import BaseModel
import json
from typing import List, Any
from datetime import datetime, time, timedelta
from ipydatetime import DatetimePicker, TimePicker
import whendo.core.util as util
from whendo.core.actions.list_action import ListOpMode


class DictionaryWidget:
    def __init__(self, dictionary: dict):
        self.dictionary = dictionary
        self.widget = None

    def ui(self):
        if not self.widget:
            titles = []
            ui_elements = []
            if self.dictionary:
                for (key, value) in self.dictionary.items():
                    key_element = None
                    if isinstance(value, BaseModel):
                        key_element = BaseModelWidget(model=value).ui()
                    elif isinstance(value, list):
                        key_element = ListWidget(values=value).ui()
                    elif isinstance(value, dict):
                        key_element = DictionaryWidget(dictionary=value).ui()
                    elif isinstance(value, BaseModel):
                        key_element = BaseModelWidget(model=value).ui()
                    else:
                        key_element = widgets.Label(
                            value=f"unknown element type ({str(value)}"
                        )
                    try:
                        titles.append(key + " -- " + value.description())
                    except AttributeError:
                        titles.append(key)
                    ui_elements.append(widgets.HBox(children=[key_element]))
                self.widget = widgets.Accordion(children=ui_elements, titles=titles)
            else:
                self.widget = widgets.Label(
                    value=f"NULL element encountered when rendering a DictionaryWidget"
                )
        return self.widget


class BaseModelWidget:
    def __init__(self, model: BaseModel):
        self.model = model
        self.name_type_default = [
            (x.name, x.type_, x.default) for x in model.__fields__.values()
        ]
        self.widget = None

    def on_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, change["new"])

        return on_value_change

    def on_int_change(self, field_name: str):
        def on_value_change(change):
            value = change["new"]
            setattr(self.model, field_name, int(value) if value else None)

        return on_value_change

    def on_time_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, str_to_t(change["new"]))

        return on_value_change

    def on_datetime_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, change["new"])

        return on_value_change

    def on_list_op_mode_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, ListOpMode(change["new"]))

        return on_value_change

    def ui(self):
        if not self.widget:
            ui_elements = []
            if len(self.name_type_default) > 0:
                for (name, type_, default) in self.name_type_default:
                    ui_element = None
                    value = getattr(self.model, name)
                    type_ = type(value) if value else type_
                    if type_ == str:
                        if name != value:  # ignore name==value fields
                            ui_element = widgets.Text(
                                value=value,
                                placeholder=str(default) if default else "",
                                description=name,
                                style={"description_width": "initial"},
                            )
                            ui_element.observe(self.on_change(name), names="value")
                    elif type_ == int:
                        ui_element = widgets.IntText(
                            value=str(value) if value else None,
                            placeholder=str(default) if default else "",
                            description=name,
                            style={"description_width": "initial"},
                        )
                        ui_element.observe(self.on_int_change(name), names="value")
                    elif type_ == float:
                        ui_element = widgets.FloatText(
                            value=value,
                            placeholder=str(default) if default else "",
                            description=name,
                            style={"description_width": "initial"},
                        )
                        ui_element.observe(self.on_change(name), names="value")
                    elif type_ == bool:
                        ui_element = widgets.IntText(
                            value=value,
                            placeholder=str(default) if default else "",
                            description=name,
                            style={"description_width": "initial"},
                        )
                        ui_element.observe(self.on_change(name), names="value")
                    elif type_ == time:
                        if False:
                            ui_element = TimePicker(
                                value=value,
                                description=name,
                                style={"description_width": "initial"},
                            )
                            ui_element.observe(self.on_change(name), names="value")
                        else:
                            ui_element = widgets.Text(
                                value=util.t_to_str(value) if value else None,
                                placeholder=str(default) if default else "",
                                description=name,
                                style={"description_width": "initial"},
                            )
                            ui_element.observe(self.on_time_change(name), names="value")
                    elif type_ == datetime:
                        ui_element = DatetimePicker(
                            value=value,
                            description=name,
                            style={"description_width": "initial"},
                        )
                        ui_element.observe(self.on_change(name), names="value")
                    #                         value_str = util.dt_to_str(value)
                    #                         ui_element = widgets.Text(
                    #                             value=value_str,
                    #                             placeholder=str(default) if default else "",
                    #                             description=name,
                    #                             style={"description_width": "initial"},
                    #                         )
                    #                         ui_element.observe(self.on_datetime_change(name), names="value")
                    elif type_ == ListOpMode:
                        value_str = value.value
                        ui_element = widgets.Select(
                            options=[
                                x.value
                                for x in ListOpMode.__dict__["_member_map_"].values()
                            ],
                            value=value_str,
                            description="list op mode",
                            disabled=False,
                        )
                        ui_element.observe(
                            self.on_list_op_mode_change(name), names="value"
                        )
                    elif type_ == dict:
                        ui_element = DictionaryWidget(value).ui()
                    elif type_ == list:
                        ui_element = ListWidget(value).ui()
                    elif isinstance(getattr(self.model, name), BaseModel):
                        ui_element = BaseModelWidget(value).ui()
                    else:
                        ui_element = widgets.Label(
                            value=f"unknown element type ({type(value)} value ({value})"
                        )

                    if ui_element:
                        ui_elements.append(ui_element)

            else:
                print(f"EMPTY UI FOR: ({self.model})")
            self.widget = widgets.VBox(children=ui_elements)
        return self.widget


class ListWidget:
    def __init__(self, values: List[Any]):
        self.values = values
        self.widget = None

    def on_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, change["new"])

        return on_value_change

    def on_time_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, util.str_to_t(change["new"]))

        return on_value_change

    def on_datetime_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, util.str_to_dt(change["new"]))

        return on_value_change

    def ui(self):
        if not self.widget:
            ui_elements = []
            i = 0
            for value in self.values:
                i += 1
                type_ = type(value)
                ui_element = None
                if type_ == str:
                    ui_element = widgets.Text(
                        value=value,
                        description=str(i),
                        style={"description_width": "initial"},
                    )
                    # ui_element.observe(self.on_change(name), names="value")
                elif type_ == int:
                    ui_element = widgets.IntText(
                        value=value,
                        description=str(i),
                        style={"description_width": "initial"},
                    )
                    # ui_element.observe(self.on_change(name), names="value")
                elif type_ == float:
                    ui_element = widgets.FloatText(
                        value=value,
                        description=str(i),
                        style={"description_width": "initial"},
                    )
                    # ui_element.observe(self.on_change(name), names="value")
                elif type_ == bool:
                    ui_element = widgets.IntText(
                        value=value,
                        description=str(i),
                        style={"description_width": "initial"},
                    )
                    # ui_element.observe(self.on_change(name), names="value")
                elif type_ == time:
                    value = value
                    value_str = util.t_to_str(value) if value else ""
                    ui_element = widgets.Text(
                        value=value_str,
                        description=str(i),
                        style={"description_width": "initial"},
                    )
                    # ui_element.observe(self.on_time_change(name), names="value")
                elif type_ == datetime:
                    value_str = util.dt_to_str(value)
                    ui_element = widgets.Text(
                        value=value_str,
                        description=str(i),
                        style={"description_width": "initial"},
                    )
                    # ui_element.observe(self.on_datetime_change(name), names="value")
                elif type_ == dict:
                    ui_element = DictionaryWidget(dictionary=value).ui()
                elif isinstance(value, BaseModel):
                    description = ""
                    try:
                        description = f" -- {value.description()}"
                    except AttributeError:
                        pass
                    ui_element = widgets.Accordion(
                        children=[BaseModelWidget(model=value).ui()],
                        titles=[value.__class__.__name__ + description],
                    )
                else:
                    ui_element = widgets.Label(
                        value=f"unknown element type ({str(value)}"
                    )
                #                 else:
                #                     raise TypeError(f"invalid type ({type_})")
                ui_elements.append(ui_element)
            self.widget = widgets.VBox(children=ui_elements)
        return self.widget
