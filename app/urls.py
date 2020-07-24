from django.urls import path
from .views import GrabView, GrabAjaxView, LinkListView, EntryDetailView, CreateLinkView

app_name = 'app'

urlpatterns = [
    # link explorer
    path("l/", LinkListView.as_view(), name="link_list"),
    path("c/", CreateLinkView.as_view(), name="create_link"),
    path("e/<int:pk>", EntryDetailView.as_view(), name="entry_detail"),

    # ajax grabber input
    path("a/<str:correlation_id>",
         GrabAjaxView.as_view(), name="grab_ajax"),

    # this wildcard has to be last
    path("<str:inbound>", GrabView.as_view(), name="grab"),
]
