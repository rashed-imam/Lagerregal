# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailTemplate'
        db.create_table(u'mail_mailtemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('usage', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'mail', ['MailTemplate'])

        # Adding model 'MailHistory'
        db.create_table(u'mail_mailhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mailtemplate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mail.MailTemplate'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('sent_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Lageruser'])),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['devices.Device'], null=True)),
        ))
        db.send_create_signal(u'mail', ['MailHistory'])


    def backwards(self, orm):
        # Deleting model 'MailTemplate'
        db.delete_table(u'mail_mailtemplate')

        # Deleting model 'MailHistory'
        db.delete_table(u'mail_mailhistory')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'devicegroups.devicegroup': {
            'Meta': {'object_name': 'Devicegroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'devices.building': {
            'Meta': {'object_name': 'Building'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        u'devices.device': {
            'Meta': {'object_name': 'Device'},
            'archived': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'bildnumber': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Lageruser']"}),
            'currentlending': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'currentdevice'", 'null': 'True', 'to': u"orm['devices.Lending']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'devicetype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['devicetypes.Type']", 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'devices'", 'null': 'True', 'to': u"orm['devicegroups.Devicegroup']"}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macaddress': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['devices.Manufacturer']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['devices.Room']", 'null': 'True', 'blank': 'True'}),
            'serialnumber': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'templending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'webinterface': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'})
        },
        u'devices.lending': {
            'Meta': {'object_name': 'Lending'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['devices.Device']"}),
            'duedate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'duedate_email': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lenddate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Lageruser']"}),
            'returndate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'devices.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'devices.room': {
            'Meta': {'object_name': 'Room'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['devices.Building']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'devicetypes.type': {
            'Meta': {'object_name': 'Type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'mail.mailhistory': {
            'Meta': {'object_name': 'MailHistory'},
            'body': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['devices.Device']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailtemplate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mail.MailTemplate']"}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sent_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Lageruser']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'mail.mailtemplate': {
            'Meta': {'object_name': 'MailTemplate'},
            'body': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'usage': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'users.lageruser': {
            'Meta': {'object_name': 'Lageruser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'de'", 'max_length': '10', 'null': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'pagelength': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['mail']