#!/usr/bin/env python

import typer
from rich.progress import track
import httpx
import os

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
        headers = {"X-Auth-Token": self.token, "Content-Type": "application/json"}
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

    def list_subnets(self):
        """
        Cette commande permet de récupérer la liste des sous-réseaux d'une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.

        Returns:
            La liste des sous-réseaux de l'instance OpenStack.
        """
        # requête pour récupérer la liste des sous-réseaux
        subnets_response = httpx.get(
            f"http://{self.ip}:9696/v2.0/networks.json", headers={"X-Auth-Token": self.token}
        )

        if subnets_response.status_code != 200:
            print("Erreur lors de la récupération de la liste des sous-réseaux")
            exit(1)

        subnets = subnets_response.json()

        if len(subnets) == 0:
            print("Aucun sous-réseau trouvé")
            exit(1)

        typer.echo("Liste des sous-réseaux :")
        for subnet in subnets:
            typer.echo(subnet[0])


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

    def create_network(self, name):
        """
        Cette commande permet de créer un réseau dans une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            name: le nom du réseau à créer.

        Returns:
            Le réseau créé.
        """
        # requête pour créer un réseau
        network_response = httpx.post(
            f"http://{self.ip}:9696",
            headers={"X-Auth-Token": self.token},
            json={"network": {"name": name}},
        )
        network = network_response.json()

        typer.echo(f"Le réseau {name} a été créé avec succès.")

        return network

    def create_subnet(self, name, cidr, network_id):
        """
        Cette commande permet de créer un sous-réseau dans une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            name: le nom du sous-réseau à créer.
            cidr: le CIDR du sous-réseau à créer.
            network_id: l'identifiant du réseau dans lequel créer le sous-réseau.

        Returns:
            Le sous-réseau créé.
        """
        # requête pour créer un sous-réseau
        subnet_response = httpx.post(
            f"http://{self.ip}:{self.port}/network/v2.0/subnets",
            headers={"X-Auth-Token": self.token},
            json={"subnet": {"name": name, "cidr": cidr, "network_id": network_id}},
        )
        subnet = subnet_response.json()

        typer.echo(f"Le sous-réseau {name} a été créé avec succès.")

        return subnet

    def create_router(self, name, external_network_id, subnet_id):
        """
        Cette commande permet de créer un routeur dans une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            name: le nom du routeur à créer.
            external_network_id: l'identifiant du réseau externe.
            subnet_id: l'identifiant du sous-réseau à attacher au routeur.

        Returns:
            Le routeur créé.
        """
        # requête pour créer un routeur
        router_response = httpx.post(
            f"http://{self.ip}:9696/network/v2.0/routers",
            headers={"X-Auth-Token": self.token},
            json={
                "router": {
                    "name": name,
                    "external_gateway_info": {"network_id": external_network_id},
                    "admin_state_up": True,
                }
            },
        )
        router = router_response.json()

        # requête pour attacher un sous-réseau au routeur
        httpx.put(
            f"http://{self.ip}:9696/network/v2.0/routers/{router['router']['id']}/add_router_interface",
            headers={"X-Auth-Token": self.token},
            json={"subnet_id": subnet_id},
        )

        typer.echo(f"Le routeur {name} a été créé avec succès.")

        return router

    def create_vm(self, name, image_id, flavor_id, network_id):
        """
        Cette commande permet de créer une machine virtuelle dans une instance OpenStack.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            name: le nom de la machine virtuelle à créer.
            image_id: l'identifiant de l'image à utiliser pour la machine virtuelle.
            flavor_id: l'identifiant du type de machine virtuelle à créer.
            network_id: l'identifiant du réseau dans lequel créer la machine virtuelle.

        Returns:
            La machine virtuelle créée.
        """
        # requête pour créer une machine virtuelle
        vm_response = httpx.post(
            f"http://{self.ip}:{self.port}/compute/v2.1/servers",
            headers={"X-Auth-Token": self.token},
            json={
                "server": {
                    "name": name,
                    "imageRef": image_id,
                    "flavorRef": flavor_id,
                    "networks": [{"uuid": network_id}],
                }
            },
        )
        vm = vm_response.json()

        typer.echo(f"La machine virtuelle {name} a été créée avec succès.")

        return vm

    def get_image_id(self, image_name):
        """
        Cette commande permet de récupérer l'identifiant d'une image.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            image_name: le nom de l'image.

        Returns:
            L'identifiant de l'image.
        """
        # requête pour récupérer la liste des images
        images_response = httpx.get(
            f"http://{self.ip}:{self.port}/image/v2/images", headers={"X-Auth-Token": self.token}
        )
        images = images_response.json()
        for image in images["images"]:
            if image["name"] == image_name:
                return image["id"]

    def get_flavor_id(self, flavor_name):
        """
        Cette commande permet de récupérer l'identifiant d'un type de machine virtuelle.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            flavor_name: le nom du type de machine virtuelle.

        Returns:
            L'identifiant du type de machine virtuelle.
        """
        # requête pour récupérer la liste des types de machine virtuelle
        flavors_response = httpx.get(
            f"http://{self.ip}:{self.port}/compute/v2.1/flavors", headers={"X-Auth-Token": self.token}
        )
        flavors = flavors_response.json()
        for flavor in flavors["flavors"]:
            if flavor["name"] == flavor_name:
                return flavor["id"]

    def get_network_id(self, network_name):
        """
        Cette commande permet de récupérer l'identifiant d'un réseau.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            network_name: le nom du réseau.

        Returns:
            L'identifiant du réseau.
        """
        # requête pour récupérer la liste des réseaux
        networks_response = httpx.get(
            f"http://{self.ip}:9696/network/v2.0/networks", headers={"X-Auth-Token": self.token}
        )
        networks = networks_response.json()
        for network in networks["networks"]:
            if network["name"] == network_name:
                return network["id"]

    def get_subnet_id(self, subnet_name):
        """
        Cette commande permet de récupérer l'identifiant d'un sous-réseau.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            subnet_name: le nom du sous-réseau.

        Returns:
            L'identifiant du sous-réseau.
        """
        # requête pour récupérer la liste des sous-réseaux
        subnets_response = httpx.get(
            f"http://{self.ip}:9696/network/v2.0/subnets", headers={"X-Auth-Token": self.token}
        )
        subnets = subnets_response.json()
        for subnet in subnets["subnets"]:
            if subnet["name"] == subnet_name:
                return subnet["id"]

    def get_vm_id(self, vm_name):
        """
        Cette commande permet de récupérer l'identifiant d'une machine virtuelle.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            vm_name: le nom de la machine virtuelle.

        Returns:
            L'identifiant de la machine virtuelle.
        """
        # requête pour récupérer la liste des machines virtuelles
        vms_response = httpx.get(
            f"http://{self.ip}:{self.port}/compute/v2.1/servers", headers={"X-Auth-Token": self.token}
        )
        vms = vms_response.json()
        for vm in vms["servers"]:
            if vm["name"] == vm_name:
                return vm["id"]

    def get_vm_ip(self, vm_id):
        """
        Cette commande permet de récupérer l'adresse IP d'une machine virtuelle.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            vm_id: l'identifiant de la machine virtuelle.

        Returns:
            L'adresse IP de la machine virtuelle.
        """
        # requête pour récupérer les informations d'une machine virtuelle
        vm_response = httpx.get(
            f"http://{self.ip}:{self.port}/compute/v2.1/servers/{vm_id}",
            headers={"X-Auth-Token": self.token},
        )
        vm = vm_response.json()
        return vm["server"]["addresses"]["private"][0]["addr"]

    def get_router_id(self, router_name):
        """
        Cette commande permet de récupérer l'identifiant d'un routeur.
        Args:
            ip: l'adresse IP de l'instance OpenStack.
            token: le token d'authentification de l'instance OpenStack.
            router_name: le nom du routeur.

        Returns:
            L'identifiant du routeur.
        """
        # requête pour récupérer la liste des routeurs
        routers_response = httpx.get(
            f"http://{self.ip}:9696/v2.0/network/routers", headers={"X-Auth-Token": self.token}
        )
        routers = routers_response.json()
        for router in routers["routers"]:
            if router["name"] == router_name:
                return router["id"]

    def create_topology(self,
                        blue_network_name,
                        blue_subnet_name,
                        blue_subnet_cidr,
                        blue_vm1_name,
                        red_network_name,
                        red_subnet_name,
                        red_subnet_cidr,
                        red_vm2_name,
                        public_network_name,
                        public_subnet_name,
                        public_subnet_cidr,
                        public_vm3_name,
                        router_name
                        ):
        """
        Cette commande permet de créer une topologie avec 2 réseaux, 2 sous-réseaux, 2 machines virtuelles et 1 routeur.
        Args:
            blue_network_name: le nom du réseau bleu.
            blue_subnet_name: le nom du sous-réseau bleu.
            blue_subnet_cidr: le CIDR du sous-réseau bleu.
            blue_vm1_name: le nom de la machine virtuelle bleue.
            red_network_name: le nom du réseau rouge.
            red_subnet_name: le nom du sous-réseau rouge.
            red_subnet_cidr: le CIDR du sous-réseau rouge.
            red_vm2_name: le nom de la machine virtuelle rouge.
            public_network_name: le nom du réseau public.
            public_subnet_name: le nom du sous-réseau public.
            public_subnet_cidr: le CIDR du sous-réseau public.
            public_vm3_name: le nom de la machine virtuelle publique.
            router_name: le nom du routeur.

        Returns:
            La topologie créée.
        """

        print("Creating networks...")

        # # Create blue network
        print("Created blue network")
        self.create_network(blue_network_name)
        blue_network_id = self.get_network_id(blue_network_name)
        print("Created blue network")

        # Create blue subnet
        print("Created blue subnet")
        self.create_subnet(blue_subnet_name, blue_network_id)
        blue_subnet_id = self.get_subnet_id(blue_subnet_name)


        # Create red network
        print("Created red network")
        self.create_network(red_network_name)
        red_network_id = self.get_network_id(red_network_name)
        print("Created red network")

        # Create red subnet
        print("Created red subnet")
        self.create_subnet(red_subnet_name, red_network_id)
        red_subnet_id = self.get_subnet_id(red_subnet_name)
        print("Created red subnet")

        # Create public network
        print("Created public network")
        self.create_network("public")
        public_network_id = self.get_network_id("public")
        print("Created public network")

        # Create public subnet
        print("Created public subnet")
        self.create_subnet("public", public_network_id)
        public_subnet_id = self.get_subnet_id("public")
        print("Created public subnet")

        print("Creating router...")
        # Create router
        print("Created router")
        self.create_router(router_name, public_network_id)
        router_id = self.get_router_id(router_name)
        print("Created router")

        print("Creating VMs...")

        # Create instance
        image_name = 'cirros-0.5.1-x86_64-disk'
        flavor_name = 'm1.tiny'
        network_name = 'private'


        print("Created blue VM")
        self.create_vm(blue_vm1_name, image_name, flavor_name, blue_network_id)
        blue_vm_id = self.get_vm_id(blue_vm1_name)
        print("Created blue VM")

        # Create red VM
        print("Created red VM")
        self.create_vm(blue_vm1_name, image_name, flavor_name, red_network_id)
        red_vm_id = self.get_vm_id(blue_vm1_name)
        print("Created red VM")

        # Create public VM
        print("Created public VM")
        self.create_vm("public", image_name, flavor_name, public_network_id)
        public_vm_id = self.get_vm_id("public")
        print("Created public VM")

        print("Created topology")


