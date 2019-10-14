from django.urls import path
from .views import EventListView, EventDetailView, EventDeleteView, EventUpdateView
from . import views

app_name = "events"
urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('<int:pk>/', EventDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='update'),
    path('<int:pk>/map/',views.map, name='map'),
]
