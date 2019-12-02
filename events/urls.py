from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import EventListView, EventDetailView, EventDeleteView, EventUpdateView,\
                   EventCreateView, MyEventListView, TagCreateView, TagUpdateView,invitation, invitation_cancellation, EventSearchView

app_name = "events"
urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('search', EventSearchView.as_view(), name='search'),
    path('my_events/', MyEventListView.as_view(), name='my_events'),
    path('<int:pk>/', EventDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', login_required(EventDeleteView.as_view()), name='delete'),
    path('<int:pk>/edit/', login_required(EventUpdateView.as_view()), name='update'),
    path('<int:pk>/invitation/',invitation,name='invitation'),
    path('<int:pk>/cancel_invitation/<int:pk2>',invitation_cancellation,name='cancel_invitation'),
    path('create/', login_required(EventCreateView.as_view()), name='create'),
    path('tag/', TagCreateView.as_view(), name='create_tag'),
    path('tag_update/', TagUpdateView.as_view(), name='update_tag'),
]
