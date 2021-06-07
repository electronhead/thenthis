from datetime import timedelta, datetime, date, time
import whendo.core.util as util
import thenthis.server_configs as conf_x
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--pi", type=str, default="remotepi", dest="pi")
parser.add_argument("--program", type=str, default="pivot", dest="program")
args = parser.parse_args()

configurations = conf_x.ranch_configurations
pp = lambda x: util.PP.pprint(x.flatten_results())

operations = {name:configuration.operations() for (name,configuration) in configurations.items()}

pi = args.pi
assert pi == "remotepi" or pi == "sandpatch-pivot"
    
program = args.program
assert program == "pivot" or program == "toggle"

print(f"stop ({program}) at ({pi})")    

if program == "pivot":
    pp(operations[pi].unschedule_pivot())
else:
    pp(operations[pi].unschedule_toggle())
    