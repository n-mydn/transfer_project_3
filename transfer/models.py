from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta,datetime
from ckeditor.fields import RichTextField

adultnumber_choices =(
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),   
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),  
        ('9','9'), 
        ('10','10'),    
)

childrennumber_choices=(
        ('0','0'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
        ('9','9'),
        ('10','10'),
)

class Currency(models.Model):
    code = models.CharField(verbose_name=_('code'), max_length=3,primary_key=True)
    name = models.CharField(verbose_name=_('name'), max_length=55,)
    symbol = models.CharField(verbose_name=_('symbol'), max_length=4, blank=True)
    factor = models.DecimalField(verbose_name=_('factor'), max_digits=30, decimal_places=10, default=1.0,)

    def __str__(self):
       return self.name
   

class FromWhere(models.Model):
    name = models.CharField(max_length=300,verbose_name=_("Name"))

    def __str__(self):
        return self.name

class ToWhere(models.Model):
    name = models.CharField(max_length=300,verbose_name="Name")

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=100,verbose_name="İsim")
    max_people = models.IntegerField(verbose_name="En Çok Kişi Sayısı")
    fromwhere = models.ForeignKey(FromWhere,verbose_name="Nereden",on_delete=models.CASCADE)
    towhere = models.ForeignKey(ToWhere,verbose_name="Nereye",on_delete=models.CASCADE)
    capasity = models.CharField(max_length=20,verbose_name="Kapasite")
    price = models.IntegerField(verbose_name="Ücret")
    currency = models.CharField(max_length=3,verbose_name="Birim",default="₺",blank=True)
    car_image = models.FileField(verbose_name="Resim")

    def __str__(self):
        return self.name


class Transfer(models.Model):
    fromwhere = models.ForeignKey(FromWhere,verbose_name="Nereden",help_text=_('Lütfen listeden bir öge seçin.'),on_delete=models.CASCADE)
    towhere = models.ForeignKey(ToWhere,verbose_name="Nereye",help_text=_('Lütfen listeden bir öge seçin.'),on_delete=models.CASCADE)
    adultnumber = models.CharField(choices=adultnumber_choices,help_text=_('Lütfen listeden bir öge seçin.'),verbose_name="Yetişkin",default="1",max_length=2)
    childrennumber = models.CharField(choices=childrennumber_choices,help_text=_('Lütfen listeden bir öge seçin.'),verbose_name="Çocuk",default="0",max_length=2)

"""
Rezervasyonda varsayılanlar dönüş için
            reservation.date_of_return = "2023-01-01"
            reservation.time_of_return = "00:00"
            reservation.flightnumber_of_return = "-"

"""


class Reservation(models.Model):
    IdCar = models.ForeignKey(Car,verbose_name="Car",on_delete=models.CASCADE)
    no = models.CharField(verbose_name="Rezervasyon No",default=" ",max_length=200)
    name_surname = models.CharField(verbose_name="Ad-Soyad",max_length=100)
    phonenumber = PhoneNumberField(verbose_name="Telefon Numarası")
    email = models.EmailField(verbose_name="E-Posta")
    passport_no = models.CharField(verbose_name="Pasaport Numarası",max_length=15,default="")
    date = models.DateField(verbose_name="Transfer Tarihi",default=timezone.now().date())
    planetime = models.TimeField(verbose_name="Uçak İniş Zamanı")
    date_of_return = models.DateField(verbose_name="Dönüş Tarihi",default=timezone.now().date())
    time_of_return = models.TimeField(verbose_name="Dönüş Saati",default=datetime.now().strftime("%H:%M"))
    flightnumber_of_return = models.CharField(max_length=20,verbose_name="Dönüş Uçuş Numarası",default="-")
    flightnumber = models.CharField(max_length=20,verbose_name="Uçuş Numarası")
    another_traveller = models.CharField(max_length=100,verbose_name="Yolcular",default=" ")
    anothername = models.TextField(verbose_name="Diğer Yolcular")
    specialrequest = models.TextField(verbose_name="Transferle ilgili özel isteğinizi bu bölüme yazınız:",blank=True,null=True)
    messages = models.CharField(max_length=200,verbose_name="Karşılama Mesajı",blank=True,null=True)
    extras = models.TextField(verbose_name="Ekstralar")
    mail_choices = models.CharField(verbose_name="Fatura Türü",max_length=10,default="İstek Oluşturulmamış",blank=True,null=True)
    mail_context = models.TextField(verbose_name="Fatura Detay",blank=True,null=True,default=" ")
    total_amount = models.IntegerField(verbose_name="Toplam Fiyat",default=0)
    payment_method = models.CharField(verbose_name="Ödeme Yöntemi",default="Araçta Nakit",max_length=20)
    status = models.CharField(verbose_name="Durum",default= "İşlemde",max_length=15)

    def __str__(self):
        return str(self.date)
    
class Extras(models.Model):
    name = models.CharField(verbose_name=("Ad"),max_length=20)
    extra_image = models.FileField(verbose_name="Resim")
    price = models.IntegerField(verbose_name="Ücret")

    def __str__(self):
        return self.name



class Blog(models.Model):
    title = models.CharField(max_length=50,verbose_name="Başlık")
    content = RichTextField(verbose_name="İçerik")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")
    article_image = models.FileField(blank=True, null= True,verbose_name="Başlık Fotoğrafı")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']


class HomePageArticleOne(models.Model):
    title = models.CharField(max_length=200,verbose_name="Başlık")
    content = models.TextField(verbose_name="İçerik")
    image = models.FileField(blank=True, null= True,verbose_name="Fotoğraf")

    def __str__(self):
        return self.title
    

class HomePageArticleTwo(models.Model):
    title = models.CharField(max_length=200,verbose_name="Başlık")
    content = models.TextField(verbose_name="İçerik")
    image = models.FileField(blank=True, null= True,verbose_name="Fotoğraf")

    def __str__(self):
        return self.title
    

class WebAbout(models.Model):
    title = models.CharField(max_length=100,verbose_name="Kısım")
    content = RichTextField(verbose_name="İçerik")

    def __str__(self):
        return self.title
    

class Gallery(models.Model):
    image = models.FileField(verbose_name="Resim")