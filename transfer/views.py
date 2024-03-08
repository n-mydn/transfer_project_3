from django.shortcuts import render,redirect
from .forms import TransferForm,ReservationForm,ReservationQueryForm,BireyselFaturaForm,KurumsalFaturaForm,LoginForm,BlogForm,WebAboutForm,CarForm,GalleryForm,RezervasyonDurumuForm
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve,reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from .models import Car,Transfer,FromWhere,ToWhere,Extras,Reservation,Blog,HomePageArticleOne,HomePageArticleTwo,WebAbout,Gallery
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.contrib import messages
import random
import string
from django.utils import timezone
from datetime import datetime,timedelta


#----------------------------------- Admin Kısmı -------------------------------------
def day_add(day):
    bugun =timezone.now().date()
    bır_gun = timezone.timedelta(days=day)
    return bugun+bır_gun

def admin(request):
    form = LoginForm(request.POST or None)
    context={
        "form":form
        }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)

        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"admin/admin_giris.html",context)

        messages.success(request,"Başarıyla Giriş Yaptınız...")
        auth_login(request,user)
        return redirect("admin_index")
    
    return render(request,"admin/admin_giris.html",context)

@login_required(login_url="admin")
def admin_index(request):
    bugun = timezone.now().date()
    reservations = Reservation.objects.filter(
        Q(status="İşlemde")&
        Q(date__gte=bugun)
    ).order_by("date")
    context={
        "reservations":reservations,
    }
    return render(request,"admin/admin_index.html",context)

@login_required(login_url="admin")
def admin_reservation_process(request):
    yarın = day_add(1)
    hafta = day_add(7)
    bugun = timezone.now().date()

    reservations_today = Reservation.objects.filter(
        Q(status="İşlemde")&
        Q(date=bugun)
        )
    reservations_tomorrow = Reservation.objects.filter(
        Q(status="İşlemde")&
        Q(date=yarın)
        ) 
    reservations_week = Reservation.objects.filter(
        Q(status="İşlemde")&
        Q(date__gte=bugun)&
        Q(date__lte=hafta)
        ) 
    context={
        "reservations_today":reservations_today,
        "reservations_tomorrow":reservations_tomorrow,
        "reservations_week":reservations_week,
    }
    return render(request,"admin/admin_reservation_process.html",context)

@login_required(login_url="admin")
def admin_reservation_certified(request):
    yarın = day_add(1)
    hafta = day_add(7)
    bugun = timezone.now().date()

    reservations_today = Reservation.objects.filter(
        Q(status="Onaylandı")&
        Q(date=bugun)
        )
    reservations_tomorrow = Reservation.objects.filter(
        Q(status="Onaylandı")&
        Q(date=yarın)
        ) 
    reservations_week = Reservation.objects.filter(
        Q(status="Onaylandı")&
        Q(date__gte=bugun)&
        Q(date__lte=hafta)
        ) 
    context={
        "reservations_today":reservations_today,
        "reservations_tomorrow":reservations_tomorrow,
        "reservations_week":reservations_week,
    }
    return render(request,"admin/admin_reservation_certified.html",context)

@login_required(login_url="admin")
def admin_reservation_deprecated(request):
    yarın = day_add(1)
    hafta = day_add(7)
    bugun = timezone.now().date()

    reservations_today = Reservation.objects.filter(
        Q(status="Ret Edilmiştir")&
        Q(date=bugun)
        )
    reservations_tomorrow = Reservation.objects.filter(
        Q(status="Ret Edilmiştir")&
        Q(date=yarın)
        ) 
    reservations_week = Reservation.objects.filter(
        Q(status="Ret Edilmiştir")&
        Q(date__gte=bugun)&
        Q(date__lte=hafta)
        ) 
    context={
        "reservations_today":reservations_today,
        "reservations_tomorrow":reservations_tomorrow,
        "reservations_week":reservations_week,
    }
    return render(request,"admin/admin_reservation_deprecated.html",context)


