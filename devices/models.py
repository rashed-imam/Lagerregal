import datetime

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

import reversion

from devicegroups.models import Devicegroup
from devicetypes.models import Type
from Lagerregal import utils
from locations.models import Building
from locations.models import Room
from locations.models import Section
from users.models import Department
from users.models import Lageruser


@reversion.register()
class Manufacturer(models.Model):
    name = models.CharField(_('Manufacturer'), max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse('manufacturer-detail', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('manufacturer-edit', kwargs={'pk': self.pk})


class Bookmark(models.Model):
    device = models.ForeignKey("Device", on_delete=models.CASCADE)
    user = models.ForeignKey(Lageruser, on_delete=models.CASCADE)


@reversion.register(follow=["typeattributevalue_set", ], exclude=[
    "archived", "currentlending", "inventoried", "bookmarks", "trashed",
], ignore_duplicates=True)
class Device(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    creator = models.ForeignKey(Lageruser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Name'), max_length=200)
    inventorynumber = models.CharField(_('Inventorynumber'), max_length=50, blank=True)
    serialnumber = models.CharField(_('Serialnumber'), max_length=50, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True, on_delete=models.SET_NULL)
    hostname = models.CharField(_('Hostname'), max_length=40, blank=True)
    description = models.CharField(_('Description'), max_length=10000, blank=True)
    devicetype = models.ForeignKey(Type, blank=True, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Devicegroup, blank=True, null=True, related_name="devices", on_delete=models.SET_NULL)
    webinterface = models.CharField(_('Webinterface'), max_length=60, blank=True)

    templending = models.BooleanField(default=False, verbose_name=_("For short term lending"))
    currentlending = models.ForeignKey("Lending", related_name="currentdevice", null=True, blank=True,
                                       on_delete=models.SET_NULL)

    manual = models.FileField(upload_to=utils.get_file_location, null=True, blank=True)
    contact = models.ForeignKey(Lageruser, related_name="as_contact",
                                help_text=_("Person to contact about using this device"), blank=True,
                                null=True, on_delete=models.SET_NULL)

    archived = models.DateTimeField(null=True, blank=True)
    trashed = models.DateTimeField(null=True, blank=True)
    inventoried = models.DateTimeField(null=True, blank=True)
    bookmarkers = models.ManyToManyField(Lageruser, through=Bookmark, related_name="bookmarks", blank=True)

    data_provider = models.CharField(max_length=20, blank=True)
    operating_system = models.CharField(max_length=10, choices=settings.OPERATING_SYSTEMS, null=True, blank=True)

    department = models.ForeignKey(Department, null=True, blank=True, related_name="devices", on_delete=models.SET_NULL)
    is_private = models.BooleanField(default=False)
    used_in = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        permissions = (
            ("boss_mails", _("Emails for bosses")),
            ("managment_mails", _("Emails for managment")),
            ("support_mails", _("Emails for support")),
            ("lend_device", _("Can lend Device")),
            ("view_devicedetails", _("View Device Details"))
        )

    def get_absolute_url(self):
        return reverse('device-detail', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('device-edit', kwargs={'pk': self.pk})

    def get_as_dict(self):
        dict = {}
        dict["name"] = self.name
        dict["description"] = self.description
        dict["manufacturer"] = self.manufacturer
        dict["devicetype"] = self.devicetype
        dict["room"] = self.room
        return dict

    @property
    def is_overdue(self):
        if self.currentlending is None:
            return False
        if self.currentlending.duedate < datetime.date.today():
            return True
        return False

    @property
    def is_active(self):
        return self.archived == None and self.trashed == None

    def archive_device(self):
        self.archived = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.make_inactive()

    def trash_device(self):
        self.trashed = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.make_inactive()

    def make_inactive(self):
        self.room = None
        if self.currentlending:
            self.currentlending.returndate = datetime.date.today()
            self.currentlending.save()
            self.currentlending = None
        # if device.uses
        if Device.objects.filter(used_in=self.pk):
            other_list = Device.objects.filter(used_in=self.pk)
            for element in other_list:
                other = element
                other.used_in = None
                other.save()
        if self.used_in:
            self.used_in = None
        for ip in self.ipaddress_set.all():
            ip.device = None
            ip.save()

    @staticmethod
    def active():
        return Device.objects.filter(archived=None, trashed=None)

    @staticmethod
    def devices_for_departments(departments=[]):
        return Device.objects.filter(department__in=departments).exclude(
            ~Q(department__in=departments), is_private=True)


class DeviceInformationType(models.Model):
    keyname = models.CharField(_('Name'), max_length=200)
    humanname = models.CharField(_('Human readable name'), max_length=200)

    def __str__(self):
        return self.humanname

    class Meta:
        verbose_name = _('Information Type')
        verbose_name_plural = _('Information Type')


class DeviceInformation(models.Model):
    information = models.CharField(_('Information'), max_length=200)
    device = models.ForeignKey(Device, related_name="information", on_delete=models.CASCADE)
    infotype = models.ForeignKey(DeviceInformationType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.infotype) + ": " + self.information

    class Meta:
        verbose_name = _('Information')
        verbose_name_plural = _('Information')


@reversion.register(ignore_duplicates=True)
class Lending(models.Model):
    owner = models.ForeignKey(Lageruser, verbose_name=_("Lent to"), on_delete=models.SET_NULL, null=True)
    lenddate = models.DateField(auto_now_add=True)
    duedate = models.DateField(blank=True, null=True)
    duedate_email = models.DateField(blank=True, null=True)
    returndate = models.DateField(blank=True, null=True)
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.CASCADE)
    smalldevice = models.CharField(_("Small Device"), max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('Lending')
        verbose_name_plural = _('Lendings')


class Template(models.Model):
    templatename = models.CharField(_('Templatename'), max_length=200)
    name = models.CharField(_('Name'), max_length=200)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True, on_delete=models.CASCADE)
    description = models.CharField(_('Description'), max_length=1000, blank=True)
    devicetype = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.templatename

    class Meta:
        ordering = ['name']
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def get_absolute_url(self):
        return reverse('device-list')

    def get_as_dict(self):
        dict = {}
        dict["name"] = self.name
        dict["description"] = self.description
        dict["manufacturer"] = self.manufacturer
        dict["devicetype"] = self.devicetype
        return dict


class Note(models.Model):
    device = models.ForeignKey(Device, related_name="notes", on_delete=models.CASCADE)
    note = models.CharField(max_length=5000)
    creator = models.ForeignKey(Lageruser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    def get_absolute_url(self):
        return reverse("device-detail", kwargs={'pk': self.device.pk})


class Picture(models.Model):
    device = models.ForeignKey(Device, related_name="pictures", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=utils.get_file_location)
    caption = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _("Picture")
        verbose_name_plural = _("Pictures")

    def get_absolute_url(self):
        return reverse("device-detail", kwargs={'pk': self.device.pk})
