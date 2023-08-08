from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import index, MailingListView, MailingDetailView, ContentCreateView

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('mailing-list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing'),
    path('create_mailing/', ContentCreateView.as_view(), name='create_mailing'),
]
