import re
from django import forms
from mainapp.models import User, Miasta, Atrakcja
from django.core.exceptions import ObjectDoesNotExist
from gmapi import maps
from gmapi.forms.widgets import GoogleMap

class FormularzKoszykowy(forms.Form):
	koszyk = forms.CharField(label="Wpisz nazwe planu", required=False)

class FormularzWyboru(forms.Form):
	miasto = forms.CharField(label="Wpisz miasto:", max_length=30, required=False)

class MapForm(forms.Form):
    	mapa = forms.Field(widget=GoogleMap(attrs={'width':600, 'height':500}))

class FormularzRejestracji(forms.Form):
	username = forms.CharField(label="Login*:",max_length=30)
	email = forms.EmailField(label="Email*:")
	password1 = forms.CharField(label="Haslo*:",widget=forms.PasswordInput())
	password2 = forms.CharField(label="Powtorz haslo*:",widget=forms.PasswordInput())
	firstname = forms.CharField(label="Imie:",max_length=20,required=False)
	lastname = forms.CharField(label="Nazwisko:",max_length=30,required=False)

	def clean_password2(self):
    		password1=self.cleaned_data['password1']
    		password2=self.cleaned_data['password2']
        	if password1==password2:
			return password2
        	else:
            		raise forms.ValidationError("Hasla sie roznia")

	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$',username):
			raise forms.ValidationError("Dopuszczalne sa tylko cyfry, litery angielskie i _")
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError("Taki uzytkownik juz istnieje")
