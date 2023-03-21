import pytest
from unittest.mock import patch, Mock
import os

from src.openstack_api import auth_openstack, list_users, list_vms

@pytest.fixture
def mocked_response_user():
    """Crée une réponse mockée."""
    response_mock = Mock()
    response_mock.json.return_value = {"users": [{"name": "John"}, {"name": "Jane"}]}
    response_mock.headers = {"X-Subject-Token": "token"}
    return response_mock

@pytest.fixture
def mocked_response_vm():
    """Crée une réponse mockée."""
    response_mock = Mock()
    response_mock.json.return_value = {
        "servers": [
            {"name": "server1"},
            {"name": "server2"},
        ]
    }
    response_mock.headers = {"X-Subject-Token": "token"}
    return response_mock

@patch("httpx.post")
def test_auth_openstack(mock_post, mocked_response_user):
    """Teste la fonction auth_openstack."""
    mock_post.return_value = mocked_response_user

    token = auth_openstack(ip="localhost", port="8092", username="admin", password="openstack", name="admin")

    mock_post.assert_called_once()
    assert token == "token"
    assert "OPENSTACK_TOKEN" in os.environ

@patch("httpx.get")
def test_list_users(mock_get, mocked_response_user):
    """Teste la fonction list_users."""
    mock_get.return_value = mocked_response_user

    list_users(ip="localhost", port="8092", token="token")

    mock_get.assert_called_once()
    mocked_response_user.json.assert_called_once_with()
    assert mocked_response_user.json()["users"][0]["name"] == "John"
    assert mocked_response_user.json()["users"][1]["name"] == "Jane"

@patch("httpx.get")
def test_list_vms(mock_get, mocked_response_vm):
    """Teste la fonction list_vms."""
    mock_get.return_value = mocked_response_vm

    list_vms(ip="localhost", port="8092", token="token")

    mock_get.assert_called_once()
    mocked_response_vm.json.assert_called_once_with()
    assert mocked_response_vm.json()["servers"][0]["name"] == "server1"
    assert mocked_response_vm.json()["servers"][1]["name"] == "server2"
