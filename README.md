# Remote TPCM tools for Dell Enterprise SONiC

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](#-how-to-contribute)
[![License](https://img.shields.io/badge/license-GPL-blue.svg)](https://github.com/gpaquis/SONiC_TPCM/blob/main/License.md)
[![GitHub issues](https://img.shields.io/github/issues/gpaquis/SONIC_TPCM)](https://github.com/gpaquis/SONiC_TPCM/issues)

Built and maintained by [Gerald PAQUIS](https://github.com/gpaquis) and [Contributors](https://github.com/gpaquis/SONiC_TPCM/graphs/contributors)

--------------------
This Repo contains a Python script for manipulate remotly TPCM (ThirdPartyContainerManager) by using REST-API, and a config file

## Contents

- [Description and Objective](#-description-and-objective)
- [Requirements](#-requirements)
- [Usage and Configuration](#Usage-and-Configuration)
- [Roadmap](#Roadmap)
- [How to Contribute](#-how-to-contribute)

## 🚀 Description and Objective

The remote_tpcm script allow to deploy, remove and list container install on a Dell Enterprise SONiC. <br />
This script is for purpose test only and explain howto deploy remotely, a container from a DockerHub Source.

## 📋 Requirements
- Python 3.8.10 version minimum 

## 🏁 Usage and Configuration
Before start, the remote_tpcm.conf must be configure. <br />
The config file must be in the same repository as remote_tpcm.py <br />
The remote_tpcm.conf(https://github.com/gpaquis/SONiC_TPCM/blob/main/src/remote_tpcm.conf) contain entry to deploy the container from DockerHub.

TPCM support deployment via HTTP/HTTPS/SFTP/SSH/USB, but this script don't support this deployment methode.<br />
See [Roadmap](#Roadmap) for more details and next feature.

**Runing the script and options:**

| Options         | Value       | Description                                 | Mandatory |
|-----------------|-------------|---------------------------------------------|-----------|
|                 | List        | List TPCM install on DES                    |           |
|--action         | Install     | Install TPCM on DES                         |   Yes     |
|                 | Remove      | Remove TPCM from DES                        |           |
|                 | Upgrade     | Upgrade TPCM                                |           |
|--switch_ip      | IPV4        | IP address of the DES management interface  |   Yes     |
|--sonic_username | type string | Login used to access to the DES             |   Yes     |
|--sonic_password | type string | Password used to access to the DES          |   Yes     |


  `python3 remote_tpcm.py --action [List|Install|Remove|Uprade] --switch_ip 192.168.101.101 --sonic_username admin --sonic_password YourPaSsWoRd`

## 📅 Roadmap
Add Update process for memory/storage assing to the TPCM <br />
Add support for http/https/ssh/scp. <br />
Allow to deploy more than one container at same time. <br />


## 👏 How to Contribute
We welcome contributions to the project.
