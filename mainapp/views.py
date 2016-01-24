import math, random
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.auth import logout
from mainapp.forms import *
from django.shortcuts import render_to_response
from gmapi import maps
from django.http import JsonResponse
import json
from gmapi.forms.widgets import GoogleMap
from mainapp.models import Miasta, Koszyk, Atrakcja
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

def dodaj(request):
    template = get_template("planowanie.html")
    form = FormularzWyboru(request.POST)
    formm = FormularzKoszykowy(request.POST)
    uri = request.GET.get('param','');
    p = Atrakcja.objects.get(nazwa=uri)
    kk = request.session['kosz']
    k = Koszyk.objects.get(nazwa=kk)
    k.atrakcje.add(p)
    k.save()
    bb = k.atrakcje.all()
    f = request.session['miasto']
    a = Atrakcja.objects.filter(miastoto=f)
    aa = k.atrakcje.all()
    v = RequestContext(request,{'wiadomosc':'Dodano do planu!', 'form':form, 'formm':formm, 'lista_atrakcji':a, 'lista_atrakcji_w_koszyku':aa, 'nowy':kk, })
    output = template.render(v)
    return HttpResponse(output)

def planowanie(request):
    template = get_template("planowanie.html")
    form = FormularzWyboru(request.POST)
    formm = FormularzKoszykowy(request.POST)
    if form.is_valid():
        f = form.cleaned_data['miasto']
        if(f != ''):
                a = Atrakcja.objects.filter(miastoto=f)
                request.session['miasto']=f
                variables = RequestContext(request,{'form':form, 'formm':formm, 'lista_atrakcji':a,})
        else:
            variables = RequestContext(request,{'form':form, 'formm':formm})
    else:
        variables = RequestContext(request,{'form':form, 'formm':formm})
    if formm.is_valid():
        ff = formm.cleaned_data['koszyk']
        if(ff != ''):
            try:
                a = Atrakcja.objects.filter(miastoto=request.session['miasto'])
                u = request.user
                try:
                    r = Koszyk.objects.get(nazwa=ff)
                    variables = RequestContext(request, {'form':form, 'formm':formm, 'lista_atrakcji':a, 'blad':'Plan o podanej nazwie już istnieje!'})
                except:
                    k = Koszyk(nazwa=ff, uzytkownik=u)
                    k.save()
                    request.session['kosz']=k.nazwa
                    variables = RequestContext(request, {'form':form, 'formm':formm, 'lista_atrakcji':a, 'nowy':k.nazwa,})
            except:
                variables = RequestContext(request, {'form':form, 'formm':formm, 'blad':'Nie podałeś miasta, które chciałbyś zwiedzić!'})
    output = template.render(variables)
    return HttpResponse(output)

def home(request):
    template = get_template("home.html")
    variables = RequestContext(request,{'podpis':'home'})
    output = template.render(variables)
    return HttpResponse(output)

def koszyk(request):
    template = get_template("koszyk.html")
    u = request.user
    k = Koszyk.objects.filter(uzytkownik=u)
    variables = RequestContext(request,{'lista_koszykow':k})
    output = template.render(variables)
    return HttpResponse(output)

def wyswietl_koszyk(request):
    template = get_template("plan.html")
    uri = request.GET.get('param','')
    k = Koszyk.objects.get(nazwa=uri)
    l = k.atrakcje.all()
    variables = RequestContext(request,{'lista_atr':l, 'kosz':uri,})
    output = template.render(variables)
    return HttpResponse(output)

def wyswietl_szczegoly(request):
    template = get_template("szczegoly.html")
    uri = request.GET.get('param','')
    a = Atrakcja.objects.get(nazwa=uri)
    variables = RequestContext(request,{'atrakcja':a, })
    output = template.render(variables)
    return HttpResponse(output)

