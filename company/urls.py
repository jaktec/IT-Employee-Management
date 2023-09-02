from django.urls import include, path

from .views import company, developers, teamleads

urlpatterns = [
    path('', company.home, name='home'),

    path('developers/', include(([

    ], 'company'), namespace='developers')),

    path('teamleads/', include(([


    ], 'company'), namespace='teamleads')),
]
