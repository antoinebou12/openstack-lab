# Openstack-lab Readme

## Introduction

Openstack-lab is a project that creates a virtual network infrastructure using Openstack's RESTful APIs. The project's objective is to create three virtual machines capable of communicating with each other via pings.

https://www.dropbox.com/s/gqr7xtz28fpzztb/DevStackOVSFinal-W2019.ova?dl=0


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

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">pip install -r requirements.txt
</code></div></div></pre>

4. Install poetry using the following command:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">pip install poetry
</code></div></div></pre>

## Scripts

The project has two scripts:

### Script 1

This script takes the DevStack VM IP address as input and creates the required topology. The script uses shell scripting and the `curl` command to send HTTP RESTful API requests. The created VMs should be able to communicate with each other via pings.

### Script 2

This script takes the DevStack VM IP address as input and displays the state (active or inactive) of the network, virtual machines, and router interfaces. The output format of the script is JSON.

## Assumptions and Directives

Please consider the following assumptions and directives before working on the scripts:

* Script 1:
  * There are no existing public networks or routers in the Openstack environment.
  * The script must be able to retrieve a token and use it to execute curl commands.
  * It is assumed that a security group called "default" already exists in the project with basic transfer rules (only IP traffic is allowed; no ICMP rules).
  * The project and user "admin" exist in the environment, and the password is "secret".
* All virtual machines must use the flavor "m1.nano" and the existing image in the DevStack VM.
* All identifiers (token, virtual machine, links, or others) may change from one environment to another. Therefore, make sure not to code them into your scripts (hardcode) or the identifiers (virtual machines or others), nor the token.

## Conclusion

This project provides a straightforward approach to creating a virtual network infrastructure using Openstack's RESTful APIs. The project's two scripts enable users to create the required topology and display the state of the network, virtual machines, and router interfaces.
