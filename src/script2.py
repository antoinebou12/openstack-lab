#!/usr/bin/env python

import json
import typer
import httpx
from rich.progress import track

app = typer.Typer()


class OpenStack:
    def __init__(self, ip, port, name, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.name = name

        self.token = self.auth_openstack()

    def auth_openstack(self):
        # Set the URL for the authentication API endpoint
        url = f"http://{self.ip}:{self.port}/identity/v3/auth/tokens"

        # Set the headers for the API request
        headers = {
            "Content-Type": "application/json",
        }

        print("Authentification à OpenStack...")

        # Set the body of the API request
        data = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": self.username,
                            "domain": {"id": "default"},
                            "password": self.password,
                        }
                    },
                },
                "scope": {"project": {"name": self.name, "domain": {"id": "default"}}},
            }
        }
        # Send the API request and get the response
        response = httpx.post(url, headers=headers, json=data)

        if response.status_code != 201:
            print("Erreur lors de l'authentification à OpenStack")
            exit(1)

        return response.headers.get("X-Subject-Token")

    def list_networks(self):
        """
        Cette commande permet de récupérer la liste des réseaux d'une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.

        Returns:
            La liste des réseaux de l'instance OpenStack.
        """
        # requête pour récupérer la liste des réseaux
        try:
            networks_response = httpx.get(
                f"http://{self.ip}:9696/v2.0/networks.json", headers={"X-Auth-Token": self.token}
            )
        except Exception:
            print("Erreur lors de la récupération de la liste des réseaux")
            exit(1)

        if networks_response.status_code != 200:
            print("Erreur lors de la récupération de la liste des réseaux")
            exit(1)

        networks = networks_response.json()

        if len(networks) == 0:
            print("Aucun réseau trouvé")
            exit(1)

        typer.echo("Liste des réseaux :")
        for network in networks:
            typer.echo(network[0])

        return networks

    def list_vms(self):
        """
        Cette commande permet de récupérer la liste des machines virtuelles d'une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.

        Returns:
            La liste des machines virtuelles de l'instance OpenStack.
        """
        # requête pour récupérer la liste des machines virtuelles
        vms_response = httpx.get(
            f"http://{self.ip}:{self.port}/compute/v2.1/servers", headers={"X-Auth-Token": self.token}
        )

        vms = vms_response.json()
        if vms == []:
            typer.echo("Aucune machine virtuelle n'a été trouvée.")

        return vms

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
    project_name: str = typer.Argument(
        "admin",
        help="OpenStack project name",
        envvar="OS_PROJECT_NAME",
        show_default=True,
    ),
):
    """Export OpenStack topology to JSON file"""

    # Création de l'instance OpenStack
    openstack = OpenStack(ip, port, project_name, username, password)

    # Récupération des informations
    network_dict = openstack.list_networks()
    servers_list = openstack.list_vms()
    router_dict = openstack.list_routers()

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
