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

def read_config():

    tpcmlist = dict()
    tpcmreturn = []
    config = configparser.ConfigParser()
    config.read('remote_tpcm.conf')

    for each_section in config.sections():
      for (each_key, each_val) in config.items(each_section):
          if each_key == "docker-name":
              tpcmlist.update({each_section : each_val})
    print (f'{tpcmlist}')
    myanswer = input('Enter TPCM id (ex: TPCM1) or ALL:')
    if myanswer.lower() != "all":
     tpcmreturn.append(myanswer.upper())
     #print (f'install: {myanswer}')
     return tpcmreturn
    else:
        for each_section in tpcmlist:
         #print (f'{each_section}')
         tpcmreturn.append(each_section)
        return tpcmreturn


def tpcm_list(remote_sw):
    """
        List all TPCM installed
        no value, list all TPCM in each VRF
    """

    switch_ip = remote_sw['switch_ip']
    user_name = remote_sw['sonic_username']
    password = remote_sw['sonic_password']

    request_data = {
        "openconfig-tpcm:input": {
        }
    }

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
        mystatus = json.loads(response.content)
        myreturn = mystatus["openconfig-tpcm:output"]["status-detail"]
        return myreturn

def tpcm_remove(remote_sw,remove_container) -> str:
    """
        Remove a TPCM installed
        Get value from the remote_tpcm.conf
    """

    switch_ip = remote_sw['switch_ip']
    user_name = remote_sw['sonic_username']
    password = remote_sw['sonic_password']

    mycontainer = remove_container

    config = configparser.ConfigParser()
    config.read('remote_tpcm.conf')

    docker_name = config[f"{mycontainer}"]['docker-name']

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


def tpcm_install(remote_sw,install_container) -> str:
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

    switch_ip = remote_sw['switch_ip']
    user_name = remote_sw['sonic_username']
    password = remote_sw['sonic_password']
    mycontainer = install_container

    config = configparser.ConfigParser()
    config.read('remote_tpcm.conf')

    print(f'{mycontainer}')

    docker_name = config[f"{mycontainer}"]['docker-name']
    image_source = config[f"{mycontainer}"]['image-source']
    image_name = config[f"{mycontainer}"]['image-name']
    tpcm_args = config[f"{mycontainer}"]['args']

    request_data = {
        "openconfig-tpcm:input": {
           "docker-name": docker_name,
           "image-source": image_source,
           "image-name": image_name,
           "args": tpcm_args
        }
    }

    print(json.dumps(request_data))
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



def tpcm_upgrade(remote_sw,upgrade_container) -> str:
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


    switch_ip = remote_sw['switch_ip']
    user_name = remote_sw['sonic_username']
    password = remote_sw['sonic_password']
    mycontainer = upgrade_container

    config = configparser.ConfigParser()
    config.read('remote_tpcm.conf')

    docker_name = config[f"{mycontainer}"]['docker-name']
    image_source = config[f"{mycontainer}"]['image-source']
    image_name = config[f"{mycontainer}"]['image-name']
    tpcm_args = config[f"{mycontainer}"]['args']
    skip_data = config[f"{mycontainer}"]['skip-data-migration']

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

    action = args.action.lower()

    switch_ip = args.switch_ip

    if validate_ip_address(switch_ip) == True:

       sonic_username = args.sonic_username
       sonic_password = args.sonic_password

       remote_sw = {'switch_ip':switch_ip, 'sonic_username':sonic_username, 'sonic_password':sonic_password}

       if action == "list":
        result = tpcm_list(remote_sw)
        print(f'{result}')

       if action == "install":
        myreturn_list = read_config()
        for container in myreturn_list:
         #result = tpcm_install(switch_ip=switch_ip, user_name=sonic_username, password=sonic_password)
         result = tpcm_install(remote_sw, install_container=container)
         print(f'{result}')

       if action == "remove":
        result = tpcm_list(remote_sw)
        tablen = len(result)
        for installed in result[1:tablen]:
          print (f'upgradable container :\r\n {installed}')
          myreturn_list = read_config()
          for container in myreturn_list:
            result = tpcm_remove(remote_sw, remove_container=container)
            print(f'{result}')

       if action == "upgrade":
        result = tpcm_list(remote_sw)
        tablen = len(result)
        for installed in result[1:tablen]:
          print (f'Installed container :\r\n {installed}')
          myreturn_list = read_config()
          for container in myreturn_list:
            result = tpcm_upgrade(remote_sw, upgrade_container=container)
            print(f'{result}')

    else:
      print("IP address is not valid\r\nUse tpcm_remote.py -h for Help")


if __name__ == '__main__':
    main()
