from django.urls import path, include
from rest_framework.routers import DefaultRouter
from guestbook.api.views.users_views import UserViewSet
from guestbook.api.views.entry_views import EntryViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'entries', EntryViewSet, basename='entry')  # Register EntryViewSet for entries CRUD

urlpatterns = [
    path('', include(router.urls)),
]
