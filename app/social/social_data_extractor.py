import os
from typing import Text

import requests


class SocialDataExtractor:

    def __init__(self):
        self.service_url = 'https://api.sharedcount.com/v1.0/'

    def get_fb_shares(self, url: Text) -> int:
        api_key = os.environ.get('SHARED_COUNT_KEY')
        params = {'url': url, 'apiKey': api_key}
        content = requests.get(self.service_url, params=params)
        fb_data = content.json()['Facebook']
        return fb_data['share_count']