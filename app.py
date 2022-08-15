from packages.app_contstants import ApiEndpoint
from urllib.request import urlopen
import ssl
import json
import pprint


ssl._create_default_https_context = ssl._create_unverified_context
print(ApiEndpoint.API1.do_something)
resp = urlopen(ApiEndpoint.API1.url)
resp = json.loads(resp.read().decode())

pp = pprint.PrettyPrinter(indent=3)
pp.pprint(resp['entries'][0]['API'])
