from django.urls import path
from . import views

urlpatterns = [
    path('custom-login/', views.custom_login_view, name='custom_login'),
    path('qr/<int:offer_id>/', views.generate_qr_code, name='generate_qr_code'),
    path('redeem/<int:offer_id>/', views.redeem_offer, name='redeem_offer'),
    path('csrf/', views.get_csrf_token, name='get_csrf_token'),
]

