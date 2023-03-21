import json
import os
from unittest import mock
from openstack import connection
from typer.testing import CliRunner
from src.script2 import app

def test_export_json():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Mock OpenStack connection and return dummy values
        with mock.patch.object(connection.Connection, "__init__") as mock_conn_init, \
             mock.patch.object(connection.Connection, "network"), \
             mock.patch.object(connection.Connection, "compute"), \
             mock.patch.object(connection.Connection, "network") as mock_network_find_network, \
             mock.patch.object(connection.Connection, "network") as mock_network_find_router, \
             mock.patch.object(connection.Connection, "network") as mock_network_interfaces:
            mock_conn_init.return_value = None
            mock_network_find_network.return_value = mock.Mock(name="network", id="network_id", status="ACTIVE")
            mock_network_find_router.return_value = mock.Mock(name="router", id="router_id", status="ACTIVE")
            mock_network_interfaces.return_value = [
                mock.Mock(port_id="port_id", subnet_id="subnet_id", fixed_ips=[{"ip_address": "ip_address"}])
            ]
            # Run the command
            result = runner.invoke(
                app,
                [
                    "export_json",
                    "--ip", "localhost",
                    "--port", "8092",
                    " --name", "admin",
                    " --username", "admin",
                    " --password", "openstack",
                ]
            )
            print(result.output)
            # Check that the command output matches the expected JSON
            assert json.loads(result.output.strip()) == {
                "network": {"name": "network", "id": "network_id", "status": "ACTIVE"},
                "servers": [],
                "router": {
                    "name": "router",
                    "id": "router_id",
                    "status": "ACTIVE",
                    "interfaces": [
                        {"port_id": "port_id", "subnet_id": "subnet_id", "ip_address": "ip_address"}
                    ]
                }
            }
            # Check that the JSON was written to a file
            assert os.path.exists("resultat.json")
            with open("resultat.json") as f:
                assert json.load(f) == json.loads(result.output.strip())
