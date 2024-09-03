
import os
import configparser
import requests
import string
import random

def get_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    #return os.environ.get('SERVERME_KEY') if os.environ.get('SERVERME_KEY') is not None else config.get('KEYS', 'SERVERME_KEY')
    return os.environ.get('SERVERME_KEY')

def get_rcon():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def get_server(map, loc):
    new_loc = None
    if loc == "eu":
        new_loc = "fr"
    elif loc == "na":
        new_loc = "chi"
    else:
        new_loc = loc.split()[1]
     
    api_key = get_key()
    map_name = get_map(map)
    if map_name is None: return None, None

    prefix = "" if "eu" in loc else "na."
    response = requests.get('https://direct.{}serveme.tf/api/reservations/new?api_key={}'.format(prefix, api_key), verify=False)
    if response.status_code == 200:
        json_response = response.json()

        url = json_response["actions"]["find_servers"] + "?api_key={}".format(api_key)
        time_slot = json_response["reservation"]

        response = requests.post(url=url, data=time_slot, verify=False).json()
        servers = response["servers"]
        if prefix == "":
            server = get_eu_server(servers, new_loc)
        else:
            server = get_na_server(servers, new_loc)
        

        url = response["actions"]["create"] + "?api_key={}".format(api_key)
        
        time_slot["rcon"] = get_rcon()
        time_slot["password"] = "rahmix" + str(random.randint(1, 1000))
        time_slot["server_id"] = int(server)
        time_slot["server_config_id"] = get_config(loc.split()[0],map_name)
        time_slot["first_map"] = map_name
        time_slot["enable_plugins"] = True

        response = requests.post(url=url, json=time_slot, verify=False).json()

        server_info = response["reservation"]["server"]
        ip_and_port = server_info["ip_and_port"]
        password = response["reservation"]["password"]
        rcon = response["reservation"]["rcon"]

        full_ip = f'connect {ip_and_port}; password "{password}"'

        return full_ip, rcon
    return None, "No API response."

def get_map(map):

    maps = {"process": "cp_process_f12", 
            "sunshine": "cp_sunshine",
            "snakewater": "cp_snakewater_final1",
            "metalworks": "cp_metalworks_f5",
            "gullywash": "cp_gullywash_f9",
            "reckoner": "cp_reckoner_rc6",
            "clearcut": "koth_clearcut_b15d", 
            "granary": "cp_granary_pro_rc16f",
            "prolands": "cp_prolands_rc2ta", 
            "bball": "ctf_ballin_skyfall",
            "ultiduo": "ultiduo_baloo_v2",
            "subbase": "cp_subbase_b2",
            "product": "koth_product_final",
            "bagel": "koth_bagel_rc10",
            "sultry": "cp_sultry_b8a"}
    return maps.get(map.lower(), None)

def get_config(region, map):
    maps_configs = {'eu' : {"cp": 142, #Previously 4
                    "koth": 24,
                    "ctf": 12,
                    "ultiduo": 11        
                    },
                    'na': {
                    "cp": 105,
                    "koth": 106,
                    "ctf": 12,
                    "ultiduo": 11   
                    }}
    region_dict = maps_configs.get(region.lower(), {})
    return region_dict.get(map.split("_")[0])

def get_eu_server(servers, loc):
    possible_servers = [x for x in servers if x["flag"] == loc and 'Anti-DDoS' in x['name']]
    possible_servers = possible_servers if len(possible_servers) > 0 else [x for x in servers if x['flag'] == loc]
    return possible_servers[0]["id"]

def get_na_server(servers, loc):
    ip_region = {"chi": "nfo-chicago",
                 "ks": "ks",
                 "la": "la"}
    loc = ip_region.get(loc, loc)
    return [x for x in servers if x["ip"].lower().startswith(loc)][0]["id"]