import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse_lazy


class Link(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    inbound = models.CharField(max_length=100)
    outbound = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse_lazy("app:link_list")

    def __str__(self):
        return self.name


class Entry(models.Model):
    link = models.ForeignKey(
        Link, on_delete=models.CASCADE, related_name="entries"
    )
    has_browser_data = models.BooleanField(default=False)
    correlation_id = models.UUIDField(
        default=uuid.uuid4, null=False, blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    data = JSONField()

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "entries"

    def __str__(self):
        return f"{self.link.name} #{self.id}"
