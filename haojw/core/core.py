
import os, sys
import json
SHOW_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)),'config/show')
APP_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),'config/app/AppData.json')

with open(APP_FILE) as a: 
        apps = json.load(a)

def get_show_app_data(type, show):
    data = []
    app_data = get_show_preset(show)['app']
    for app in app_data:
        if app_data[app]['type'] == type:
            data.append(app_data[app])
    
    return data

def get_app_by_id(id):
    for app in apps:
        if apps[app]['data']['id'] == id:
            return apps[app]['data']
    return None

def should_app_show(app):
    app_name = app['name']
    app_version = app['version']
    level = app['level']
    shows = app['shows']

    if level == 0:
        return True
    elif level == -1:
        return False
    
    return False


def get_approved_shows(show_names=None):
    # should approved shows, should from db
    shows = [i.split('.')[0] for i in os.listdir(SHOW_DIR)]
    return shows

def get_show_preset(show):
    shows_presets = os.listdir(SHOW_DIR)
    for i in shows_presets:
        if show in i:
            with open(os.path.join(SHOW_DIR, i)) as f:
                preset = json.load(f)
                return preset
    return

def get_user_recent_show(user_name):
    #get user recent show
    pass
    return

def get_show_description(show):
    preset = get_show_preset(show)
    description = preset['description']
    
    return description

############# test
# get_app_data('software')
# get_approved_shows()
# get_show_description('test_show_1')