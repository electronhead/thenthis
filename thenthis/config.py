from datetime import timedelta
from whendo.sdk.client import Client
import whendo.core.util as util
import thenthis.pi as pi_objs
from thenthis.ui import Pivot, Chain, Flock

def compute_flock():
    pi3 = Pivot(
        name="pi3",
        host="192.168.0.46",
    )
    pi4 = Pivot(
        name="pi4",
        host="192.168.0.45",
    )
    chain = Chain(
        name="the_band", pivots=[pi3, pi4], programs=["pivot_program"]*2, durations=[timedelta(seconds=45), timedelta(seconds=30)]
    )
    return Flock(pivots=[pi3, pi4], chains=[chain])


def reset(client: Client):
    try:
        client.stop_jobs()
    except:
        pass
    client.clear_jobs()
    client.clear_dispatcher()


def add_actions(client: Client):
    [client.add_action(*action) for action in pi_objs.compute_actions().items()]


def add_schedulers(client: Client):
    [client.add_scheduler(*scheduler) for scheduler in pi_objs.compute_schedulers().items()]


def add_programs(client: Client):
    [client.add_program(*program) for program in pi_objs.compute_programs().items()]


def initialize_pivots(flock: Flock):
    for pivot in flock.pivots:
        client = Client(host=pivot.host, port=pivot.port)
        reset(client)
        add_actions(client)
        add_schedulers(client)
        add_programs(client)
        client.run_jobs()


def schedule_programs(flock: Flock):
    for chain in flock.chains:
        chain.schedule_programs(start=util.Now.dt() + timedelta(seconds=5))