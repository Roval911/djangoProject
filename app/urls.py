from django.urls import path
from .views import *

urlpatterns = [
    path('buy/<int:item_id>/', get_checkout_session, name='get_checkout_session'),
    path('item/<int:item_id>/', view_item, name='view_item'),
    path('create_order/<int:item_id>/', create_order, name='create_order'),
    path('order/<int:order_id>/', view_order, name='view_order'),
]