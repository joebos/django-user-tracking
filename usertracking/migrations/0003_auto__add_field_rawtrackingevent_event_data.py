# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'UserTrackingEvent.event_data'
        db.add_column('user_tracking_UserTrackingEvent', 'event_data', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'UserTrackingEvent.event_data'
        db.delete_column('user_tracking_UserTrackingEvent', 'event_data')


    models = {
        'user_tracking.UserTrackingEvent': {
            'Meta': {'object_name': 'UserTrackingEvent'},
            'cookie': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'event_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'raw_request': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['user_tracking']
