from django.urls import path
from . import views
app_name= 'todo'
urlpatterns = [
   path('', views.home,name='home'),
   path('signup/',views.signupuser,name='signupuser'),
   path('login/',views.loginuser,name='loginuser'),
   path('logout/',views.logoutuser,name='logoutuser'),

   path('create/',views.createtodo,name='createtodo'),
   path('current/',views.currenttodos,name='currenttodos'),
   path('completed/',views.completedtodos,name='completedtodos'),
   path('<int:id>/',views.viewtodo,name='viewtodo'),
   path('<int:id>/complete/',views.completetodo,name='completetodo'),
   path('<int:id>/delete/',views.deletetodo,name='deletetodo'),
]