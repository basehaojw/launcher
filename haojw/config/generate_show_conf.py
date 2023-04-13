import json
import os

APP_DATA_FILE = os.path.join(os.path.dirname(__file__),'app/AppData.json')
TARGET_DIR = os.path.join(os.path.dirname(__file__),'show')

def generate_show_conf(show, show_description, show_app_list=None, defaule_app_list=None):
    result_data = {"name": show, "description": show_description, "app":{}}
    with open(APP_DATA_FILE) as f:
        apps = json.load(f)
    
    for show_app in show_app_list:
        for app in apps:
            if show_app == app:
                if app in defaule_app_list:
                    apps[show_app]['data']['version'] = 'default'
                result_data["app"].update({show_app: apps[show_app]['data']})
    
    with open(os.path.join(TARGET_DIR, "{}.preset".format(show)), 'w') as t:
        json.dump(result_data, t, indent=4)

    print("done!!!")
    
        
        

# example
# generate_show_conf('test_show_1', 'test amazing show 1', ['maya2019','maya2022', 'houdini18.5.351'],['maya2019', 'houdini18.5.351'])
