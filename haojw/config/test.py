import json

app_data_file = "/sw/PLE/workspace/haojw/ts/haojw_work/launcher/config/app/AppData.json"

data = {"houdini18.5.351":{"data": {'wiki_url': u'houdini help page',
                                            'id': 4,
                                            'name': u'houdini',
                                            'exec_cmd': u'houdini',
                                            'level': 0,
                                            'icon_path': u'/launcher/ui/app_icon/houdini.png',
                                            'pre_exec': u'source /sw/PLE/studio/shell/binit_setup && binit studio houdini houdini@18.5.351',
                                            'platform': u'linux',
                                            'label_name': u'Houdini',
                                            'version': u'18.5.351',
                                            'type': u'software',
                                            'shows': u''}
                                    },
        "houdini19.0.455":{"data": {'wiki_url': u'houdini help page',
                                            'id': 3,
                                            'name': u'houdini',
                                            'exec_cmd': u'houdini',
                                            'level': 0,
                                            'icon_path': u'/launcher/ui/app_icon/houdini.png',
                                            'pre_exec': u'source /sw/PLE/studio/shell/binit_setup && binit studio houdini houdini@18.5.351',
                                            'platform': u'linux',
                                            'label_name': u'Houdini',
                                            'version': u'19.0.455',
                                            'type': u'software',
                                            'shows': u''}
                                    },
        "maya2019":{"data":{'wiki_url': u'maya2019 help page',
                                    'id': 1,
                                    'name': u'maya',
                                    'exec_cmd': u'maya',
                                    'level': 0,
                                    'icon_path': u'/launcher/ui/app_icon/maya.png',
                                    'pre_exec': u'source /sw/PLE/studio/shell/binit_setup && binit studio maya show_maya',
                                    'platform': u'linux',
                                    'label_name': u'Maya',
                                    'version': u'2019',
                                    'type': u'software',
                                    'shows': None}
                          
                            },
        "maya2022":{"data":{'wiki_url': u'maya2022 help page',
                                    'id': 2,
                                    'name': u'maya',
                                    'exec_cmd': u'maya',
                                    'level': 0,
                                    'icon_path': u'/launcher/ui/app_icon/maya.png',
                                    'pre_exec': u'source /sw/PLE/studio/shell/binit_setup && binit studio maya show_maya',
                                    'platform': u'linux',
                                    'label_name': u'Maya',
                                    'version': u'2022',
                                    'type': u'software',
                                    'shows': None}
                          
                            },
        

}

with open(app_data_file, 'w') as f:
    json.dump(data, f, indent=4)
