import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define constants using environment variables
OPENSTACK_IP = os.getenv("OPENSTACK_IP")
OPENSTACK_PORT = os.getenv("OPENSTACK_PORT")
BLUE_NETWORK_NAME = os.getenv("BLUE_NETWORK_NAME")
BLUE_SUBNET_NAME = os.getenv("BLUE_SUBNET_NAME")
BLUE_SUBNET_CIDR = os.getenv("BLUE_SUBNET_CIDR")
BLUE_VM1_NAME = os.getenv("BLUE_VM1_NAME")
BLUE_VM2_NAME = os.getenv("BLUE_VM2_NAME")
RED_NETWORK_NAME = os.getenv("RED_NETWORK_NAME")
RED_SUBNET_NAME = os.getenv("RED_SUBNET_NAME")
RED_SUBNET_CIDR = os.getenv("RED_SUBNET_CIDR")
RED_VM3_NAME = os.getenv("RED_VM3_NAME")
PUBLIC_NETWORK_NAME = os.getenv("PUBLIC_NETWORK_NAME")
PUBLIC_SUBNET_NAME = os.getenv("PUBLIC_SUBNET_NAME")
PUBLIC_SUBNET_CIDR = os.getenv("PUBLIC_SUBNET_CIDR")
KEYSTONE_URL = os.getenv("KEYSTONE_URL")
NOVA_URL = os.getenv("NOVA_URL")