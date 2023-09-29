import json
import argparse
import ast
import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import boto3
import base64
from botocore.exceptions import ClientError

def tpcm_list(vrf_id: int):
    """
	List TPCM install
	vrf_id: ID integer is the VRF id
	If no value, list all TPCM in each VRF
    """

    request_data = {

    


def sonic_create_vlan(vlan_id: int, switch_ip: str, user_name: str, password: str):
    """
        Create a VLAN on a SONiC device via an API call based on the passed VLAN ID
        :param vlan_id: VLAN ID in the form of an integer
        :param switch_ip: IP address of the switch to target for creating the VLAN
        :param user_name: Administrative username for the switch - must have admin level access
        :param password: Password for the specified user
        """
    request_data = {
        "openconfig-interfaces:interface": [
            {
                "config": {
                    "name": f"Vlan{vlan_id}"
                },
                "name": f"Vlan{vlan_id}"
            }
        ]
    }
    print(json.dumps(request_data))
    try:
        response = requests.post(url=f"https://{switch_ip}/restconf/data/openconfig-interfaces:interfaces",
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
        print(f'Success! VLAN {vlan_id} created')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--aws_profile_name", help="AWS profile name to use to pull from Secrets Manager", type=str)
    parser.add_argument("--secret_name", help="Name of the secret to pull from AWS Secrets Manager", type=str)
    parser.add_argument("--aws_region_name", help="Name of the AWS region in which your secret is stored IE: us-west-1", type=str)
    parser.add_argument("--vlan_id", help="VLAN ID to use specified as an integer", type=int)
    parser.add_argument("--switch_ip", help="IP address of the switch to automate", type=str)
    args = parser.parse_args()

    aws_profile_name = args.aws_profile_name  # If no argument is passed for aws_profile_name the default profile will
    # be used if it exists in ~/.aws/credentials

    secret_name = args.secret_name
    vlan_id = args.vlan_id
    switch_ip = args.switch_ip
    aws_region_name = args.aws_region_name

    secret = get_secret(secret_name_query=secret_name, profile_name=aws_profile_name, region_name=aws_region_name)
    dict_secret = ast.literal_eval(secret)
    sonic_username = dict_secret.get("sonic_username")
    sonic_password = dict_secret.get("sonic_password")

    sonic_create_vlan(vlan_id=vlan_id, switch_ip=switch_ip, user_name=sonic_username, password=sonic_password)


if __name__ == '__main__':
    main()
