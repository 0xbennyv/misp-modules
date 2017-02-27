import json
import base64

from pymisp.tools import openioc

misperrors = {'error': 'Error'}
userConfig = {}
inputSource = ['file']

moduleinfo = {'version': '0.1', 'author': 'Raphaël Vinot',
              'description': 'Import OpenIOC package',
              'module-type': ['import']}

moduleconfig = []


def handler(q=False):
    # Just in case we have no data
    if q is False:
        return False

    # The return value
    r = {'results': []}

    # Load up that JSON
    q = json.loads(q)

    # It's b64 encoded, so decode that stuff
    package = base64.b64decode(q.get("data")).decode('utf-8')

    # If something really weird happened
    if not package:
        return json.dumps({"success": 0})

    pkg = openioc.load_openioc(package)
    for attrib in pkg.attributes:
        r["results"].append({"values": [attrib.value], "types": [attrib.type], "categories": [attrib.category]})
    return r


def introspection():
    modulesetup = {}
    try:
        userConfig
        modulesetup['userConfig'] = userConfig
    except NameError:
        pass
    try:
        inputSource
        modulesetup['inputSource'] = inputSource
    except NameError:
        pass
    return modulesetup


def version():
    moduleinfo['config'] = moduleconfig
    return moduleinfo
