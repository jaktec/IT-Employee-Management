from django.urls import include, path

from .views import classroom, developers, teamleads

urlpatterns = [
    path('', classroom.home, name='home'),

    path('developers/', include(([

    ], 'classroom'), namespace='developers')),

    path('teamleads/', include(([


    ], 'classroom'), namespace='teamleads')),
]
