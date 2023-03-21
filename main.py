#!/usr/bin/env python

from src.script1 import create_topology
from src.script2 import export_json
from src.openstack_api import list_users, list_vms, list_networks
from src.scripts.convert_ova import vagrant, docker, app
import typer


app = typer.Typer()

if __name__ == "main":
    app.add_typer(create_topology, name="create_topology")
    app.add_typer(export_json, name="export_json")