from whendo.core.server import Server
from thenthis.config import Config
from thenthis.inventory import Inventory


ranch_config = Config(
    inventory=Inventory(pinA=18, pinB=17)
    .create_actions()
    .create_schedulers()
    .create_programs()
    .put_server(
        "batterypi",
        Server(
            host="192.168.1.94",
            port=8000,
            tags={"server_name": ["batterypi"], "roles": ["hub"]},
        ),
    )
    .put_server(
        "remotepi",
        Server(
            host="192.168.1.214",
            port=8000,
            tags={"server_name": ["remotepi"], "roles": ["pivot"]},
        ),
    )
    .put_server(
        "sandpatch",
        Server(
            host="192.168.1.141",
            port=8000,
            tags={"server_name": ["sandpatch"], "roles": ["pivot"]},
        ),
    )
    .put_server(
        "sandpatch-pivot",
        Server(
            host="192.168.1.11",
            port=8000,
            tags={"server_name": ["sandpatch"], "roles": ["pivot"]},
        ),
    )
)
pdx_config = Config(
    inventory=Inventory(pinA=25, pinB=27)
    .create_actions()
    .create_schedulers()
    .create_programs()
    .put_server(
        "local",
        Server(
            host="192.168.0.26",
            port=8000,
            tags={"server_name": ["local"], "roles": ["hub"]},
        ),
    )
    .put_server(
        "pi4",
        Server(
            host="192.168.0.45",
            port=8000,
            tags={"server_name": ["pi4"], "roles": ["pivot"]},
        ),
    )
    .put_server(
        "pi3",
        Server(
            host="192.168.0.46",
            port=8000,
            tags={"server_name": ["pi3"], "roles": ["pivot"]},
        ),
    )
)
