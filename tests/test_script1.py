import pytest
from unittest import mock
from openstack.exceptions import SDKException

from src.script1 import create_topology


def test_create_topology_success():
    """Test the create_topology function with mocked data."""
    # Mock the OpenStack connection object
    conn_mock = mock.MagicMock()

    # Mock the create_network and create_subnet methods to return dummy data
    conn_mock.network.create_network.return_value = mock.MagicMock(id='blue_network_id')
    conn_mock.network.create_subnet.return_value = mock.MagicMock(id='blue_subnet_id')
    conn_mock.network.create_network.return_value = mock.MagicMock(id='red_network_id')
    conn_mock.network.create_subnet.return_value = mock.MagicMock(id='red_subnet_id')
    conn_mock.network.create_network.return_value = mock.MagicMock(id='public_network_id')
    conn_mock.network.create_subnet.return_value = mock.MagicMock(id='public_subnet_id')

    # Mock the find_image, find_flavor, and find_network methods to return dummy data
    conn_mock.compute.find_image.return_value = mock.MagicMock(id='image_id')
    conn_mock.compute.find_flavor.return_value = mock.MagicMock(id='flavor_id')
    conn_mock.network.find_network.return_value = mock.MagicMock(id='private_network_id')

    # Mock the create_server method to return dummy data
    conn_mock.compute.create_server.return_value = mock.MagicMock(id='server_id')

    # Call the function with mocked data
    create_topology(
        conn=conn_mock,
        blue_network_name='blue',
        blue_subnet_name='blue_subnet',
        blue_subnet_cidr='10.0.0.0/24',
        blue_vm1_name='blue_vm1',
        red_network_name='red',
        red_subnet_name='red_subnet',
        red_subnet_cidr='192.168.1.0/24',
        red_vm2_name='red_vm3',
        public_network_name='public',
        public_subnet_name='public_subnet',
        public_subnet_cidr='172.24.4.0/24',
        public_vm3_name='blue_vm2',
    )

    # Assert that the expected methods were called with the expected arguments
    conn_mock.network.create_network.assert_any_call(name='blue')
    conn_mock.network.create_subnet.assert_any_call(
        name='blue_subnet', network_id='blue_network_id', cidr='10.0.0.0/24'
    )
    conn_mock.network.create_network.assert_any_call(name='red')
    conn_mock.network.create_subnet.assert_any_call(
        name='red_subnet', network_id='red_network_id', cidr='192.168.1.0/24'
    )
    conn_mock.network.create_network.assert_any_call(name='public')
    conn_mock.network.create_subnet.assert_any_call(
        name='public_subnet', network_id='public_network_id', cidr='172.24.4.0/24'
    )
    conn_mock.compute.find_image.assert_called_once_with('cirros-0.5.1-x86_64-disk')
    conn_mock.compute.find_flavor.assert_called_once_with('m1.tiny')
    conn_mock.network.find_network.assert_called_once_with('private')
    conn_mock.compute.create_server.assert_any_call(
        name='blue_vm1',
        image_id='image_id',
        flavor_id='flavor_id',
        networks=[{'uuid': 'blue_network_id'}]
    )
    conn_mock.compute.create_server.assert_any_call(
        name='red_vm2',
        image_id='image_id',
        flavor_id='flavor_id',
        networks=[{'uuid': 'red_network_id'}]
    )
    conn_mock.compute.create_server.assert_any_call(
        name='public_vm3',
        image_id='image_id',
        flavor_id='flavor_id',
        networks=[{'uuid': 'public_network_id'}]
    )

def test_create_topology_failure():
    """Test the create_topology function with mocked data."""
    # Mock the OpenStack connection object
    conn_mock = mock.MagicMock()

    # # Mock the create_network and create_subnet methods to raise an exception
    # conn_mock.network.create_network.side_effect = SDKException
    # conn_mock.network.create_subnet.side_effect = SDKException

    # # Call the function with mocked data
    # with pytest.raises(SDKException):
    #     create_topology(
    #         conn=conn_mock,
    #         blue_network_name='blue',
    #         blue_subnet_name='blue_subnet',
    #         blue_subnet_cidr='