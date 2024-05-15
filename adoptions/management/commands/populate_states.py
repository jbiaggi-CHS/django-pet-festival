import requests
import os
from django.core.management.base import BaseCommand
from adoptions.models import State
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Fetch states from the API and populate the database'

    def handle(self, *args, **kwargs):
        url = 'https://chsnebraska.shelterbuddy.com/api/v2/location/state/list'
        s = requests.Session()
        USERNAME = os.environ.get('API_USER')
        PASSWORD = os.environ.get('API_PASSWORD')
        s.get('https://chsnebraska.shelterbuddy.com/api/v2/authenticate?username=' + USERNAME + '&password=' + PASSWORD)

        searchModel = {
            'CountryId': [1],
        }
        page = 1
        pageSize = 10
        startIndex = 0

        while True:
            params = {
            'page': page,
            'pageSize': pageSize,
            'startIndex': startIndex,
            }
            r = s.post(url, json=searchModel, params=params)
            data = r.json()


            if 'Data' in data:
                for item in data['Data']:
                    state_id = item['Id']
                    name = item['Name']
                    abbreviation = item['Abbreviation']

                    #create or update the state
                    State.objects.update_or_create(
                        state_id=state_id,
                        defaults={'name': name, 'abbreviation': abbreviation}
                    )
                
                
                total_results = data.get('Paging', {}).get('TotalResults', 0)
                total_pages = data.get('Paging', {}).get('TotalPages', 1)

                if page >= total_pages:
                    break

                page += 1
            else:
                print("JSON is empty or returned a null value")
                break
            self.stdout.write(self.style.SUCCESS('Successfully populated the database with states'))
