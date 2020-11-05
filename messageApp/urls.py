from . import views
from django.urls import path, include

urlpatterns = [

    path('write/', views.writeMessage),
    path('all/', views.getAllMessages),
    path('unread/', views.getUnreadMessages),
    path('delete/', views.deleteMessage),
    path('read/', views.readMessage),
]
