from django.urls import path
from .views import homeView,user_profile_view,UserList,cerca

urlpatterns = [
    path('',homeView.as_view(),name='homepage'),
    path('users/',UserList.as_view(),name='user_list'),
    path('user/<str:username>/',user_profile_view,name='user_profile'),
    path('cerca/',cerca,name='funzione_cerca'),
]
