import httpx
import typer
from rich.progress import track
import os

app = typer.Typer()


@app.command(help="Authentifie l'instance OpenStack.")
def auth_openstack(
    ip: str = typer.Argument(
        "localhost",
        help="OpenStack IP address",
        envvar="OPENSTACK_IP",
        show_default=True,
    ),
    port: str = typer.Argument(
        "8092",
        help="OpenStack port",
        envvar="OPENSTACK_PORT",
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
        show_default=True
    ),
    name: str = typer.Argument(
        "admin",
        help="OpenStack project name",
        envvar="OS_PROJECT_NAME",
        show_default=True
    ),
):
    """Authentifie l'instance OpenStack.
    Args:
        ip: l'adresse IP de l'instance OpenStack.
        username: le nom de l'administrateur.
        password: le mot de passe de l'administrateur.
        name: le nom du projet.

    Returns:
        Le token d'authentification de l'instance OpenStack.
    """
    # Set the URL for the authentication API endpoint
    url = f"http://{ip}:{port}/v3/auth/tokens"

    # Set the headers for the API request
    headers = {
        "Content-Type": "application/json",
    }

    # Set the body of the API request
    data = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": username,
                        "domain": {"id": "default"},
                        "password": password,
                    }
                },
            },
            "scope": {"project": {"name": name, "domain": {"id": "default"}}},
        }
    }
    # Send the API request and get the response
    response = httpx.post(url, headers=headers, json=data)

    # save token into environment variable
    os.environ["OPENSTACK_TOKEN"] = response.headers.get("X-Subject-Token")

    return response.headers.get("X-Subject-Token")


@app.command(
    help="Récupère la liste des utilisateurs à partir d'un endpoint OpenStack."
)
def list_users(
    ip: str = typer.Argument(
        "localhost",
        help="OpenStack IP address",
        envvar="OPENSTACK_IP",
        show_default=True,
    ),
    port: str = typer.Argument(
        "8092",
        help="OpenStack port",
        envvar="OPENSTACK_PORT",
        show_default=True,
    ),
    token: str = typer.Argument(
        "openstack",
        help="OpenStack token",
        envvar="OPENSTACK_TOKEN",
        show_default=True,
    ),
):
    """
    Récupère la liste des utilisateurs à partir d'un endpoint OpenStack.
    """
    # requête pour récupérer la liste des utilisateurs
    url = f"{ip}:{port}/v3/users"
    headers = {"X-Auth-Token": token}
    response = httpx.get(url, headers=headers)
    users = response.json()["users"]

    print("Liste des utilisateurs :")
    for user in track(users, description="Récupération des utilisateurs"):
        print(user["name"])


@app.command(help="Liste les instances virtuelles d'une instance OpenStack.")
def list_vms(
    ip: str = typer.Argument(
        "localhost:8092",
        help="OpenStack IP address",
        envvar="OPENSTACK_IP",
        show_default=True,
    ),
    port : str = typer.Argument(
        "8092",
        help="OpenStack port",
        envvar="OPENSTACK_PORT",
        show_default=True,
    ),
    token: str = typer.Argument(
        "openstack",
        help="OpenStack token",
        envvar="OS_TOKEN",
        show_default=True,
    ),
):
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
        f"http://{ip}:{port}/compute/v2.1/servers", headers={"X-Auth-Token": token}
    )
    vms = vms_response.json()
    typer.echo("Liste des machines virtuelles :")
    for vm in track(vms, description="Récupération des machines virtuelles"):
        typer.echo(vm[0])

@app.command(help="Liste les instances virtuelles d'une instance OpenStack.")
def list_networks(
    ip: str = typer.Argument(
        "localhost:8092",
        help="OpenStack IP address",
        envvar="OPENSTACK_IP",
        show_default=True,
    ),
    port : str = typer.Argument(
        "8092",
        help="OpenStack port",
        envvar="OPENSTACK_PORT",
        show_default=True,
    ),
    token: str = typer.Argument(
        "openstack",
        help="OpenStack token",
        envvar="OS_TOKEN",
        show_default=True,
    ),
):
    """
    Cette commande permet de récupérer la liste des réseaux d'une instance OpenStack.
    Args:
        ip: l'adresse IP de l'instance OpenStack.
        token: le token d'authentification de l'instance OpenStack.

    Returns:
        La liste des réseaux de l'instance OpenStack.
    """
    # requête pour récupérer la liste des réseaux
    networks_response = httpx.get(
        f"http://{ip}:{port}/network/v2.0/networks", headers={"X-Auth-Token": token}
    )
    networks = networks_response.json()["networks"]
    typer.echo("Liste des réseaux :")
    for network in track(networks, description="Récupération des réseaux"):
        typer.echo(network["name"])

@app.command(help="Liste les instances subnet  d'une instance OpenStack.")
def list_subnets(
    ip: str = typer.Argument(
        "localhost:8092",
        help="OpenStack IP address",
        envvar="OPENSTACK_IP",
        show_default=True,
    ),
    port : str = typer.Argument(
        "8092",
        help="OpenStack port",
        envvar="OPENSTACK_PORT",
        show_default=True,
    ),
    token: str = typer.Argument(
        "openstack",
        help="OpenStack token",
        envvar="OS_TOKEN",
        show_default=True,
    ),
):
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
        f"http://{ip}:{port}/network/v2.0/subnets", headers={"X-Auth-Token": token}
    )
    subnets = subnets_response.json()["subnets"]
    typer.echo("Liste des sous-réseaux :")
    for subnet in track(subnets, description="Récupération des sous-réseaux"):
        typer.echo(subnet["name"])


