# -*- coding: utf-8 -*-
from devices.models import Device, Room, Building, Manufacturer
from devicetypes.models import Type
from network.models import IpAddress
from django.utils import simplejson
from django.core.urlresolvers import reverse
from main.models import DashboardWidget, widgets, get_progresscolor
from django.db.models import Max
from django.template.loader import render_to_string
from reversion.models import Version
import datetime
from main.views import get_widget_data
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import View
from django.http import HttpResponse
from django.http import QueryDict

class WidgetAdd(View):
    def post(self, request):
        widgetname = request.POST["widgetname"]
        if widgetname in widgets:
            userwidgets = DashboardWidget.objects.filter(user=request.user)
            if len(userwidgets.filter(widgetname=widgetname)) != 0:
                return HttpResponse("")
            widget = DashboardWidget()
            widget.column = "l"
            oldindex = userwidgets.filter(column="l").aggregate(Max('index'))["index__max"]
            widget.index = oldindex + 1 if oldindex != None else 1
            widget.widgetname = widgetname
            widget.user = request.user
            widget.save()
            context = get_widget_data()
            context["usestable"] = True
            context["hidecontrols"] = True
            return HttpResponse(render_to_string('snippets/widgets/{0}.html'.format(widgetname), context))
        else:
            return HttpResponse("Error: invalid widget name")

class WidgetRemove(View):
    def post(self, request):
        widgetname = request.POST["widgetname"]
        if widgetname in widgets:
            DashboardWidget.objects.get(user=request.user, widgetname=widgetname).delete()
            return HttpResponse("")
        else:
            return HttpResponse("Error: invalid widget name")

class WidgetToggle(View):
    def post(self, request):
        widgetname = request.POST["widgetname"]
        if widgetname in widgets:
            w = DashboardWidget.objects.get(user=request.user, widgetname=widgetname)
            w.minimized = not w.minimized
            w.save()
            return HttpResponse("")
        else:
            return HttpResponse("Error: invalid widget name")

 
class WidgetMove(View):
    def post(self, request):
        userwidgets = simplejson.loads(request.POST["widgets"])
        print userwidgets, type(userwidgets)

        for widgetname, widgetattr in userwidgets.iteritems():
            if widgetname in widgets:
                w = DashboardWidget.objects.get(user=request.user, widgetname=widgetname)
                if w.index != widgetattr["index"] or w.column != widgetattr["column"]:
                    w.index = widgetattr["index"]
                    w.column = widgetattr["column"]
                    w.save()
        return HttpResponse("")