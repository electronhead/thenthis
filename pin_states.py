from datetime import timedelta, datetime, date, time
import whendo.core.util as util
import thenthis.server_configs as conf_x
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--pi", type=str, default="remotepi", dest="pi")
args = parser.parse_args()

configurations = conf_x.ranch_configurations
pp = lambda x: util.PP.pprint(x.flatten_results())

operations = {name:configuration.operations() for (name,configuration) in configurations.items()}

pi = args.pi
assert pi == "remotepi" or pi == "sandpatch-pivot"

print(f"pin states at ({pi})")    

pp(operations[pi].show_pin_states())
