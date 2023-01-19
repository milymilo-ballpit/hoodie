from django.urls import path, re_path
from .views import GrabView, GrabAjaxView, LinkListView, EntryDetailView, CreateLinkView, IndexRedirectView, DownloadEntryView

app_name = 'app'

urlpatterns = [
    # link explorer
    path("", IndexRedirectView.as_view(), name="index"),
    path("links/", LinkListView.as_view(), name="link_list"),
    path("create/", CreateLinkView.as_view(), name="create_link"),
    path("entry/<int:pk>", EntryDetailView.as_view(), name="entry_detail"),
    path("download/<int:pk>.json", DownloadEntryView.as_view(), name="entry_download"),
    path("a/<str:correlation_id>", GrabAjaxView.as_view(), name="grab_ajax"),

    # this wildcard has to be last
    re_path(r"^(?P<inbound>.*)/?$", GrabView.as_view(), name="grab"),
]
