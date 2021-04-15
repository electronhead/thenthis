import ipywidgets as widgets
from pydantic import BaseModel
from ipywidgets import HBox, VBox, Accordion, AppLayout

class BaseModelWidget:
    def __init__(self, model:BaseModel):
        self.model = model
        self.name_type_default = [(x.name, x.type_, x.default) for x in model.__fields__.values()]
        self.ui_untouched = True
    
    def on_change(self, field_name: str):
        def on_value_change(change):
            setattr(self.model, field_name, change["new"])
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
                else:
                    raise TypeError(f"invalid type ({type_})")
                ui_elements.append(ui_element)
            self.ui_untouched = False
            self.widget = VBox(children=ui_elements)
        return self.widget