from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django_cbkarma.views.home', name='home'),
    url(r'^details$', 'django_cbkarma.views.details', name='details'),
    url(r'^init$', 'django_cbkarma.rest_api.init', name='init'),
    url(r'^update$', 'django_cbkarma.rest_api.update', name='update'),
    url(r'^histo$', 'django_cbkarma.rest_api.histo', name='histo'),
    url(r'^report$', 'django_cbkarma.rest_api.report', name='report'),
    # url(r'^django_cbkarma/', include('django_cbkarma.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
