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
import whendo.core.schedulers.timed_scheduler as sched_x
from whendo.core.scheduler import Immediately
from whendo.sdk.client import Client
from thenthis.operations import Operations


class NeedAnAction(Action):
    def execute(self, tag: str = None, rez: util.Rez = None):
        return self.action_result(result = "NeedAnAction", rez=rez, flds = rez.flds if rez else None)


class Configuration(BaseModel):
    server_name: str
    servers: Dict[str, Server]
    actions: Dict[str, Action] = {}
    schedulers: Dict[str, Scheduler] = {}
    programs: Dict[str, Program] = {}

    def operations(self):
        self.define_inventory()
        self.initialize_server()
        return Operations(server=self.get_server())

    def get_server(self):
        return self.servers[self.server_name]

    def make_client(self):
        server = self.get_server()
        return Client(host=server.host, port=server.port)

    def initialize_server(self):
        client = self.make_client()
        try:
            client.stop_jobs()
        except:
            pass
        client.clear_jobs()
        client.clear_dispatcher()
        [client.add_server(*server) for server in self.servers.items()]
        [client.add_action(*action) for action in self.actions.items()]
        [
            client.add_scheduler(*scheduler)
            for scheduler in self.schedulers.items()
        ]
        [client.add_program(*program) for program in self.programs.items()]
        client.execute_action("reset")
        client.run_jobs()

    def define_inventory(self):
        """
        abstract actions (defined or not in sub-Configurations)
        """
        self.actions["reset"] = NeedAnAction()

        """
        actions
        """
        self.actions["file_append"] = file_x.FileAppend()
        self.actions["system_info"] = sys_x.SysInfo()
        self.actions["mini_info"] = sys_x.MiniInfo()
        self.actions["scheduling_info"] = list_x.All(actions=[
            sys_x.MiniInfo(),
            disp_x.SchedulingInfo(),
            list_x.RezFmt()
        ])
        self.actions["dispatcher_info"] = disp_x.DispatcherDump()
        self.actions["pause1"] = sys_x.Pause(seconds=1)
        self.actions["pause2"] = sys_x.Pause(seconds=2)
        self.actions["fmt"] = list_x.RezFmt()

        """
        schedulers
        """
        self.schedulers["leisurely"] = sched_x.Timely(interval=30)
        self.schedulers["timely"] = sched_x.Timely(interval=10)
        self.schedulers["quickly"] = sched_x.Timely(interval=1)
        self.schedulers["immediately"] = Immediately()


        return self
