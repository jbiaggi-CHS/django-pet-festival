from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
import requests
import json
from .models import Pet, State
from .forms import UserInputForm
from dotenv import load_dotenv
import urllib3.util.url
import os

load_dotenv()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def petFest(request):
    #urllib3.util.url._QUERY_CHARS.add('-')
    #urllib3.util.url._QUERY_CHARS.add(':')
    #url_base = 'https://chsnebraska.shelterbuddy.com/api/v2/animal/note/list?page=1&pageSize=10&startIndex=0'
    #searchModel = {
        #'UpdatedSinceUtc': '2024-05-10T00:00:00Z',
        #'AnimalId': [106095, 100678],
    #}
    #s = requests.Session()
    #USERNAME = os.environ.get('API_USER')
    #PASSWORD = os.environ.get('API_PASSWORD')
    #s.get('https://chsnebraska.shelterbuddy.com/api/v2/authenticate?username=' + USERNAME + '&password=' + PASSWORD)

    #r = s.post(url_base, json=searchModel)
    #print(r.request.body)
    #print(r.status_code)
    #data = r.json()
    #print(json.dumps(data, indent=2))

    pets = Pet.objects.all()

    return render(request, 'index.html', {'pets': pets})

def load_pets(request):
    pets = Pet.objects.all()
    return render(request, 'pet_cards.html', {'pets': pets})

def pet_detail_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            phoneNumber = form.cleaned_data['phoneNumber']
            streetNumber = form.cleaned_data['streetNumber']
            streetName = form.cleaned_data['streetName']
            state_form = form.cleaned_data['state']
            postCode = form.cleaned_data['postCode']

            try:
                state = State.objects.get(name=state_form)
                state_id = state.state_id
            except State.DoesNotExist:
                return JsonResponse({'message': 'Invalid state'}, status=400)
            
            s = requests.Session()
            USERNAME = os.getenv('API_USER')
            PASSWORD = os.getenv('API_PASSWORD')
            s.get('https://chsnebraska.shelterbuddy.com/api/v2/authenticate?username=' + USERNAME + '&password=' + PASSWORD)

            suburb_url = 'https://chsnebraska.shelterbuddy.com/api/v2/location/suburb/list'
            searchModel = {
                'Postcode': postCode,
            }
            page = 1
            pageSize = 10
            startIndex = 0
            params = {
                'page': page,
                'pageSize': pageSize,
                'startIndex': startIndex,
            }
            city_response = s.post(suburb_url, json=searchModel, params=params)
            data = city_response.json()
            if city_response.status_code == 200:
                if 'Data' in data:
                    for item in data['Data']:
                        country = item['Country']['Id']
                        jurisdiction = item['Jurisdiction']['Id']
                        suburb = item['Id']
                else:
                    print('Data not found in JSON')
            else:
                print(f"Error: {city_response.status_code}")
            #combine pet info and user input for SB API call
            model = {
                'AcquisitionId': 2,
                'CountryId': country,
                'Stateid': state_id,
                'SuburbId': suburb,
                'Email': email,
                'FirstName': firstName,
                'LastName': lastName,
                'StreetNumber': streetNumber,
                'StreetName': streetName,
                'PostCode': postCode,
                'HomePhoneNumber': phoneNumber,
            }
            url = 'https://chsnebraska.shelterbuddy.com/api/v2/fundraising/acquisition/person'
            r = s.put(url, json=model)
            if r.status_code == 200:
                pet.hold = True
                pet.save()
                subject = 'Animal On Hold'
                message = f'Shelterbuddy {pet.shelterbuddyId} | {pet.name} has been put on hold at Pet Festival! {firstName} {lastName} is on their way to adopt them. Please merge them in from the Pre Registration / Data Acquisition menu in shelterbuddy: https://chsnebraska.shelterbuddy.com/Fundraising/Acquisition/AcquisitionList.aspx'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [
                    'frontdesk@capitalhumanesociety.org',
                    ]
                send_mail(subject, message, email_from, recipient_list)
                return redirect('index')
            else:
                return JsonResponse({'message': 'API call failed', 'response_data': r.json()}, status=r.status_code)
    else:
        form = UserInputForm()

    return render(request, 'pet_detail.html', {'form': form, 'pet': pet})
        
def pet_hold_view(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'remove_hold':
            pet.hold = False
            pet.save()
            subject = 'Animal On Hold'
            message = f'Shelterbuddy {pet.shelterbuddyId} | {pet.name} has been taken off hold at Pet Festival.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [
                'frontdesk@capitalhumanesociety.org',
                ]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('index')
        return redirect('index')
    return render(request, 'pet-hold.html', {'pet': pet})
