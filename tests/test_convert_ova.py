import os
import pytest
import subprocess
from typer.testing import CliRunner

from src.scripts.convert_ova import vagrant, docker, app


@pytest.fixture
def runner():
    return CliRunner()


def test_vagrant(runner):
    with runner.isolated_filesystem():
        # Create a mock virtual machine with VBoxManage
        subprocess.run(["VBoxManage", "createvm", "--name", "test_vm", "--register"])
        # Create a mock OVA file
        subprocess.run(["touch", "test_box.ova"])
        # Run the Vagrant command and check for successful execution
        result = runner.invoke(app, ["vagrant", "--vmid", "test_vm", "--boxname", "test_box"])
        assert result.exit_code == 0
        # Check that the Vagrant box was successfully created
        assert os.path.isfile("test_box.box")
        # Check that the Vagrant box was successfully added
        result = runner.invoke(app, ["vagrant", "box", "list"])
        assert "test_box" in result.output


def test_docker(runner):
    with runner.isolated_filesystem():
        # Create a mock OVA file
        subprocess.run(["touch", "test_image.ova"])
        # Run the Docker command and check for successful execution
        result = runner.invoke(app, ["docker", "--image", "test_image", "--nom_image", "test_image_docker"])
        assert result.exit_code == 0
        # Check that the Docker image was successfully imported
        result = subprocess.run(["docker", "images"], capture_output=True)
        assert "test_image_docker" in result.stdout.decode("utf-8")
