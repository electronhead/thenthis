from whendo.sdk.client import Client
from whendo.core.server import Server
import whendo.core.util as util
import whendo.core.actions.dispatch_action as disp_x
import thenthis.inventory as inventory


actions = inventory.actions
schedulers = inventory.schedulers
programs = inventory.programs
servers = inventory.servers
hub = inventory.hub
pi3 = inventory.pi3
pi4 = inventory.pi4
pivot_servers = [pi3, pi4]


def server_client(s: Server):
    return Client(host=s.host, port=s.port)


def off(client: Client):
    client.execute_action("gpio_clear")


def reset(client: Client):
    try:
        client.stop_jobs()
    except:
        pass
    client.clear_jobs()
    client.clear_dispatcher()


def initialize_servers():
    for (name, server) in servers.items():
        client = server_client(server)
        reset(client)
        [client.add_server(*server) for server in servers.items()]
        [client.add_action(*action) for action in actions.items()]
        [client.add_scheduler(*scheduler) for scheduler in schedulers.items()]
        [client.add_program(*program) for program in programs.items()]
        off(client)
        client.run_jobs()


def schedule_programs(start_stop: util.DateTime2):
    client = server_client(hub)
    client.execute_action_with_rez(
        action_name="schedule_pivots", rez=util.Rez(flds={"start_stop": start_stop})
    )

def schedule_notifications():
    client = server_client(hub)
    client.execute_action(action_name="schedule_pivot_notifications")

def unschedule_pivots():
    client = server_client(hub)
    action = disp_x.ClearAllScheduling()
    client.execute_supplied_action(disp_x.ExecSuppliedKeyTags(key_tags={"roles":["pivot"]}, action=action))
    client.execute_supplied_action(disp_x.ExecKeyTags(key_tags={"roles":["pivot"]}, action_name="gpio_clear"))

def show_servers():
    for (name, server) in servers.items():
        client = server_client(server)
        server_txt = str(server)
        boundary = ''.join(["-"] * len(server_txt))
        print(f"{boundary}\n{server}\n{boundary}")
        util.PP.pprint(client.load_dispatcher().dict())
        print("\n")
