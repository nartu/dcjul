from django.test import TestCase
from urllib.parse import urlencode, quote_plus, quote
from urllib.parse import urlparse
import os
from dc_parse.models import MediaVkPhoto
from dc_main.models import Media, Tag, TagMediaBond

class DbTest(TestCase):
    def main():
        media = Media.objects.get(pk=120)
        MediaVkPhoto.objects.get(media=media)
