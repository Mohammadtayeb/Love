from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('view_profile', views.view_profile, name='view_profile'),
    path('message', views.message, name='message'),
    path('change_password', views.change_password, name='change_password'),
    path('questionnaire', views.questionnaire, name='questionnaire'),
    path('my_mismatch', views.my_mismatch, name='my_mismatch'),
    path('mismatch_prof/<int:user_id>', views.mismatch_prof, name='mismatch_prof')
]