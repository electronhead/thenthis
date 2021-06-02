from pydantic import BaseModel
from whendo.sdk.client import Client
from whendo.core.server import Server
import whendo.core.util as util
from thenthis.inventory import Inventory


class Config(BaseModel):
    inventory: Inventory

    def role_servers(self, role: str = None):
        if role:
            return {
                name: server
                for (name, server) in self.inventory.servers.items()
                if role in server.tags["roles"]
            }
        else:
            return self.inventory.servers

    def hub(self):
        return list(self.role_servers("hub").values())[0]

    def server_client(self, s: Server):
        return Client(host=s.host, port=s.port)

    def execute_action(self, server: Server, action_name: str):
        client = self.server_client(server)
        return client.execute_action(action_name)

    def off(self, client: Client):
        client.execute_action("gpio_clear")

    def reset(self, client: Client):
        try:
            client.stop_jobs()
        except:
            pass
        client.clear_jobs()
        client.clear_dispatcher()

    def initialize_server(self, server):
        client = self.server_client(server)
        try:
            client.stop_jobs()
        except:
            pass
        client.clear_jobs()
        client.clear_dispatcher()
        [client.add_server(*server) for server in self.inventory.servers.items()]
        [client.add_action(*action) for action in self.inventory.actions.items()]
        [
            client.add_scheduler(*scheduler)
            for scheduler in self.inventory.schedulers.items()
        ]
        [client.add_program(*program) for program in self.inventory.programs.items()]
        client.execute_action("gpio_clear")
        client.run_jobs()

    def initialize_servers(self):
        for server in self.inventory.servers.values():
            self.initialize_server(server)

    def run_jobs(self):
        for (name, server) in self.inventory.servers.items():
            client = self.server_client(server)
            client.run_jobs()

    def schedule_programs(self, start_stop: util.DateTime2):
        client = self.server_client(self.hub())
        return client.execute_action_with_rez(
            action_name="schedule_pivots", rez=util.Rez(flds={"start_stop": start_stop})
        )

    def schedule_toggles(self, start_stop: util.DateTime2):
        client = self.server_client(self.hub())
        return client.execute_action_with_rez(
            action_name="toggle_pivots", rez=util.Rez(flds={"start_stop": start_stop})
        )

    def schedule_notifications(self):
        client = self.server_client(self.hub())
        return client.execute_action(action_name="schedule_pivot_notifications")

    def unschedule_notifications(self):
        client = self.server_client(self.hub())
        return client.execute_action(action_name="unschedule_pivot_notifications")

    def unschedule_pivots(self):
        client = self.server_client(self.hub())
        results1 = [result for result in client.execute_action("clear_all_scheduling")]
        results2 = [result for result in client.execute_action("clear_gpio_pivots")]
        return {"clear_scheduling": results1, "clear_gpio": results2}

    def show_header(self, server):
        server_txt = str(server)
        boundary = "".join(["-"] * len(server_txt))
        print(f"{boundary}\n{server_txt}\n{boundary}")

    def show_servers(self):
        for (name, server) in self.inventory.servers.items():
            client = self.server_client(server)
            self.show_header(server)
            util.PP.pprint(client.load_dispatcher().dict())

    def show_info(self):
        for (name, server) in self.inventory.servers.items():
            client = self.server_client(server)
            self.show_header(server)
            util.PP.pprint(client.execute_action("system_info").dict())

    def show_pin_state(self, server):
        client = self.server_client(server)
        self.show_header(server)
        for action_name in ["pinA_state", "pinB_state"]:
            util.PP.pprint(client.execute_action(action_name).dict())

    def show_pin_states(self):
        for (name, server) in self.role_servers("pivot").items():
            self.show_pin_state(server)
