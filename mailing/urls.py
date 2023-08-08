from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import index, ContentListView, ContentDetailView, ContentCreateView

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('mailing-list/', ContentListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', ContentDetailView.as_view(), name='mailing'),
    path('create_mailing/', ContentCreateView.as_view(), name='create_mailing'),
]
