from django.conf.urls import patterns, include, url
from django.contrib import admin
from mainapp.views import *
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'przewodnik.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	(r'', include('gmapi.urls.media')),
	(r'^$', home),
	(r'^register/$',register_page),
	(r'^login/$','django.contrib.auth.views.login'),
	(r'^logout/$',logout_page),
	(r'^mapa/$',mapa),
	url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
	(r'^planowanie/$', planowanie),
	(r'^dodaj/$', dodaj),
	(r'^koszyk/$', koszyk),
	(r'^wyswietl/$', wyswietl_koszyk),
	(r'^wyswietl_szczegoly/$', wyswietl_szczegoly),
	(r'^zapis_pdf/$', zapis_pdf),
)
