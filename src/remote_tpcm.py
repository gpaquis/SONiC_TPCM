import json
import argparse
import ast
import requests
import configparser
import ipaddress
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def validate_ip_address(ip_string) -> bool:
    try:
      ip_object = ipaddress.ip_address(ip_string)
      return True
    except ValueError:
      return False


def tpcm_list(switch_ip: str, user_name: str, password: str) -> str:
    """
        List all TPCM installed
        no value, list all TPCM in each VRF
    """


    request_data = {
        "openconfig-tpcm:input": {
        }
    }

    #print(json.dumps(request_data))
    try:
       response = requests.post(url=f"https://{switch_ip}/restconf/operations/openconfig-tpcm:tpcm-list",
                                data=json.dumps(request_data),
                                headers={'Content-Type': 'application/yang-data+json'},
                                auth=HTTPBasicAuth(f"{user_name}", f"{password}"),
                                verify=False
                                )
       response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        #print(f'{response}')
        return response.content

def tpcm_remove(switch_ip: str, user_name: str, password: str) -> str:
    """
        Remove a TPCM installed
        Get value from the remote_tpcm.conf
    """

    config = configparser.ConfigParser()
    config.read('remote_tpcm.conf')

    docker_name = config['TPCM1']['docker-name']

    request_data = {
        "openconfig-tpcm:input": {
           "clean-data": "yes",
           "docker-name": docker_name
        }
    }

    #print(json.dumps(request_data))
    try:
       response = requests.post(url=f"https://{switch_ip}/restconf/operations/openconfig-tpcm:tpcm-uninstall",
                                data=json.dumps(request_data),
                                headers={'Content-Type': 'application/yang-data+json'},
                                auth=HTTPBasicAuth(f"{user_name}", f"{password}"),
                                verify=False
                                )
       response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        #print(f'{response}')
        return response.content


def tpcm_install(switch_ip: str, user_name: str, password: str) -> str:
    """
        Install TPCM
        Read from a config file, here the container install from DockerHUB
        [TPCM1]
        docker-name = "str",
        image-source = "str",
        image-name = "str/str:str",
        args = "str"

        Image-source must be set with "pull" if container is locate on the dockerhub, otherwise use http/https/usb/sftp/ssh
    """

    config = configparser.ConfigParser()
    config.read('remote_tpcm.conf')

    docker_name = config['TPCM1']['docker-name']
    image_source = config['TPCM1']['image-source']
    image_name = config['TPCM1']['image-name']
    tpcm_args = config['TPCM1']['args']

    request_data = {
        "openconfig-tpcm:input": {
           "docker-name": docker_name,
           "image-source": image_source,
           "image-name": image_name,
           "args": tpcm_args
        }
    }

    #print(json.dumps(request_data))
    try:
       response = requests.post(url=f"https://{switch_ip}/restconf/operations/openconfig-tpcm:tpcm-install",
                                data=json.dumps(request_data),
                                headers={'Content-Type': 'application/yang-data+json'},
                                auth=HTTPBasicAuth(f"{user_name}", f"{password}"),
                                verify=False
                                )
       response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        #print(f'{response}')
        return response.content

def tpcm_upgrade(switch_ip: str, user_name: str, password: str) -> str:
    """
        Upgrade TPCM
        Read from a config file, here the container install from DockerHUB
        [TPCM1]
        docker-name = "str",
        image-source = "str",
        image-name = "str/str:str",
        args = "str"

        Image-source must be set with "pull" if container is locate on the dockerhub, otherwise use http/https/usb/sftp/ssh
    """

    config = configparser.ConfigParser()
    config.read('remote_tpcm.conf')

    docker_name = config['TPCM1']['docker-name']
    image_source = config['TPCM1']['image-source']
    image_name = config['TPCM1']['image-name']
    tpcm_args = config['TPCM1']['args']
    skip_data = config['TPCM1']['skip-data-migration']

    request_data = {
        "openconfig-tpcm:input": {
           "docker-name": docker_name,
           "image-source": image_source,
           "image-name": image_name,
           "args": tpcm_args,
           "skip-data-migration": skip_data
        }
    }

    #print(json.dumps(request_data))
    try:
       response = requests.post(url=f"https://{switch_ip}/restconf/operations/openconfig-tpcm:tpcm-upgrade",
                                data=json.dumps(request_data),
                                headers={'Content-Type': 'application/yang-data+json'},
                                auth=HTTPBasicAuth(f"{user_name}", f"{password}"),
                                verify=False
                                )
       response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        #print(f'{response}')
        return response.content


def main():
    parser = argparse.ArgumentParser(description='Remote TPCM tools')
    parser.add_argument("--action", help="action type supported Install/Remove/List", type=str)
    parser.add_argument("--switch_ip", help="IP address of the switch to automate", type=str)
    parser.add_argument("--sonic_username", help="SONiC Login", type=str)
    parser.add_argument("--sonic_password", help="SONiC Password", type=str)
    args = parser.parse_args()

    action = args.action

    switch_ip = args.switch_ip

    if validate_ip_address(switch_ip) == True:

       sonic_username = args.sonic_username
       sonic_password = args.sonic_password

       if action == "List":
        result = tpcm_list(switch_ip=switch_ip, user_name=sonic_username, password=sonic_password)
        print(f'{result}')

       if action == "Install":
        result = tpcm_install(switch_ip=switch_ip, user_name=sonic_username, password=sonic_password)
        print(f'{result}')

       if action == "Remove":
        result = tpcm_remove(switch_ip=switch_ip, user_name=sonic_username, password=sonic_password)
        print(f'{result}')
     
       if action == "Upgrade":
        result = tpcm_upgrade(switch_ip=switch_ip, user_name=sonic_username, password=sonic_password)
        print(f'{result}')
    
    else:
      print("IP address is not valid\r\nUse tpcm_remote.py -h for Help")


if __name__ == '__main__':
    main()
