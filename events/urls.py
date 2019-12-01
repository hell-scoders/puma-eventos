from django.urls import path
from .views import EventListView, EventDetailView, EventDeleteView, EventUpdateView,\
                   EventCreateView, MyEventListView, TagCreateView, TagUpdateView

app_name = "events"
urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('my_events/', MyEventListView.as_view(), name='my_events'),
    path('<int:pk>/', EventDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='update'),
    path('create/', EventCreateView.as_view(), name='create'),
    path('tag/', TagCreateView.as_view(), name='create_tag'),
    path('tag_update/', TagUpdateView.as_view(), name='update_tag'),
]
