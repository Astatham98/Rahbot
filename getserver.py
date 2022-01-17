
import os
import configparser
import requests
import string
import random

def get_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return os.environ.get('SERVERME_KEY') if os.environ.get('SERVERME_KEY') is not None else config.get('KEYS', 'servermekey')

def get_rcon():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))



def get_server(map):
    api_key = get_key()
    print(api_key, type(api_key))
    map_name = get_map(map)
    if map_name is None: return None, None

    response = requests.get('https://direct.serveme.tf/api/reservations/new?api_key={}'.format(api_key), verify=False)
    print(response.status_code)
    if response.status_code == 200:
        json_response = response.json()

        url = json_response["actions"]["find_servers"] + "?api_key={}".format(api_key)
        time_slot = json_response["reservation"]

        response = requests.post(url=url, data=time_slot, verify=False).json()
        servers = response["servers"]
        possible_servers = [x for x in servers if x["flag"] == "fr"]
        server = possible_servers[0]["id"]

        url = response["actions"]["create"] + "?api_key={}".format(api_key)
        
        time_slot["rcon"] = get_rcon()
        time_slot["password"] = "rahmix"
        time_slot["server_id"] = int(server)
        time_slot["server_config_id"] = 4 if "koth" not in map_name else 24
        time_slot["first_map"] = map_name
        time_slot["enable_plugins"] = True


        response = requests.post(url=url, json=time_slot, verify=False).json()

        server_info = response["reservation"]["server"]
        ip_and_port = server_info["ip_and_port"]
        password = response["reservation"]["password"]
        rcon = response["reservation"]["rcon"]

        full_ip = "connect " + ip_and_port + f"; password {password}"

        return full_ip, rcon
    return None, "No API response."

def get_map(map):

    maps = {"process": "cp_process_f9a", 
            "sunshine": "cp_sunshine",
            "snakewater": "cp_snakewater_final1",
            "metalworks": "cp_metalworks_f2",
            "gullywash": "cp_gullywash_f5",
            "reckoner": "cp_reckoner_rc6",
            "clearcut": "koth_clearcut_b15d", 
            "granary": "cp_granary_pro_rc8"}
    return maps.get(map.lower(), None)
