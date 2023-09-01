from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import index, MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView,\
    MailingDeleteView, stopped, forcibly_send, LogsListView

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('mailing-list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing'),
    path('create/mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('update/mailing/<int:pk>', MailingUpdateView.as_view(), name='update_mailing'),
    path('delete/mailing/<int:pk>', MailingDeleteView.as_view(), name='delete_mailing'),
    path('list/logs/', LogsListView.as_view(), name='logs_list'),
    path('state/mailing/<int:pk>', stopped, name='stopped_mailing'),
    path('send/<int:pk>', forcibly_send, name='send_mailing'),
]
