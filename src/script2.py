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

    def list_users(self):
        """
        Récupère la liste des utilisateurs à partir d'un endpoint OpenStack.
        """
        # requête pour récupérer la liste des utilisateurs
        print("Récupération de la liste des utilisateurs...")
        print(self.token)
        url = f"http://{self.ip}:{self.port}/identity/v3/users"
        headers = {"X-Auth-Token": self.token,
                   "Content-Type": "application/json"}
        response = httpx.get(url, headers=headers)
        users = response.json()["users"]

        if response.status_code != 200:
            print("Erreur lors de la récupération de la liste des utilisateurs")
            exit(1)

        if len(users) == 0:
            print("Aucun utilisateur trouvé")
            exit(1)

        print("Liste des utilisateurs :")
        for user in users:
            print(user["name"])

        return users

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
                f"http://{self.ip}:9696/networking/v2.0/networks.json", headers={"X-Auth-Token": self.token}
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
        for network in networks["networks"]:
            typer.echo(network["name"])
            typer.echo(network["id"])

        return networks

    def list_subnets(self):
        """
        Cette commande permet de récupérer la liste des sous-réseaux d'une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.

        Returns:
            La liste des sous-réseaux de l'instance OpenStack.
        """
        subnets_list = []
        for network in self.list_networks()["networks"]:
            subnet_object = {
                "network_id": network["id"],
                "subnets": [],
            }
            for subnet in network["subnets"]:
                typer.echo(subnet)
                subnet_object["subnets"].append(subnet)
                subnets_list.append(subnet_object)

        print(subnets_list)

        return subnets_list

    def list_projects(self):
        """
        Cette commande permet de récupérer la liste des projets d'une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.

        Returns:
            La liste des projets de l'instance OpenStack.
        """
        # requête pour récupérer la liste des projets
        projects_response = httpx.get(
            f"http://{self.ip}:{self.port}/identity/v3/projects", headers={"X-Auth-Token": self.token}
        )

        projects = projects_response.json()
        typer.echo("Liste des projets :")
        for project in projects["projects"]:
            typer.echo(project["name"])

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
        typer.echo("Liste des machines virtuelles :")
        if vms == []:
            typer.echo("Aucune machine virtuelle n'a été trouvée.")
        for vm in vms["servers"]:
            typer.echo(vm["name"])

        return vms

    def list_images(self):
        """
        Cette commande permet de récupérer la liste des images d'une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.

        Returns:
            La liste des images de l'instance OpenStack.
        """
        # requête pour récupérer la liste des images
        images_response = httpx.get(
            f"http://{self.ip}:{self.port}/image/v2/images", headers={"X-Auth-Token": self.token}
        )

        images = images_response.json()
        typer.echo("Liste des images :")
        for image in images['images']:
            typer.echo(image['name'])

    def list_flavors(self):
        """
        Cette commande permet de récupérer la liste des flavors d'une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.

        Returns:
            La liste des flavors de l'instance OpenStack.
        """
        # requête pour récupérer la liste des flavors
        flavors_response = httpx.get(
            f"http://{self.ip}:{self.port}/compute/v2.1/flavors", headers={"X-Auth-Token": self.token}
        )

        flavors = flavors_response.json()
        typer.echo("Liste des flavors :")
        for flavor in flavors['flavors']:
            typer.echo(flavor['name'])

    def list_routers(self):
        """
        Cette commande permet de récupérer la liste des routeurs d'une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.

        Returns:
            La liste des routeurs de l'instance OpenStack.
        """
        # requête pour récupérer la liste des routeurs
        routers_response = httpx.get(
            f"http://{self.ip}:9696/networking/v2.0/routers", headers={"X-Auth-Token": self.token}
        )

        routers = routers_response.json()

        print(routers)

        typer.echo("Liste des routeurs :")
        for router in routers['routers']:
            typer.echo(router['name'])

        return routers

@app.command()
def export_json(
    ip: str = typer.Argument(
        "172.28.0.2",
        help="OpenStack IP address",
        envvar="DEVSTACK_IP",
        show_default=True,
    ),
    port: str = typer.Argument(
        "80",
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
        "password",
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
    result_json = json.dumps(
        result_dict, indent=4, sort_keys=True, default=str
    )

    # Ecriture du JSON dans un fichier texte
    with open("resultat.json", "w") as f:
        json.dump(result_dict, f)

    return result_json

if __name__ == "__main__":
    app()