def mapa(request):
        template = get_template("mapa.html")
        uri = request.GET.get('param','')
        kk = Koszyk.objects.get(nazwa=uri)
        kkk = kk.atrakcje.all()
        kkko = list(kkk)
        kkkoo = kkko.pop(0)
        kkkkk = kkkoo.miastoto
        kkkkkk = Miasta.objects.get(miasto=kkkkk)
        wsp_m = kkkkkk.wspolrzedne
    	gmap = maps.Map(opts = {
        	'center': maps.LatLng(wsp_m.wsp_y, wsp_m.wsp_x),
        	'mapTypeId': maps.MapTypeId.ROADMAP,
        	'zoom': 13,
        	'mapTypeControlOptions': {
             		'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        	},
    	})

        najlepszaLista = list(kkk)
        najlepszaDlugosc = 100000
        for num in range(0, 10000):
            kopiaNajlepszej = []
            kopiaNajlepszej.extend(najlepszaLista)
            nowaLista = []
            nowaLista.append(kopiaNajlepszej.pop(0))
            ostatnie = kopiaNajlepszej.pop()
            dlugosc = len(kopiaNajlepszej)
            for numm in range(0, dlugosc):
                nrAtrakcji = kopiaNajlepszej.pop(random.randrange(0, len(kopiaNajlepszej)))
                nowaLista.append(nrAtrakcji)
            nowaLista.append(ostatnie)
            suma = 0
            for nummm in range(0, len(nowaLista)-1):
                nl1 = nowaLista[nummm]
                nl1wsp = nl1.wspolrzedne
                n = nummm+1
                nl2 = nowaLista[n]
                nl2wsp = nl2.wspolrzedne
                wynik = math.sqrt(math.pow((nl2wsp.wsp_x-nl1wsp.wsp_x),2)+math.pow((nl2wsp.wsp_y-nl1wsp.wsp_y),2))
                suma= suma + wynik
            dlugoscNowej = suma
            if dlugoscNowej<najlepszaDlugosc:
                najlepszaDlugosc=dlugoscNowej
                najlepszaLista=nowaLista
        z = 0
        nr = 1
        czas = 0
        path = []
        for ko in najlepszaLista:
            wsp = ko.wspolrzedne
            if z==0:
                l1 = maps.LatLng(wsp.wsp_y, wsp.wsp_x)
                path.append(l1)
                z = 1
            else:
                l2 = maps.LatLng(wsp.wsp_y, wsp.wsp_x)
                path.append(l2)
            czas+=ko.czas
    	    marker = maps.Marker(opts = {
        	   'map': gmap,
               'position': maps.LatLng(wsp.wsp_y, wsp.wsp_x),
               'title': ko.nazwa,
               'label': nr,
    	    })
            nr+=1
        czasd = najlepszaDlugosc*1000
        czas+=czasd
        czasy=math.ceil(czas)
        czass = math.floor(czas/60)
        czasss = czasy - czass*60
        if z==1:
            polyline = maps.Polyline(opts={'map':gmap,'path':path, 'strokeColor':'#0066cc', 'strokeWeight':3, 'strokeOpacity':1})
            context = {'form': MapForm(initial={'mapa': gmap}), 'nazwa':uri, 'lista':najlepszaLista, 'droga':czass, 'droga2':czasss}
        else:
    	       context = {'form': MapForm(initial={'mapa': gmap}), 'nazwa':uri,'lista':najlepszaLista,}
        variables = RequestContext(request,context)
        output = template.render(variables)
        return HttpResponse(output)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")

def register_page(request):
	if request.method == 'POST':
		form = FormularzRejestracji(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1'],
				email=form.cleaned_data['email']
            		)
			user.first_name = form.cleaned_data['firstname']
            		user.last_name = form.cleaned_data['lastname']
            		user.save()

			template = get_template("registration/register_success.html")
			variables = RequestContext(request,{'username':form.cleaned_data['username']})
                	output = template.render(variables)
                	return HttpResponse(output)
    	else:
		form = FormularzRejestracji()
    		template = get_template("registration/register.html")
    		variables = RequestContext(request,{'form':form})
    		output = template.render(variables)
    		return HttpResponse(output)

def zapis_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    uri = request.GET.get('param','')
    kk = Koszyk.objects.get(nazwa=uri)
    kkk = kk.atrakcje.all()
    kkko = list(kkk)
    kkkoo = kkko.pop(0)
    kkkkk = kkkoo.miastoto
    response['Content-Disposition'] = 'attachment; filename="twojplan.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    p.setFont('Arial', 15)
    p.drawString(20, 800, "Wycieczka "+kk.nazwa+" po mieście "+kkkkk)
    p.setFont('Arial', 13)
    p.drawString(20, 750, "Twoje punkty wycieczki:")
    p.setFont('Arial', 10)
    zmienna = 730
    numerek = 1
    for ko in kkk:
	p.drawString(30, zmienna, str(numerek)+".")
	p.drawString(40, zmienna, ko.nazwa)
	adres = ko.adres
     	zmienna-=15
	p.drawString(60, zmienna, "ul."+adres.ulica+" "+str(adres.nr_budynku))
	zmienna-=20
	numerek+=1
    p.showPage()
    p.save()
    return response
