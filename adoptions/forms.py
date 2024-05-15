from django import forms
from adoptions.models import State

class UserInputForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserInputForm, self).__init__(*args, **kwargs)
        try:
            nebraska = State.objects.get(name='Nebraska')
            self.fields['state'].initial = nebraska.id 
        except State.DoesNotExist:
            pass

    firstName = forms.CharField(label='First Name', max_length=200)
    lastName = forms.CharField(label='Last Name', max_length=200)
    email = forms.CharField(label='Email', max_length=200)
    phoneNumber = forms.CharField(label='Phone Number', max_length=200)
    streetNumber = forms.CharField(label='Street Number', max_length=200)
    streetName = forms.CharField(label='Street Name', max_length=200)
    city = forms.CharField(label='City', max_length=200)
    state = forms.ModelChoiceField(queryset=State.objects.all(), label='State', empty_label='Choose...')
    postCode = forms.CharField(label='Zip Code', max_length=200)