@login_required(login_url="admin")
def admin_reservation_detail(request,id):
    reservation = Reservation.objects.get(id=id)
    car = Car.objects.get(id=reservation.IdCar.id)
    form = RezervasyonDurumuForm(request.POST or None)
    context = {
        "car":car,
        "reservation":reservation,
        "form":form,
    }

    if form.is_valid():
        rezervasyon_durumu = form.cleaned_data['rezervasyon_durumu']
        reservation.status = rezervasyon_durumu
        reservation.save()
        messages.success(request,"Rezervasyon durumu başarıyla güncellenmiştir.")
        return redirect("admin_reservation_detail",reservation.id)
        
    return render(request,"admin/admin_reservation_detail.html",context)

@login_required(login_url="admin")
def admin_price_extras(request):
    extras = Extras.objects.all()
    if request.method == "POST":
        for extra in extras:
            if request.POST.get(extra.name) != None:
                no = extra.id
                price_value = request.POST.get(extra.name)
                extra_update = Extras.objects.get(id=no)
                extra_update.price = price_value
                extra_update.price_en = price_value
                extra_update.price_de = price_value
                extra_update.price_ru = price_value
                extra_update.save()
                messages.success(request,"{} fiyatı başarı ile güncellendi.".format(extra_update.name))
                
        extras = Extras.objects.all()
        return redirect("admin_price_extras")
    
    return render(request,"admin/admin_price_extras.html",{"extras":extras})


@login_required(login_url="admin")
def admin_price_cars(request):
    cars = Car.objects.all()
    if request.method == "POST":
        for car in cars:
            if request.POST.get(car.name) != None:
                car_value = request.POST.get(car.name)
                car_update = Car.objects.filter(id=car.id).first()
                car_update.price = car_value
                car_update.price_en = car_value
                car_update.price_de = car_value
                car_update.price_ru = car_value
                car_update.save()
                messages.success(request,"{}: ({} - {}) fiyatı başarıyla güncellendi.".format(car_update.name,car_update.fromwhere,car_update.towhere))
        car = Car.objects.all()
        return redirect("admin_price_cars")    
        
    return render(request,"admin/admin_price_cars.html",{"cars":cars})

@login_required(login_url="admin")
def admin_cars_add(request):
    cars = Car.objects.all()
    form = CarForm(request.POST or None, request.FILES or None)
    context={
        "cars":cars,
        "form":form,
    }
    if form.is_valid():
        form.save()
        messages.success(request,"Araba başarıyla eklendi.")
        return redirect("admin_cars_add")

    return render(request,"admin/admin_cars_add.html",context)

@login_required(login_url="admin")
def admin_car_delete(request,id):
    car = Car.objects.filter(id=id).first()
    car.delete()
    messages.success(request,"Araba başarıyla silindi.")
    return redirect("admin_cars_add")


@login_required(login_url="admin")
def admin_blog(request):
    blogs = Blog.objects.all()
    form = BlogForm(request.POST or None, request.FILES or None)
    context={
        "blogs":blogs,
        "form":form,
    }
    if form.is_valid():
        title_en = request.POST.get("title_en")
        content_en = request.POST.get("content_en")
        title_de = request.POST.get("title_de")
        content_de = request.POST.get("content_de")
        title_ru = request.POST.get("title_ru")
        content_ru = request.POST.get("content_ru")
        article = form.save(commit=False)
        article.title_en = title_en
        article.content_en = content_en
        article.title_de = title_de
        article.content_de = content_de
        article.title_ru = title_ru
        article.content_ru = content_ru
        article.save()
        messages.success(request,"Yazı Başarıyla Eklendi.")
        return redirect("admin_blog")
    
    return render(request,"admin/admin_blog.html",context)

@login_required(login_url="admin")
def admin_blog_delete(request,id):
    article = Blog.objects.get(id=id)
    article.delete()
    messages.success(request,"Yazı Başarıyla Silindi.")
    return redirect("admin_blog")

