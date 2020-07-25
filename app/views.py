import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.decorators.csrf import csrf_exempt

from ua_parser import user_agent_parser
from ipware import get_client_ip
from .models import Link, Entry


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry


class LinkUpdateView(LoginRequiredMixin, UpdateView):
    model = Link
    fields = ['name', 'description', 'inbound', 'outbound']


class LinkListView(LoginRequiredMixin, ListView):
    model = Link


class CreateLinkView(LoginRequiredMixin, CreateView):
    model = Link
    fields = ['name', 'description', 'inbound', 'outbound']


class GrabView(View):
    def get(self, request, *args, **kwargs):
        link = get_object_or_404(Link, inbound=self.kwargs['inbound'])

        data = {
            "headers": {},
            "cookies": [],
            "browser": {}
        }

        for key in request.headers:
            if key == "Cookie":
                data["cookies"] = list(map(
                    lambda x: x.strip(), request.headers[key].split(';')
                ))
                continue

            data["headers"][key] = request.headers[key]

        ip, _ = get_client_ip(request, request_header_order=['X-Real-IP'])
        data['ipAddress'] = ip
        data['userAgent'] = user_agent_parser.Parse(
            data['headers'].get("User-Agent", "")
        )

        entry = Entry(link=link, data=data)
        entry.save()
        return render(request, "app/grab.html", context={"correlation_id": entry.correlation_id})


@method_decorator(csrf_exempt, name='dispatch')
class GrabAjaxView(View):

    def post(self, request, *args, **kwargs):
        entry = Entry.objects.get(correlation_id=self.kwargs['correlation_id'])
        if not entry.has_browser_data:
            data = json.loads(request.body.decode("utf-8"))
            entry.data['browser'] = data
            entry.has_browser_data = True
            entry.save()

        return JsonResponse({"status": "ok", "forward": entry.link.outbound})
