# Openstack-lab

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Poetry](https://img.shields.io/badge/poetry-1.1.4-blue.svg)](https://python-poetry.org/docs/)
[![Openstack](https://img.shields.io/badge/openstack-queens-blue.svg)](https://docs.openstack.org/queens/)
[![VirtualBox](https://img.shields.io/badge/virtualbox-6.1-blue.svg)](https://www.virtualbox.org/wiki/Downloads)

## Introduction

Openstack-lab is a project that creates a virtual network infrastructure using Openstack's RESTful APIs. The project's objective is to create three virtual machines capable of communicating with each other via pings.

https://www.dropbox.com/s/gqr7xtz28fpzztb/DevStackOVSFinal-W2019.ova?dl=0

https://ena.etsmtl.ca/pluginfile.php/1656895/mod_resource/content/11/GTI778-Labo2-V01-OpenStack.pdf

Network: BLUE
Subnet 10.0.0.0/24

VM1

Network: RED
Subnet 192.168.1.0/24

VM2

Public Network
Subnet 172.24.4.0/24

VM3

## Requirements

To use this project, you need to have the following:

* Openstack DevStack installation
* Python3
* VirtualBox

## Installation

To get started with the project, perform the following steps:

1. Download and install VirtualBox from the official website.
2. Clone the repository.
3. Install the required dependencies using the following command:

```shell
pip install -r requirements.txt
```

4. Install poetry using the following command:

```shell
pip install poetry
```
## Script 1

This script takes the DevStack VM IP address as input and creates the required topology. The script uses shell scripting and the `curl` command to send HTTP RESTful API requests. The created VMs should be able to communicate with each other via pings.

### Script 2

This script takes the DevStack VM IP address as input and displays the state (active or inactive) of the network, virtual machines, and router interfaces. The output format of the script is JSON.

## Assumptions and Directives

Before working on the scripts, please consider the following assumptions and directives:

* Script 1:
  * There are no existing public networks or routers in the Openstack environment.
  * The script must be able to retrieve a token and use it to execute curl commands.
  * A security group called "default" already exists in the project with basic transfer rules (only IP traffic is allowed; no ICMP rules).
  * The project and user "admin" exist in the environment, and the password is "secret".
* All virtual machines must use the flavor "m1.nano" and the existing image in the DevStack VM.
* All identifiers (token, virtual machine, links, or others) may change from one environment to another. Therefore, make sure not to hardcode them into your scripts.

## Conclusion

This project provides a straightforward approach to creating a virtual network infrastructure using Openstack's RESTful APIs. The project's two scripts enable users to create the required topology and display the state of the network, virtual machines, and router interfaces.