@login_required(login_url="admin")
def admin_blog_detail(request,id):
    article = Blog.objects.filter(id=id).first()
    form = BlogForm(request.POST or None, request.FILES or None,instance=article)
    title_en = article.title_en
    content_en = article.content_en
    title_de = article.title_de
    content_de = article.content_de
    title_ru = article.title_ru
    content_ru = article.content_ru
    context = {
        "article":article,
        "title_en":title_en,
        "content_en":content_en,
        "title_de":title_de,
        "content_de":content_de,
        "title_ru":title_ru,
        "content_ru":content_ru,
        "form":form,
    }
    if form.is_valid():
        title_en = request.POST.get("title_en")
        content_en = request.POST.get("content_en")
        title_de = request.POST.get("title_de")
        content_de = request.POST.get("content_de")
        title_ru = request.POST.get("title_ru")
        content_ru = request.POST.get("content_ru")
        article_update = form.save(commit=False)
        article_update.title_en = title_en
        article_update.content_en = content_en
        article_update.title_de = title_de
        article_update.content_de = content_de
        article_update.title_ru = title_ru
        article_update.content_ru = content_ru
        article_update.save()
        messages.success(request,"Yazı Başarıyla Güncellendi.")
        return redirect("admin_blog_detail",article.id)

    return render(request,"admin/admin_blog_detail.html",context)


@login_required(login_url="admin")
def admin_about(request):
    web_about = WebAbout.objects.filter(title="Biz Kimiz?").first()
    form = WebAboutForm(request.POST or None, request.FILES or None,instance=web_about)
    context = {
        "content":web_about.content,
        "content_en":web_about.content_en,
        "content_de":web_about.content_de,
        "content_ru":web_about.content_ru,
        "form":form,
        }
    
    if form.is_valid():
        content_en = request.POST.get("content_en")
        content_de = request.POST.get("content_de")
        content_ru = request.POST.get("content_ru")
        about_update = form.save(commit=False)
        about_update.content_en = content_en
        about_update.content_de = content_de
        about_update.content_ru = content_ru
        about_update.save()
        messages.success(request,"Başarıyla Güncellendi.")
        return redirect("admin_about")

    return render(request,"admin/admin_about.html",context)

@login_required(login_url="admin")
def admin_services(request):
    web_services = WebAbout.objects.filter(title="Hizmetlerimiz").first()
    form = WebAboutForm(request.POST or None, request.FILES or None,instance=web_services)
    context = {
        "content":web_services.content,
        "content_en":web_services.content_en,
        "content_de":web_services.content_de,
        "content_ru":web_services.content_ru,
        "form":form,
        }
    
    if form.is_valid():
        content_en = request.POST.get("content_en")
        content_de = request.POST.get("content_de")
        content_ru = request.POST.get("content_ru")
        about_update = form.save(commit=False)
        about_update.content_en = content_en
        about_update.content_de = content_de
        about_update.content_ru = content_ru
        about_update.save()
        messages.success(request,"Başarıyla Güncellendi.")
        return redirect("admin_services")

    return render(request,"admin/admin_services.html",context)


@login_required(login_url="admin")
def admin_gallery(request):
    images = Gallery.objects.all()
    form = GalleryForm(request.POST or None,request.FILES or None)
    context = {
        "images":images,
        "form":form
    }
    if form.is_valid():
        form.save()
        messages.success(request,"Resim Başarıyla Eklendi.")
        return redirect(admin_gallery)
    
    return render(request,"admin/admin_gallery.html",context)

# --------------------------------- Uygulama Kısmı -------------------------------------

@login_required(login_url="admin")
def logout(request):
    auth_logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız.")
    return redirect("index")

def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response

def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)

def about(request):
    web_about = WebAbout.objects.filter(title="Biz Kimiz?").first()
    context={
        "about":web_about,
    } 
    return render(request,"about.html",context)

def services(request):
    web_about = WebAbout.objects.filter(title="Hizmetlerimiz").first()
    context={
        "services":web_about.content
    }
    return render(request,"services.html",context)

def vip_transfer_with_driver(request):
    vip_about = WebAbout.objects.filter(title="Özel Sürücülü").first()
    context={
        "content":vip_about.content
    }
    return render(request,"vip_transfer_with_driver.html",context)

def shuttle_transfer(request):
    shuttle_about = WebAbout.objects.filter(title="Paylaşımlı").first()
    context={
        "content":shuttle_about.content
    }
    return render(request,"shuttle_transfer.html",context)

def gallery(request):
    return render(request,"gallery.html")

