import ipywidgets as widgets
from pydantic import BaseModel
import json
from datetime import datetime, time, timedelta
import ipywidgets as widgets
import whendo.core.util as util

class BaseModelWidget:
    def __init__(self, model:BaseModel):
        self.model = model
        self.name_type_default = [(x.name, x.type_, x.default) for x in model.__fields__.values()]
        self.ui_untouched = True
    
    def on_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, change["new"])
        return on_value_change

    def on_time_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, str_to_t(change["new"]))
        return on_value_change

    def on_datetime_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, util.str_to_dt(change["new"]))
        return on_value_change

    def ui(self):
        if self.ui_untouched:
            ui_elements = []
            for (name, type_, default) in self.name_type_default:
                ui_element = None
                if type_==str:
                    ui_element = widgets.Text(
                        value=getattr(self.model, name),
                        placeholder=str(default) if default else "",
                        description=name,
                        style={"description_width": "initial"},
                    )
                    ui_element.observe(self.on_change(name), names="value")
                elif type_==int:
                    ui_element = widgets.IntText(
                        value=getattr(self.model, name),
                        placeholder=str(default) if default else "",
                        description=name,
                        style={"description_width": "initial"},
                    )
                    ui_element.observe(self.on_change(name), names="value")
                elif type_==bool:
                    ui_element = widgets.IntText(
                        value=getattr(self.model, name),
                        placeholder=str(default) if default else "",
                        description=name,
                        style={"description_width": "initial"},
                    )
                    ui_element.observe(self.on_change(name), names="value")
                elif type_==dict:
                    value_str = json.dumps(getattr(self.model, name))
                    ui_element = widgets.Text(
                        value=value_str,
                        placeholder=str(default) if default else "",
                        description=name,
                        style={"description_width": "initial"},
                    )
                    ui_element.observe(self.on_change(name), names="value")
                elif type_==time:
                    value_str = t_to_str(getattr(self.model, name))
                    ui_element = widgets.Text(
                        value=value_str,
                        placeholder=str(default) if default else "",
                        description=name,
                        style={"description_width": "initial"},
                    )
                    ui_element.observe(self.on_time_change(name), names="value")
                elif type_==datetime:
                    value_str = util.dt_to_str(getattr(self.model, name))
                    ui_element = widgets.Text(
                        value=value_str,
                        placeholder=str(default) if default else "",
                        description=name,
                        style={"description_width": "initial"},
                    )
                    ui_element.observe(self.on_datetime_change(name), names="value")
                else:
                    raise TypeError(f"invalid type ({type_})")
                ui_elements.append(ui_element)
            self.ui_untouched = False
            self.widget = widgets.VBox(children=ui_elements)
        return self.widget


def t_to_str(t: time) -> str:
    return t.isoformat(timespec="seconds")


def str_to_t(ts: str) -> time:
    return time.fromisoformat(ts)