from django.views.generic.base import TemplateView
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import library_view, item_view, profile_view, user_items_view
from .views import user_holds_view, user_reserves_view
from .views import search, reserve_item, request_hold, return_item, rent_item, renew_item

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('library/', library_view, name='library'),
    path('library/results/', search, name='search'),
    path('library/<slug:item_slug>/', item_view, name='item'),
    path('profile/', profile_view, name='profile'),
    path('profile/borrowed/', user_items_view, name='borrowed'),
    path('profile/pending-holds/', user_holds_view, name='holds'),
    path('profile/reserves/', user_reserves_view, name='reserves'),
    path('library/<item_id>/return/', return_item, name='return_item'),
    path('library/<slug:item_slug>/rent/', rent_item, name='rent_item'),
    path('library/<item_id>/renew/', renew_item, name='renew_item'),
    path('library/<slug:item_slug>/hold/', request_hold, name='request_hold'),
    path('library/<slug:item_slug>/reserve/', reserve_item, name='reserve_item'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