def index(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer=form.save()
            id = transfer.id
            return redirect("carcall",id=id)
    if request.method == "GET":
        #ilk 4 resmi al sadece
        images = Gallery.objects.all()[:4]
        article_one = HomePageArticleOne.objects.all() 
        articles_two = HomePageArticleTwo.objects.all()
        car_antalya = Car.objects.filter(Q(towhere__name="Antalya Şehir Merkezi")| 
                                        Q(towhere__name_en="Antalya City Center")|
                                        Q(towhere__name_de="Stadtzentrum von Antalya")|
                                        Q(towhere__name_ru="Antalya Центр Анталии")
                                        ).order_by('price').first()
        car_alanya = Car.objects.filter(Q(towhere__name="Alanya Şehir Merkezi")| 
                                        Q(towhere__name_en="Alanya City Center")|
                                        Q(towhere__name_de="Stadtzentrum von Alanya")|
                                        Q(towhere__name_ru="Alanya Центр Алании")
                                        ).order_by('price').first()
        form = TransferForm()
    context={
        "form":form,
        "car_antalya":car_antalya.price,
        "car_alanya":car_alanya,
        "article_one":article_one,
        "articles_two":articles_two,
        "images":images
    }
    
    return render(request,"index.html",context) 
  
#populer yerler
def antalya(request):
    return render(request,"antalya.html")

def alanya(request):
    return render(request,"alanya.html")

def side(request):
    return render(request,"side.html")

def blog(request):
    articles = Blog.objects.all()
    return render(request,"blog.html",{"articles":articles})

def blog_detail(request,id):
    article = Blog.objects.get(id=id)
    return render(request,"blog_detail.html",{"article":article})


def carcall(request,id):
    transfer = Transfer.objects.filter(id =id).first()
    fromwhere = transfer.fromwhere
    towhere = transfer.towhere
    adult = transfer.adultnumber
    children = transfer.childrennumber
    total_people = int(adult)+int(children)
    cars = Car.objects.filter(Q(fromwhere=fromwhere)& 
                              Q(towhere = towhere)& 
                              Q(max_people__gte = total_people)
                              ).order_by('max_people')
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer=form.save()
            id = transfer.id
            return redirect("carcall",id=id)
    if request.method == "GET":
        form = TransferForm()
        context ={
            "form":form,
            "cars":cars,
            "transfer_id":id,
            "fromwhere":fromwhere.name,
            "towhere":towhere.name,
            }
          
        return render(request,"carcall.html",context)



def extras_list(i_name):
    extras = Extras.objects.all()
    liste=list()
    obj_tr = Extras.objects.filter(name_tr=i_name).first()
    obj_en = Extras.objects.filter(name_en=i_name).first()
    obj_de = Extras.objects.filter(name_de=i_name).first()
    obj_ru = Extras.objects.filter(name_ru=i_name).first()
    if obj_tr:
        obj_price = obj_tr.price
        for i in range(1,11):
            w_p = obj_price*i
            liste.append(w_p)
    if obj_en:
        obj_price = obj_en.price
        for i in range(1,11):
            w_p = obj_price*i
            liste.append(w_p)
    if obj_de:
        obj_price = obj_de.price
        for i in range(1,11):
            w_p = obj_price*i
            liste.append(w_p)
    if obj_ru:
        obj_price = obj_ru.price
        for i in range(1,11):
            w_p = obj_price*i
            liste.append(w_p)
    return liste

"""
def extras_list(i_name):
    extras = Extras.objects.all()
    liste=list()
    obj = Extras.objects.filter(name=i_name).first()
    obj_price = obj.price
    for i in range(1,11):
        w_p = obj_price*i
        liste.append(w_p)
    return liste
"""

def extras_name(name):
    extras_name = Extras.objects.get(name_tr=name)
    return extras_name.name

def extras_name_en(name):
    extras_name = Extras.objects.get(name_en=name)
    return extras_name.name

def extras_name_de(name):
    extras_name= Extras.objects.get(name_de=name)
    return extras_name.name

def random_string():
    l_chars = string.ascii_lowercase
    u_chars =string.ascii_uppercase
    d_chars = string.digits
    deger = l_chars+u_chars+d_chars
    data = random.sample(deger,6)
    numara = "".join(data)
    return numara


#Rezervasyon kısmı olunca güncelle
def reservation(request,transfer_id,car_id):
    extras = Extras.objects.all()
    water_list = extras_list("Su")
    beer_list = extras_list("Bira")
    wine_list = extras_list("Şarap")
    drink_list= extras_list("İçecek")
    baby_list = extras_list("Bebek Koltuğu")
    extras_su = extras_name("Su")
    extras_bira = extras_name("Bira")
    extras_sarap = extras_name("Şarap")
    extras_icecek = extras_name("İçecek")
    extras_baby = extras_name("Bebek Koltuğu")
    extras_name_list = list()
    extras_name_list.append(extras_su)
    extras_name_list.append(extras_bira)
    extras_name_list.append(extras_sarap)
    extras_name_list.append(extras_icecek)
    extras_name_list.append(extras_baby)

    car = Car.objects.filter(id=car_id).first()
    transfer = Transfer.objects.filter(id=transfer_id).first()
    people = int(transfer.adultnumber) + int(transfer.childrennumber)+1
    form = ReservationForm(request.POST or None)

    context={
        "form":form,
        "car":car,
        "water_list":water_list,
        "beer_list":beer_list,
        "wine_list":wine_list,
        "drink_list":drink_list,
        "baby_list":baby_list,
        "extras":extras,
        "transfer":transfer,
        'people' : range(1,people), 
    }

    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.IdCar_id = car_id

        people_name = " "
        for i in range(1,people):
            people_name += "' " + request.POST.get("person"+str(i)) + "'" + "\n"
        reservation.anothername = people_name #kişilerin bilgisi
        reservation.another_traveller = _(" Yetişkin Sayısı:")+" "+transfer.adultnumber +"\n"+ _("Çocuk Sayısı:")+" "+transfer.childrennumber

        id_status = request.POST.get('id_status')
        if id_status == "on":
            if request.POST.get('id_messages') == None and request.POST.get('id_specialrequest') == None :
                messages.info(request,_("Lütfen 'Özel karşılama istiyorum' kısmını doldurunuz!") )
                return render(request,"reservation.html",context)
            reservation.messages = request.POST.get('id_messages')
            reservation.specialrequest = request.POST.get('id_specialrequest')

        return_date = request.POST.get('return_date')
        if return_date == "on":
            if request.POST.get('date_of_return') == None or request.POST.get('time_of_return') == None or request.POST.get('flightnumber_of_return') == "-":
                messages.info(request,_("Lütfen 'Dönüş Transferi Ekleme' kısmını eksiksiz doldurunuz!") )
                return render(request,"reservation.html",context)
            reservation.date_of_return = request.POST.get('date_of_return')
            reservation.time_of_return = request.POST.get('time_of_return')
            reservation.flightnumber_of_return = request.POST.get('flightnumber_of_return')
        if return_date != "on":
            reservation.date_of_return = "2023-01-01"
            reservation.time_of_return = "00:00"
            reservation.flightnumber_of_return = "-"
            

        #extras_list_total = list()
        extras_total = " "
        extras_toplam = 0
        for i in extras_name_list:
            if i == "Su" or i == "Water" or i =="Wasser" or i == "Этот": 
                if request.POST.get(i) == "0":
                    pass
                else:
                    a= "'" + i + ":" + " " + str(request.POST.get(i)) + _(" adet")  + "'" +"\n" 
                    extras_total += a

            elif i != "Su" or i !="Water" or i!="Wasswe" or i!= "Этот":       
                extra = Extras.objects.filter(name=i).first()
                if extra:
                    fiyat = extra.price
                extra_en = Extras.objects.filter(name_en=i).first()
                if extra_en:
                    fiyat = extra.price
                else:
                    pass
                extra_de = Extras.objects.filter(name_de =i).first()
                if extra_de:
                    fiyat = extra.price
                else:
                    pass

                if request.POST.get(i) == "0":
                    pass
                else:
                    extras_toplam += int(request.POST.get(i))  #ekstraların toplam fiyatını bulmak için
                    deger = str((int(request.POST.get(i))) / int(fiyat))
                    if deger.endswith(".0") == True:
                        deger = deger.rstrip(".0")
                        a= "'" + i + ":" + " " + deger + _(" adet") + "'"+"\n" 
                        extras_total += a

        reservation.extras = extras_total  #ekstraları ekleme
        
        """
        #fatura kısmı
        mail_list = list()
        fatura_checkbox = request.POST.get("bill")

        if fatura_checkbox == "on":
            reservation.mail_choices = "İstek oluşturulmuş"
       """
        
        #fatura kısmı deneme
        return_bill = request.POST.get('return_bill')
        if return_bill == "on":
            if request.POST.get('bireysel_name') != "" and request.POST.get('bireysel_adress') == "":
                messages.info(request,_("Lütfen 'Bireysel Fatura' kısmını doldurunuz!") )
                return render(request,"reservation.html",context)
            if request.POST.get('bireysel_name') == "" and request.POST.get('bireysel_adress') != "":
                messages.info(request,_("Lütfen 'Bireysel Fatura' kısmını doldurunuz!") )
                return render(request,"reservation.html",context)
            if request.POST.get('kurumsal_firma_name') != "" and request.POST.get('kurumsal_vergi_no') == "" and request.POST.get('kurumsal_vergi_daire') == "" and request.POST.get('kurumsal_adress') == "" :
                messages.info(request,_("Lütfen 'Kurumsal Fatura' kısmını doldurunuz!") )
                return render(request,"reservation.html",context)
            if request.POST.get('kurumsal_firma_name') == "" and request.POST.get('kurumsal_vergi_no') != "" and request.POST.get('kurumsal_vergi_daire') == "" and request.POST.get('kurumsal_adress') == "" :
                messages.info(request,_("Lütfen 'Kurumsal Fatura' kısmını doldurunuz!") )
                return render(request,"reservation.html",context)
            if request.POST.get('kurumsal_firma_name') == "" and request.POST.get('kurumsal_vergi_no') == "" and request.POST.get('kurumsal_vergi_daire') != "" and request.POST.get('kurumsal_adress') == "" :
                messages.info(request,_("Lütfen 'Kurumsal Fatura' kısmını doldurunuz!") )
                return render(request,"reservation.html",context)
            if request.POST.get('bireysel_name') != "" and request.POST.get('bireysel_adress') != "" and request.POST.get('kurumsal_firma_name') != "" and request.POST.get('kurumsal_vergi_no') != "" and request.POST.get('kurumsal_vergi_daire') != "" and request.POST.get('kurumsal_adress') != "" :
                messages.info(request,_("Lütfen sadece bir fatura türü seçiniz!") )
                return render(request,"reservation.html",context)            
            else:
                if request.POST.get('bireysel_name') != "" and request.POST.get('bireysel_adress') != "":
                    reservation.mail_choices = "Bireysel"
                    reservation.mail_context = "Ad-Soyad:{}\nFatura Adresi:{}".format(request.POST.get('bireysel_name'),request.POST.get('bireysel_adress'))

                if request.POST.get('kurumsal_firma_name') != "" and request.POST.get('kurumsal_vergi_no') != "" and request.POST.get('kurumsal_vergi_daire') != "" and request.POST.get('kurumsal_adress') != "" :
                    reservation.mail_choices = "Kurumsal"
                    reservation.mail_context = "Firma Adı:{}\nVergi No:{}\nVergi Dairesi:{}\nFatura Adresi:{}".format(request.POST.get('kurumsal_firma_name'),request.POST.get('kurumsal_vergi_no'),request.POST.get('kurumsal_vergi_daire'),request.POST.get('kurumsal_adress'))


        exampleRadios = request.POST.get('exampleRadios')
        if exampleRadios == "option1":
            reservation.payment_method = "Araçta Nakit"
        if exampleRadios == "option2" :
            reservation.payment_method = "EFT/Havale"

        total_amount = extras_toplam + int(car.price) #toplam tutarı hesaplama
        reservation.total_amount = int(total_amount)

        if reservation.date == timezone.now().date():
            currentDateAndTime = datetime.now()
            currentTime = currentDateAndTime.strftime("%H:%M")
            if reservation.planetime == currentTime :
                messages.info(request,_("Uçak saatinizi lütfen kontrol ediniz!") )
                return render(request,"reservation.html",context)
             
        reservation.save()
        reservation_id = reservation.id

        numara = random_string()  #numara değeri verdik
        reserv = Reservation.objects.get(id=reservation_id)
        reserv.no = numara+str(reservation_id)
        reserv.save()

        messages.success(request,_("Rezervasyon Kaydınız Başarıyla Oluşturuldu."))
        return redirect("reservation_detail",id=reservation_id)

    return render(request,"reservation.html",context)


def reservation_detail(request,id):
    reservation = Reservation.objects.filter(id=id).first()
    car_id = reservation.IdCar.id
    car = Car.objects.filter(id=car_id).first()
    context = {
        "reservation":reservation,
        "car":car,
    }
    return render(request,"reservation_detail.html",context)

def reservation_query(request):
    form = ReservationQueryForm(request.POST or None)
    context={
        "form":form,
    }
    if form.is_valid():
        no = request.POST.get("no")
        email = request.POST.get("email")
        reservation = Reservation.objects.filter(no=no,email=email).first()
        if reservation:
            id = reservation.id
            return redirect("reservation_detail",id=id)
        else:
            messages.info(request,_("Girilen Bilgiler Yanlıştır!"))
            messages.info(request,_("Lütfen Tekrar Deneyiniz!"))
    return render(request,"reservation_query.html",context)

"""
            tur = request.POST.get("exampleRadioBill")

            if tur == None :
                messages.info(request,_("Lütfen fatura istiyorsanız 'Bireysel/Kurumsal' fatura türünü seçiniz!") )
                return render(request,"reservation.html",context)
            
            if tur == "bireysel" :
                reservation.mail_choices = "Bireysel"
                name_surname = request.POST.get("name_surname")
                tc_no = request.POST.get("tc_no")
                if name_surname == None or tc_no == None:
                    messages.info(request,_("Lütfen Bireysel Fatura kısmındaki 'Ad Soyad-TC Kimlik No' kısımlarını doldurunuz!") )
                    return render(request,"reservation.html",context)
                else:
                    name_surname = "Ad Soyad" + ": " + request.POST.get("name_surname")
                    tc_no = "TC Kimlik No " + ": " + request.POST.get("tc_no")
                    mail_list.append(name_surname)
                    mail_list.append(tc_no)
                    reservation.mail_context = mail_list

            if tur == "kurumsal":
                reservation.mail_choices = "Kurumsal"
                firma_name = request.POST.get("firma_name")
                vergi_no = request.POST.get("vergi_no")
                bill_adress = request.POST.get("bill_adress")
                if firma_name == None or vergi_no == None or bill_adress == None  :
                    messages.info(request,_("Lütfen Kurumsal Fatura kısmındaki 'Firma Ünvanı-Vergi No-Fatura Adresi' kısımlarını doldurunuz!") )
                    return render(request,"reservation.html",context)
                else:
                    firma_name = "Firma Ünvanı" ": " + request.POST.get("firma_name")
                    vergi_no = "Vergi No" + ": " + request.POST.get("vergi_no")
                    bill_adress = "Fatura Adresi" + ": " + request.POST.get("bill_adress")
                    mail_list.append(firma_name)
                    mail_list.append(vergi_no)
                    mail_list.append(bill_adress)
                    reservation.mail_context = mail_list
"""


def deneme(request,transfer_id,car_id):
    car = Car.objects.filter(id=car_id).first()
    transfer = Transfer.objects.filter(id=transfer_id).first()
    people = int(transfer.adultnumber) + int(transfer.childrennumber)+1
    extras = Extras.objects.all()
    
    water_list = extras_list("Su")
    beer_list = extras_list("Bira")
    wine_list = extras_list("Şarap")
    drink_list= extras_list("İçecek")
    baby_list = extras_list("Bebek Koltuğu")

    extras_su = extras_name("Su")
    extras_sarap = extras_name("Bira")
    extras_icecek = extras_name("Şarap")
    extras_bira = extras_name("İçecek")
    extras_baby = extras_name("Bebek Koltuğu")
    extras_name_list = list()
    extras_name_list.append(extras_su)
    extras_name_list.append(extras_bira)
    extras_name_list.append(extras_sarap)
    extras_name_list.append(extras_icecek)
    extras_name_list.append(extras_baby)

    bireysel_form = BireyselFaturaForm()
    kurumsal_form = KurumsalFaturaForm()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        context={
            "bireysel_fatura_form":bireysel_form,
            "kurumsal_fatura_form":kurumsal_form,
            "form":form,
            "car":car,
            "water_list":water_list,
            "beer_list":beer_list,
            "wine_list":wine_list,
            "drink_list":drink_list,
            "baby_list":baby_list,
            "extras":extras,
            "transfer":transfer,
            'people' : range(1,people), 
            }
        
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.IdCar_id = car_id

            people_name = list()
            for i in range(1,people):
                people_name.append(request.POST.get("person"+str(i)))
            reservation.anothername = people_name #kişilerin bilgisi

            id_status = request.POST.get('id_status')
            if id_status == "on":
                if request.POST.get('id_messages') == None or request.POST.get('id_specialrequest') == None :
                    messages.info(request,"Karşıla kısmının bilgilerini doldur.")
                    return render(request,"deneme.html",context)

            extras_list_total = list()
            for i in extras_name_list:
                if i == "Su":
                    if request.POST.get(i) == "0":
                        pass
                    else:
                        a= i + ":" + " " + str(request.POST.get(i))
                        extras_list_total.append(a)

                elif i != "Su":       
                    extra = Extras.objects.filter(name=i).first()
                    fiyat = extra.price

                    if request.POST.get(i) == "0":
                        pass
                    else:
                        deger = str((int(request.POST.get(i))) / int(fiyat))
                        if deger.endswith(".0") == True:
                            deger = deger.rstrip(".0")
                            a= i + ":" + " " + deger
                            extras_list_total.append(a)

            reservation.extras = extras_list_total  #ekstraları ekleme
            mail_list = list()
            tur = request.POST.get("exampleRadioBill")

            if tur == None :
                messages.info(request,_("Lütfen fatura istiyorsanız 'Bireysel/Kurumsal' fatura türünü seçiniz!") )
                return render(request,"reservation.html",context)
            
            if tur == "bireysel" :
                reservation.mail_choices = "Bireysel"
                name_surname = request.POST.get("name_surname")
                tc_no = request.POST.get("tc_no")
                if name_surname == None or tc_no == None:
                    messages.info(request,_("Lütfen Bireysel Fatura kısmındaki 'Ad Soyad-TC Kimlik No' kısımlarını doldurunuz!") )
                    return render(request,"reservation.html",context)
                else:
                    name_surname = "Ad Soyad" + ": " + request.POST.get("name_surname")
                    tc_no = "TC Kimlik No " + ": " + request.POST.get("tc_no")
                    mail_list.append(name_surname)
                    mail_list.append(tc_no)
                    reservation.mail_context = mail_list

            if tur == "kurumsal":
                reservation.mail_choices = "Kurumsal"
                firma_name = request.POST.get("firma_name")
                vergi_no = request.POST.get("vergi_no")
                bill_adress = request.POST.get("bill_adress")
                if firma_name == None or vergi_no == None or bill_adress == None  :
                    messages.info(request,_("Lütfen Kurumsal Fatura kısmındaki 'Firma Ünvanı-Vergi No-Fatura Adresi' kısımlarını doldurunuz!") )
                    return render(request,"reservation.html",context)
                else:
                    firma_name = "Firma Ünvanı" ": " + request.POST.get("firma_name")
                    vergi_no = "Vergi No" + ": " + request.POST.get("vergi_no")
                    bill_adress = "Fatura Adresi" + ": " + request.POST.get("bill_adress")
                    mail_list.append(firma_name)
                    mail_list.append(vergi_no)
                    mail_list.append(bill_adress)
                    reservation.mail_context = mail_list
            exampleRadios = request.POST.get('exampleRadios')
            if exampleRadios == "option1":
                reservation.payment_method = "Araçta Nakit"
            if exampleRadios == "option2" :
                reservation.payment_method = "EFT/Havale"

             
            reservation.save()
            messages.success(request,"Oldu")
            return redirect("index")
    else:
        form = ReservationForm()

    context={
            "form":form,
            "car":car,
            "water_list":water_list,
            "beer_list":beer_list,
            "wine_list":wine_list,
            "drink_list":drink_list,
            "baby_list":baby_list,
            "extras":extras,
            "transfer":transfer,
            'people' : range(1,people), 
            }

    return render(request,"deneme.html",context)