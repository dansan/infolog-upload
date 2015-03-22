# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field tags on 'Infolog'
        m2m_table_name = db.shorten_name(u'infolog_upload_infolog_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('infolog', models.ForeignKey(orm[u'infolog_upload.infolog'], null=False)),
            ('tag', models.ForeignKey(orm[u'srs.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['infolog_id', 'tag_id'])


    def backwards(self, orm):
        # Removing M2M table for field tags on 'Infolog'
        db.delete_table(db.shorten_name(u'infolog_upload_infolog_tags'))


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'infolog_upload.infolog': {
            'Meta': {'object_name': 'Infolog'},
            'client': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'ext_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'free_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srs.Game']", 'null': 'True', 'blank': 'True'}),
            'has_support_ticket': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infolog_text': ('django.db.models.fields.TextField', [], {}),
            'replay': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srs.Replay']", 'null': 'True', 'blank': 'True'}),
            'severity': ('django.db.models.fields.CharField', [], {'default': "'Normal'", 'max_length': '32', 'blank': 'True'}),
            'subscribed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscriber'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['srs.Tag']", 'symmetrical': 'False'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'infolog_uploader'", 'to': u"orm['auth.User']"})
        },
        u'srs.game': {
            'Meta': {'ordering': "['name']", 'object_name': 'Game'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'developer': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'sldb_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        u'srs.map': {
            'Meta': {'ordering': "['name']", 'object_name': 'Map'},
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'startpos': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        u'srs.mapimg': {
            'Meta': {'object_name': 'MapImg'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srs.Map']"}),
            'startpostype': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'srs.replay': {
            'Meta': {'ordering': "['-upload_date']", 'object_name': 'Replay'},
            'autohostname': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'download_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'gameID': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'gametype': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_text': ('django.db.models.fields.CharField', [], {'max_length': '513', 'db_index': 'True'}),
            'map_img': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srs.MapImg']", 'null': 'True', 'blank': 'True'}),
            'map_info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srs.Map']", 'null': 'True', 'blank': 'True'}),
            'notcomplete': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_text': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'startpostype': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['srs.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'unixTime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'versionString': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'wallclockTime': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'srs.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'})
        }
    }

    complete_apps = ['infolog_upload']