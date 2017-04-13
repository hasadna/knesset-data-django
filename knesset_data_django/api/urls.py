try:
	from django.conf.urls import patterns, include, url
except ImportError:
	from django.conf.urls.defaults import patterns, include, url

from ..mks.views import GetAllMkNamesView

urlpatterns = patterns('',
    url(r'^get_all_mk_names.json$', GetAllMkNamesView.as_view(), name='get_all_mk_names'),
)
