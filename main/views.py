from django.views.generic import TemplateView
from devices.models import *
from network.models import *
from reversion.models import Version
import datetime
from django.contrib.contenttypes.models import ContentType
from main.models import DashboardWidget, widgets

class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['device_all'] = Device.objects.all().count()
            context['device_available'] = Device.objects.filter(currentlending=None).count()
            context['ipaddress_all'] = IpAddress.objects.all().count()
            context['ipaddress_available'] = IpAddress.objects.filter(device=None).count()
            context['revisions'] = Version.objects.filter(content_type_id=ContentType.objects.get(model='device').id).order_by("-pk")[:20]
            context['newest_devices'] = Device.objects.all().order_by("-pk")[:10]
            context["today"] = datetime.date.today()
            context["overdue"] = Device.objects.filter(currentlending__duedate__lt = context["today"]).order_by("currentlending__duedate")
            context["widgets_left"] = DashboardWidget.objects.filter(user=self.request.user, column="l").order_by("index")
            context["widgets_right"] = DashboardWidget.objects.filter(user=self.request.user, column="r").order_by("index")
            userwidget_list = dict(widgets)
            for w in context["widgets_left"]:
                del userwidget_list[w.widgetname]

            for w in context["widgets_right"]:
                del userwidget_list[w.widgetname]
            context["widgets_list"] = userwidget_list
        return context