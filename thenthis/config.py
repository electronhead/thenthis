from whendo.sdk.client import Client
from whendo.core.server import Server
import whendo.core.util as util
import whendo.core.actions.dispatch_action as disp_x
import whendo.core.resolver as rslv_x
import thenthis.inventory as inventory


actions = inventory.actions
schedulers = inventory.schedulers
programs = inventory.programs
servers = inventory.servers

def role_servers(role:str=None):
    if role:
        return {name:server for (name,server) in servers.items() if role in server.tags["roles"]}
    else:
        return servers
hub = list(role_servers("hub").values())[0]


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
    return client.execute_action_with_rez(
        action_name="schedule_pivots", rez=util.Rez(flds={"start_stop": start_stop})
    )

def schedule_toggles(start_stop: util.DateTime2):
    client = server_client(hub)
    return client.execute_action_with_rez(
        action_name="toggle_pivots", rez=util.Rez(flds={"start_stop": start_stop})
    )

def schedule_notifications():
    client = server_client(hub)
    return client.execute_action(action_name="schedule_pivot_notifications")

def unschedule_pivots():
    client = server_client(hub)
    action = disp_x.ClearAllScheduling()
    results1 = [result for result in client.execute_supplied_action(disp_x.ExecSuppliedKeyTags(key_tags={"roles":["pivot"]}, action=action))]
    results2 = [result for result in client.execute_supplied_action(disp_x.ExecKeyTags(key_tags={"roles":["pivot"]}, action_name="gpio_clear"))]
    return {
        "clear_scheduling": results1,
        "clear_gpio": results2
    }
    
def show_header(server):
    server_txt = str(server)
    boundary = ''.join(["-"] * len(server_txt))
    print(f"{boundary}\n{server_txt}\n{boundary}")

def show_servers():
    for (name, server) in servers.items():
        client = server_client(server)
        show_header(server)
        util.PP.pprint(client.load_dispatcher().dict())

def show_info():
    for (name, server) in servers.items():
        client = server_client(server)
        show_header(server)
        util.PP.pprint(client.execute_action("system_info"))

def show_pin_states():
    for (name, server) in role_servers("pivot").items():
        client = server_client(server)
        show_header(server)
        for action_name in ["pinA_state", "pinB_state"]:
            rez = rslv_x.resolve_rez(client.execute_action(action_name))
            print(f"\taction ({action_name}) value ({1 if rez.result else 0})")