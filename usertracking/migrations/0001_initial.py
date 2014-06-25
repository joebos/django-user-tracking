# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TrackedUser'
        db.create_table('user_tracking_trackeduser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cookie', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('user_tracking', ['TrackedUser'])


    def backwards(self, orm):
        
        # Deleting model 'TrackedUser'
        db.delete_table('user_tracking_trackeduser')


    models = {
        'user_tracking.trackeduser': {
            'Meta': {'object_name': 'TrackedUser'},
            'cookie': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['user_tracking']