@app.command(
    help="Create a topology with 2 networks, 2 subnets, 2 VMs and 1 router."
)
def create_topology(
    openstack_ip: str = typer.Argument("localhost", help="OpenStack IP address", envvar="OPENSTACK_IP", show_default=True),
    openstack_port: str = typer.Argument("8090", help="OpenStack port", envvar="OPENSTACK_PORT", show_default=True),
    project_name: str = typer.Argument("admin", help="OpenStack project name", envvar="OS_PROJECT_NAME", show_default=True),
    username: str = typer.Argument("admin", help="OpenStack username", envvar="OS_USERNAME", show_default=True),
    password: str = typer.Argument("secret", help="OpenStack password", envvar="OS_PASSWORD", show_default=True),
    blue_network_name: str = typer.Argument("blue", help="Name of the blue network", show_default=True),
    blue_subnet_name: str = typer.Argument("blue_subnet", help="Name of the blue subnet", show_default=True),
    blue_subnet_cidr: str = typer.Argument("10.0.0.0/24", help="CIDR for the blue subnet", show_default=True),
    blue_vm1_name: str = typer.Argument("blue_vm1", help="Name of the first blue VM", show_default=True),
    red_network_name: str = typer.Argument("red", help="Name of the red network", show_default=True),
    red_subnet_name: str = typer.Argument("red_subnet", help="Name of the red subnet", show_default=True),
    red_subnet_cidr: str = typer.Argument("192.168.1.0/24", help="CIDR for the red subnet", show_default=True),
    red_vm2_name: str = typer.Argument("red_vm2", help="Name of the red VM", show_default=True),
    public_network_name: str = typer.Argument("public", help="Name of the public network", show_default=True),
    public_subnet_name: str = typer.Argument("public_subnet", help="Name of the public subnet", show_default=True),
    public_subnet_cidr: str = typer.Argument("172.24.4.0/24", help="CIDR for the public subnet", show_default=True),
    public_vm3_name: str = typer.Argument("public_vm3", help="Name of the second blue VM", show_default=True),
    router_name: str = typer.Argument("router", help="Name of the router", show_default=True),
):
    """
    Cette commande permet de créer une topologie avec 2 réseaux, 2 sous-réseaux, 2 machines virtuelles et 1 routeur.
    Args:
        openstack_ip: l'adresse IP de l'instance OpenStack.
        openstack_port: le port de l'instance OpenStack.
        project_name: le nom du projet OpenStack.
        username: le nom d'utilisateur OpenStack.
        password: le mot de passe OpenStack.
        blue_network_name: le nom du réseau bleu.
        blue_subnet_name: le nom du sous-réseau bleu.
        blue_subnet_cidr: le CIDR du sous-réseau bleu.
        blue_vm1_name: le nom de la première machine virtuelle bleue.
        red_network_name: le nom du réseau rouge.
        red_subnet_name: le nom du sous-réseau rouge.
        red_subnet_cidr: le CIDR du sous-réseau rouge.
        red_vm2_name: le nom de la machine virtuelle rouge.
        public_network_name: le nom du réseau public.
        public_subnet_name: le nom du sous-réseau public.
        public_subnet_cidr: le CIDR du sous-réseau public.
        public_vm3_name: le nom de la machine virtuelle public.
        router_name: le nom du routeur.
        """
    openstack = OpenStack(openstack_ip, openstack_port, project_name, username, password)
    openstack.list_projects()
    openstack.list_users()
    openstack.list_vms()
    openstack.list_flavors()
    openstack.list_images()
    # openstack.list_networks()
    # openstack.list_subnets()
    # openstack.list_routers()
    # print("Creating topology...")
    # openstack.create_topology(
    #     blue_network_name,
    #     blue_subnet_name,
    #     blue_subnet_cidr,
    #     blue_vm1_name,
    #     red_network_name,
    #     red_subnet_name,
    #     red_subnet_cidr,
    #     red_vm2_name,
    #     public_network_name,
    #     public_subnet_name,
    #     public_subnet_cidr,
    #     public_vm3_name,
    #     router_name,
    # )

if __name__ == "__main__":
    app()