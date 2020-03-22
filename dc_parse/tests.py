from django.test import TestCase
from urllib.parse import urlencode, quote_plus, quote
from urllib.parse import urlparse
import os

def write_json(date='', filename='answer.json'):
    save_dir = os.path.join('dc_parse','debug','json')
    filename = os.path.join(save_dir,filename)
    return filename


print(write_json())
