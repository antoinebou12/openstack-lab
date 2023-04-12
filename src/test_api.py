import pytest
from unittest.mock import patch
from src.script1 import create_topology, OpenStack


@patch('httpx.post')
def test_auth_openstack(mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.headers = {'X-Subject-Token': 'fake_token'}

    openstack = OpenStack('10.0.0.1', '5000', 'test', 'user', 'pass')
    assert openstack.token == 'fake_token'


@patch('httpx.post')
@patch('httpx.get')
def test_list_users(mock_get, mock_post):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'users': [{'name': 'test_user_1'}, {'name': 'test_user_2'}]}
    mock_post.return_value.status_code = 201
    mock_post.return_value.headers = {'X-Subject-Token': 'fake_token'}

    openstack = OpenStack('10.0.0.1', '5000', 'test', 'user', 'pass')
    users = openstack.list_users()

    assert len(users) == 2
    assert users[0]['name'] == 'test_user_1'
    assert users[1]['name'] == 'test_user_2'


@patch('httpx.post')
@patch('httpx.get')
def test_list_networks(mock_get, mock_post):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'networks': [{'name': 'test_network_1', 'id': 'network_1_id'},
                                                            {'name': 'test_network_2', 'id': 'network_2_id'}]}
    mock_post.return_value.status_code = 201
    mock_post.return_value.headers = {'X-Subject-Token': 'fake_token'}

    openstack = OpenStack('10.0.0.1', '5000', 'test', 'user', 'pass')
    networks = openstack.list_networks()

    assert len(networks['networks']) == 2
    assert networks['networks'][0]['name'] == 'test_network_1'
    assert networks['networks'][0]['id'] == 'network_1_id'
    assert networks['networks'][1]['name'] == 'test_network_2'
    assert networks['networks'][1]['id'] == 'network_2_id'


@patch('httpx.post')
@patch('httpx.get')
def test_list_subnets(mock_get, mock_post):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'networks': [{'name': 'test_network_1', 'id': 'network_1_id', 'subnets': ['subnet_1_id']},
                                                            {'name': 'test_network_2', 'id': 'network_2_id', 'subnets': ['subnet_1_id', 'subnet_2_id']}]}
    mock_post.return_value.status_code = 201
    mock_post.return_value.headers = {'X-Subject-Token': 'fake_token'}

    openstack = OpenStack('10.0.0.1', '5000', 'test', 'user', 'pass')
    subnets = openstack.list_subnets()

    assert len(subnets) == 3
    print(subnets)
    assert subnets[0]['network_id'] == 'network_1_id'
    assert subnets[0]['subnets'][0] == 'subnet_1_id'
    assert subnets[1]['network_id'] == 'network_2_id'
    assert subnets[1]['subnets'][0] == 'subnet_1_id'
    assert subnets[1]['subnets'][1] == 'subnet_2_id'
