import os
import json
import urllib.request
import sys
import requests
import socket

from urllib.request import urlopen
from PIL import Image, ImageFont, ImageDraw
from inky import InkyWHAT
from font_fredoka_one import FredokaOne
from font_source_serif_pro import SourceSerifProSemibold
from font_source_sans_pro import SourceSansProSemibold
from time import gmtime, strftime

# Set current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Set up the correct display and scaling factors
inky_display = InkyWHAT("red")
inky_display.set_border(inky_display.WHITE)

w = inky_display.WIDTH
h = inky_display.HEIGHT

# Create a new canvas to draw on
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# Get API data
try:
  f = urllib.request.urlopen('http://pi.hole/admin/api.php')
  json_string = f.read()
  parsed_json = json.loads(json_string)
  adsblocked = parsed_json['ads_blocked_today']
  ratioblocked = parsed_json['ads_percentage_today']
  domainsblocked = parsed_json['domains_being_blocked']
  status = parsed_json['status']
  queries = parsed_json['dns_queries_today']
  gravity = parsed_json['gravity_last_updated']
  f.close()
except:
  queries = '?'
  adsblocked = '?'
  ratio = '?'

try:
  f = urllib.request.urlopen('http://pi.hole/admin/api.php?topItems=1&auth=b6a9f62f596a91adb02f3a02a04300d66b05bfc482e4056709bac922c3358aca')
  json_string = f.read()
  parsed_json = json.loads(json_string)
  topquery = parsed_json['top_queries']
  topad = parsed_json['top_ads']
  f.close()
except:
  topclient = '?'
  topad = '?'

try:
  lastblocked = requests.get('http://pi.hole/admin/api.php?recentBlocked&auth=b6a9f62f596a91adb02f3a02a04300d66b05bfc482e4056709bac922c3358aca')
except:
  response = '?'

catfont = ImageFont.truetype(SourceSerifProSemibold, 20)
datafont = ImageFont.truetype(SourceSansProSemibold, 20)
titlefont = ImageFont.truetype(FredokaOne,22)

inky_display = InkyWHAT("red")
inky_display.set_border(inky_display.WHITE)

draw.text((10,10), "Pi-Hole Monitor", inky_display.RED, titlefont)

draw.text((10,40), "HOSTNAME:", inky_display.BLACK, catfont)
draw.text((130,40), socket.gethostname(), inky_display.RED, datafont)

draw.text((10,70), "Status:", inky_display.BLACK, catfont)
draw.text((85,70), str(status), inky_display.RED, datafont)
draw.text((200,70), str(strftime("%d-%m-%y %H:%M:%S", gmtime())), inky_display.RED, datafont)

draw.text((10,100), "Queries/24h:", inky_display.BLACK, catfont)
draw.text((135,100), str(queries), inky_display.RED, datafont)

draw.text((200,100), "Blocked:", inky_display.BLACK, catfont)
draw.text((300,100), str(adsblocked), inky_display.RED, datafont)

draw.text((10,130), "Percentage blocked:", inky_display.BLACK, catfont)
draw.text((200,130), str("%.1f" % round(ratioblocked,2)) + "%", inky_display.RED, datafont)

draw.text((10,160), "Domains in Gravity:", inky_display.BLACK, catfont)
draw.text((200,160), str(domainsblocked), inky_display.RED, datafont)

draw.text((10,190), "Top Query:", inky_display.BLACK, catfont)
draw.text((200,190), str(topquery), inky_display.RED, datafont)

#draw.text((10,220), "Updated:", inky_display.BLACK, catfont)
#draw.text((200,220), str(strftime("%d-%m-%Y %H:%M:%S", gmtime())), inky_display.RED, datafont)

draw.text((10,250), "Last Blocked:", inky_display.BLACK, catfont)
draw.text((140,250), str(lastblocked.text), inky_display.RED, datafont)

inky_display.set_image(img)
inky_display.show()
