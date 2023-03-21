#!/usr/bin/env python

import openstack
import typer
from rich.progress import track

app = typer.Typer()

@app.command(
    help="Create a topology with 2 networks, 2 subnets, 2 VMs and 1 router."
)
def create_topology(
    openstack_ip: str = typer.Argument("localhost", help="OpenStack IP address", envvar="OPENSTACK_IP", show_default=True),
    openstack_port: str = typer.Argument("8092", help="OpenStack port", envvar="OPENSTACK_PORT", show_default=True),
    project_name: str = typer.Argument("admin", help="OpenStack project name", envvar="OS_PROJECT_NAME", show_default=True),
    username: str = typer.Argument("admin", help="OpenStack username", envvar="OS_USERNAME", show_default=True),
    password: str = typer.Argument("openstack", help="OpenStack password", envvar="OS_PASSWORD", show_default=True),
    blue_network_name: str = typer.Option("blue", help="Name of the blue network", show_default=True),
    blue_subnet_name: str = typer.Option("blue_subnet", help="Name of the blue subnet", show_default=True),
    blue_subnet_cidr: str = typer.Option("10.0.0.0/24", help="CIDR for the blue subnet", show_default=True),
    blue_vm1_name: str = typer.Option("blue_vm1", help="Name of the first blue VM", show_default=True),
    red_network_name: str = typer.Option("red", help="Name of the red network", show_default=True),
    red_subnet_name: str = typer.Option("red_subnet", help="Name of the red subnet", show_default=True),
    red_subnet_cidr: str = typer.Option("192.168.1.0/24", help="CIDR for the red subnet", show_default=True),
    red_vm2_name: str = typer.Option("red_vm2", help="Name of the red VM", show_default=True),
    public_network_name: str = typer.Option("public", help="Name of the public network", show_default=True),
    public_subnet_name: str = typer.Option("public_subnet", help="Name of the public subnet", show_default=True),
    public_subnet_cidr: str = typer.Option("172.24.4.0/24", help="CIDR for the public subnet", show_default=True),
    public_vm3_name: str = typer.Option("public_vm3", help="Name of the second blue VM", show_default=True),
    router_name: str = typer.Option("router", help="Name of the router", show_default=True),
    conn: openstack.connection.Connection = typer.Option(None, help="OpenStack connection"),
):

    if conn is None:
        # Create connection to OpenStack
        conn = openstack.connect(
            auth_url=f"http://{openstack_ip}:{openstack_port}/v3",
            project_name=project_name,
            username=username,
            password=password,
        )

    # Create blue network
    blue_network = conn.network.create_network(name=blue_network_name)
    blue_subnet = conn.network.create_subnet(
        name=blue_subnet_name, network_id=blue_network.id, cidr=blue_subnet_cidr
    )

    # Create red network
    red_network = conn.network.create_network(name=red_network_name)
    red_subnet = conn.network.create_subnet(
        name=red_subnet_name, network_id=red_network.id, cidr=red_subnet_cidr
    )

    # Create public network
    public_network = conn.network.create_network(name=public_network_name)
    public_subnet = conn.network.create_subnet(
        name=public_subnet_name, network_id=public_network.id, cidr=public_subnet_cidr
    )

    # Create instance
    image_name = 'cirros-0.5.1-x86_64-disk'
    flavor_name = 'm1.tiny'
    network_name = 'private'

    image = conn.compute.find_image(image_name)
    flavor = conn.compute.find_flavor(flavor_name)
    network = conn.network.find_network(network_name)

    blue_vm1 = conn.compute.create_server(
        name= blue_vm1_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": blue_network.id}]
    )

    # wait for instance to be ready
    conn.compute.wait_for_server(blue_vm1)

    # Get instance details
    blue_vm1_instance = conn.compute.get_server(blue_vm1)
    print('blue_vm1 address:', blue_vm1_instance.accessIPv4)


    red_vm2 = conn.compute.create_server(
        name= red_vm2_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": red_network.id}]
    )

    # wait for instance to be ready
    conn.compute.wait_for_server(red_vm2)

    # Get instance details
    red_vm2_instance = conn.compute.get_server(red_vm2)
    print('red_vm2 IP address:', red_vm2_instance.accessIPv4)

    public_vm3 = conn.compute.create_server(
        name= public_vm3_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": public_network.id}]
    )

    # wait for instance to be ready
    conn.compute.wait_for_server(public_vm3)

    # Get instance details
    public_vm3_instance = conn.compute.get_server(public_vm3)
    print('public_vm3 IP address:', public_vm3_instance.accessIPv4)

    # Create router
    router = conn.network.create_router(name=router_name, external_gateway_info={"network_id": public_network.id})
    conn.network.add_interface_to_router(router, red_subnet.id)
    conn.network.add_interface_to_router(router, blue_subnet.id)

    # Create floating IP
    floating_ip = conn.network.create_ip(floating_network_id=public_network.id)
    print('Floating IP:', floating_ip.floating_ip_address)

    # Associate floating IP to VM
    conn.compute.add_floating_ip_to_server(blue_vm1, floating_ip.floating_ip_address)

    # Create security group
    security_group = conn.network.create_security_group(name="security_group")

    # Create security group rule
    security_group_rule_ssh = conn.network.create_security_group_rule(
        security_group_id=security_group.id,
        direction="ingress",
        ethertype="IPv4",
        protocol="tcp",
        port_range_min=22,
        port_range_max=22,
    )

    security_group_rule_ping = conn.network.create_security_group_rule(
        security_group_id=security_group.id,
        direction="ingress",
        ethertype="IPv4",
        protocol="icmp",
    )

    # Add security group to VM
    conn.compute.add_security_group_to_server(blue_vm1, security_group.id)

    # Create keypair
    keypair = conn.compute.create_keypair(name="keypair")

    # Create keypair file
    with open("keypair.pem", "w") as f:
        f.write(f"{keypair.private_key}")

    # add keypair to VM
    conn.compute.add_keypair_to_server(blue_vm1, keypair.name)