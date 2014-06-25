# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'TrackedUser'
        db.delete_table('user_tracking_trackeduser')

        # Adding model 'UserTrackingEvent'
        db.create_table('user_tracking_UserTrackingEvent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('cookie', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('raw_request', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('user_tracking', ['UserTrackingEvent'])


    def backwards(self, orm):
        
        # Adding model 'TrackedUser'
        db.create_table('user_tracking_trackeduser', (
            ('cookie', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_agent', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('user_tracking', ['TrackedUser'])

        # Deleting model 'UserTrackingEvent'
        db.delete_table('user_tracking_UserTrackingEvent')


    models = {
        'user_tracking.UserTrackingEvent': {
            'Meta': {'object_name': 'UserTrackingEvent'},
            'cookie': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'event_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'raw_request': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['user_tracking']
