from whendo.core.server import Server
from thenthis.configuration import Configuration
from thenthis.configuration_ab import ConfigurationAB

ranch_servers = {
    "batterypi": Server(
        host="192.168.1.94",
        port=8000,
        tags={"server_name": ["batterypi"], "roles": ["hub"]},
    ),
    "remotepi": Server(
        host="192.168.1.37",
        port=8000,
        tags={"server_name": ["remotepi"], "roles": ["pivot"]},
    ),
#     "sandpatch": Server(
#         host="192.168.1.141",
#         port=8000,
#         tags={"server_name": ["sandpatch"], "roles": ["test"]},
#     ),
    "sandpatch-pivot": Server(
        host="192.168.1.161",
        port=8000,
        tags={"server_name": ["sandpatch-pivot"], "roles": ["test"]},
    ),
}
ranch_configurations = {
    "batterypi": Configuration(server_name="batterypi", servers=ranch_servers),
    "remotepi": ConfigurationAB(
        server_name="remotepi", servers=ranch_servers, pinA=18, pinB=17
    ),
#     "sandpatch": ConfigurationAB(
#         server_name="sandpatch", servers=ranch_servers, pinA=18, pinB=17
#     ),
    "sandpatch-pivot": ConfigurationAB(
        server_name="sandpatch-pivot", servers=ranch_servers, pinA=18, pinB=17
    ),
}

pdx_servers = {
    "local": Server(
        host="192.168.0.26",
        port=8000,
        tags={"server_name": ["local"], "roles": ["hub"]},
    ),
    "pi4": Server(
        host="192.168.0.45",
        port=8000,
        tags={"server_name": ["pi4"], "roles": ["pivot"]},
    ),
    "pi3": Server(
        host="192.168.0.46",
        port=8000,
        tags={"server_name": ["pi3"], "roles": ["pivot"]},
    ),
}

pdx_configurations = {
    "local": Configuration(server_name="local", servers=pdx_servers),
    "pi4": ConfigurationAB(server_name="pi4", servers=pdx_servers, pinA=25, pinB=27),
    "pi3": ConfigurationAB(server_name="pi3", servers=pdx_servers, pinA=25, pinB=27),
}
