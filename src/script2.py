#!/usr/bin/env python

import subprocess
import requests
import json
import time
import openstack
import typer
import httpx
from rich.progress import track
from openstack import connection

app = typer.Typer()

@app.command()
def export_json(
    ip: str = typer.Argument(
        "localhost",
        help="OpenStack IP address",
        envvar="DEVSTACK_IP",
        show_default=True,
    ),
    port: str = typer.Argument(
        "8092",
        help="OpenStack port",
        envvar="DEVSTACK_PORT",
        show_default=True,
    ),
    name: str = typer.Argument(
        "admin",
        help="OpenStack project name",
        envvar="OS_PROJECT_NAME",
        show_default=True,
    ),
    username: str = typer.Argument(
        "admin",
        help="OpenStack username",
        envvar="OS_USERNAME",
        show_default=True,
    ),
    password: str = typer.Argument(
        "openstack",
        help="OpenStack password",
        envvar="OS_PASSWORD",
        show_default=True,
    ),
):
    """Export OpenStack topology to JSON file"""

    # Informations d'authentification pour se connecter à OpenStack
    auth_url = f"http://{ip}:{port}/identity/v3"
    user_domain_name = "Default"
    project_domain_name = "Default"

    # Connexion à OpenStack
    conn = connection.Connection(
        auth_url=auth_url,
        project_name=name,
        username=username,
        password=password,
        user_domain_name=user_domain_name,
        project_domain_name=project_domain_name,
    )

    # Récupération des informations du réseau
    network = conn.network.find_network("private")
    network_dict = {"name": network.name, "id": network.id, "status": network.status}

    # Récupération des informations des machines virtuelles
    servers = conn.compute.servers()
    servers_list = []
    for server in track(servers, description="Fetching servers..."):
        server_dict = {"name": server.name, "id": server.id, "status": server.status}
        servers_list.append(server_dict)

    # Récupération des informations du routeur
    router = conn.network.find_router("router1")
    router_dict = {"name": router.name, "id": router.id, "status": router.status}
    interfaces = conn.network.interfaces(router_id=router.id)
    interfaces_list = []
    for interface in track(interfaces, description="Fetching interfaces..."):
        interface_dict = {
            "port_id": interface.port_id,
            "subnet_id": interface.subnet_id,
            "ip_address": interface.fixed_ips[0]["ip_address"],
        }
        interfaces_list.append(interface_dict)
    router_dict["interfaces"] = interfaces_list

    # Création du dictionnaire contenant toutes les informations
    result_dict = {
        "network": network_dict,
        "servers": servers_list,
        "router": router_dict,
    }

    # Conversion en JSON et affichage
    result_json = json.dumps(result_dict)

    # Ecriture du JSON dans un fichier texte
    with open("resultat.json", "w") as f:
        json.dump(result_dict, f)

    return result_json
