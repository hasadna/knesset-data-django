# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KnessetPerson'
        db.create_table(u'kns_persons_knessetperson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_id', self.gf('django.db.models.fields.IntegerField')()),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('gender_id', self.gf('django.db.models.fields.IntegerField')()),
            ('gender_description', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('is_current', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'kns_persons', ['KnessetPerson'])

        # Adding model 'KnessetPosition'
        db.create_table(u'kns_persons_knessetposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_id', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('gender_id', self.gf('django.db.models.fields.IntegerField')()),
            ('gender_description', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'kns_persons', ['KnessetPosition'])

        # Adding model 'KnessetPersonToPosition'
        db.create_table(u'kns_persons_knessetpersontoposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_id', self.gf('django.db.models.fields.IntegerField')()),
            ('person_id', self.gf('django.db.models.fields.IntegerField')()),
            ('position_id', self.gf('django.db.models.fields.IntegerField')()),
            ('knesset_num', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ministry_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ministry_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('duty_description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('faction_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('faction_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('gov_num', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('committee_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('committee_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('start_update', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('finish_update', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_current', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'kns_persons', ['KnessetPersonToPosition'])

        # Adding model 'KnessetSiteCode'
        db.create_table(u'kns_persons_knessetsitecode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_id', self.gf('django.db.models.fields.IntegerField')()),
            ('kns_id', self.gf('django.db.models.fields.IntegerField')()),
            ('site_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'kns_persons', ['KnessetSiteCode'])


    def backwards(self, orm):
        # Deleting model 'KnessetPerson'
        db.delete_table(u'kns_persons_knessetperson')

        # Deleting model 'KnessetPosition'
        db.delete_table(u'kns_persons_knessetposition')

        # Deleting model 'KnessetPersonToPosition'
        db.delete_table(u'kns_persons_knessetpersontoposition')

        # Deleting model 'KnessetSiteCode'
        db.delete_table(u'kns_persons_knessetsitecode')


    models = {
        u'kns_persons.knessetperson': {
            'Meta': {'object_name': 'KnessetPerson'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'gender_description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'gender_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {}),
            'source_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'kns_persons.knessetpersontoposition': {
            'Meta': {'object_name': 'KnessetPersonToPosition'},
            'committee_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'committee_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'duty_description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'faction_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'faction_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'finish_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gov_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'knesset_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ministry_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ministry_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'person_id': ('django.db.models.fields.IntegerField', [], {}),
            'position_id': ('django.db.models.fields.IntegerField', [], {}),
            'source_id': ('django.db.models.fields.IntegerField', [], {}),
            'start_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'kns_persons.knessetposition': {
            'Meta': {'object_name': 'KnessetPosition'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'gender_description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'gender_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {}),
            'source_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'kns_persons.knessetsitecode': {
            'Meta': {'object_name': 'KnessetSiteCode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kns_id': ('django.db.models.fields.IntegerField', [], {}),
            'site_id': ('django.db.models.fields.IntegerField', [], {}),
            'source_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['kns_persons']