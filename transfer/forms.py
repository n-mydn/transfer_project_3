from django import forms
from .models import Transfer,Reservation,Blog,WebAbout,Car,Gallery
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from bootstrap_datepicker_plus.widgets import DatePickerInput,TimePickerInput
from django.utils import timezone
from datetime import timedelta
from .models import Extras
from ckeditor.fields import RichTextField
from datetime import datetime

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = "__all__"

class ReservationForm(forms.ModelForm):
    phonenumber = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='TR',
            attrs={'class': "form-control"}),
    )
    class Meta:
        model=Reservation
        fields = ["name_surname","phonenumber","email","date","planetime","flightnumber","passport_no","date_of_return","time_of_return","flightnumber_of_return"]
        start_date = timezone.now().date()
        end_date = start_date+ timedelta(weeks=8) 
        time_now= datetime.now()
        end_time = time_now+ timedelta(hours=2)
        value = end_time.strftime("%H:%M")
        widgets = {
            'name_surname': forms.TextInput(attrs={'class': "form-control"}),
            'email':forms.EmailInput(attrs={'class': "form-control"}),
            'date': DatePickerInput(attrs={'class': "form-control"},
                                    options={
                                        "format": "DD/MM/YYYY",
                                        "minDate": str(start_date),
                                        "maxDate": str(end_date)
                                       }),
            'planetime': TimePickerInput(attrs={'class': "form-control",'value': value},
                                    options={
                                        "format": 'HH:mm',
                                        }),
            'flightnumber': forms.TextInput(attrs={'class': "form-control"}),
            'passport_no': forms.TextInput(attrs={'class': "form-control"}),
            'date_of_return': DatePickerInput(attrs={'class': "form-control"},
                                    options={
                                        "format": "DD/MM/YYYY",
                                        "minDate": str(start_date),
                                        "maxDate": str(end_date)
                                       }),
            'time_of_return': TimePickerInput(attrs={'class': "form-control"},
                                    options={
                                        "format": 'HH:mm',
                                        }),
            'flightnumber_of_return': forms.TextInput(attrs={'class': "form-control"}),
        }

class ReservationQueryForm(forms.ModelForm):
    class Meta:
        model=Reservation
        fields = ["email","no"]
        widgets = {
            'email':forms.EmailInput(attrs={'class': "form-control"}),
            'no': forms.TextInput(attrs={'class': "form-control"}),

        }

class BireyselFaturaForm(forms.Form):
    name_surname = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
    tc_no = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': "form-control"}))

class KurumsalFaturaForm(forms.Form):
    firma_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
    vergi_no = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
    bill_adress = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}),
                                  required=False)
    
class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı",widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label = "Parola",widget=forms.PasswordInput(attrs={'class': "form-control"}))

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title","content","article_image"]
        widgets = {
            'title':forms.TextInput(attrs={'class': "form-control"}),
            'content':RichTextField(),
        }

class WebAboutForm(forms.ModelForm):
    class Meta:
        model = WebAbout
        fields = ["content"]
        widgets = {
            'content':RichTextField(),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'

class RezervasyonDurumuForm(forms.Form):
    rezervasyon_durumu = forms.ChoiceField(choices=[('Onaylandı', 'Onaylandı'), ('Ret Edilmiştir', 'Ret Edilmiştir')],
                                           widget=forms.RadioSelect)