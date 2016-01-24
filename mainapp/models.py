from django.db import models
from django.contrib.auth.models import User

class Adres(models.Model):
	ulica = models.TextField()
	nr_budynku = models.IntegerField()
	nr_domu = models.IntegerField()

class Wspolrzedne(models.Model):
	wsp_x = models.FloatField()
	wsp_y = models.FloatField()

class Miasta(models.Model):
	miasto = models.TextField()
	wspolrzedne = models.ForeignKey(Wspolrzedne)

class Atrakcja(models.Model):
	miasto = models.ForeignKey(Miasta)
	miastoto = models.TextField()
	typ = models.TextField()
	nazwa = models.TextField()
	adres = models.ForeignKey(Adres)
	czas_otwarcia = models.TimeField()
	czas_zamkniecia = models.TimeField()
	czas = models.FloatField()
	cena = models.FloatField()
	opis = models.TextField()
	wspolrzedne = models.ForeignKey(Wspolrzedne)

class Koszyk(models.Model):
	nazwa = models.TextField()
	uzytkownik = models.ForeignKey(User)
	atrakcje = models.ManyToManyField(Atrakcja)
