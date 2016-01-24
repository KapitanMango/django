from django.contrib import admin

from .models import Atrakcja
from .models import Adres
from .models import Wspolrzedne
from .models import Koszyk
from .models import Miasta

admin.site.register(Atrakcja)
admin.site.register(Adres)
admin.site.register(Wspolrzedne)
admin.site.register(Koszyk)
admin.site.register(Miasta)
