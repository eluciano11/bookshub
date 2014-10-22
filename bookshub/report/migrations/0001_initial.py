# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReportedUser'
        db.create_table(u'report_reporteduser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver', to=orm['users.User'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'report', ['ReportedUser'])

        # Adding M2M table for field sender on 'ReportedUser'
        m2m_table_name = db.shorten_name(u'report_reporteduser_sender')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reporteduser', models.ForeignKey(orm[u'report.reporteduser'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reporteduser_id', 'user_id'])

        # Adding model 'ReportedBook'
        db.create_table(u'report_reportedbook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'report', ['ReportedBook'])

        # Adding model 'ReportedOffer'
        db.create_table(u'report_reportedoffer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['offers.Offer'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'report', ['ReportedOffer'])


    def backwards(self, orm):
        # Deleting model 'ReportedUser'
        db.delete_table(u'report_reporteduser')

        # Removing M2M table for field sender on 'ReportedUser'
        db.delete_table(db.shorten_name(u'report_reporteduser_sender'))

        # Deleting model 'ReportedBook'
        db.delete_table(u'report_reportedbook')

        # Deleting model 'ReportedOffer'
        db.delete_table(u'report_reportedoffer')


    models = {
        u'books.book': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['books.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'isbn_10': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'isbn_13': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'books.category': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'})
        },
        u'offers.offer': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Offer'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['books.Book']"}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'report.reportedbook': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'ReportedBook'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['books.Book']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'report.reportedoffer': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'ReportedOffer'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['offers.Offer']"}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'report.reporteduser': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'ReportedUser'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'to': u"orm['users.User']"}),
            'sender': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sender'", 'symmetrical': 'False', 'to': u"orm['users.User']"})
        },
        u'users.user': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'User'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'facebook_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'google_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'token_version': ('django.db.models.fields.CharField', [], {'default': "'370122d8-32e7-4100-a1c2-6a47c9005dcf'", 'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'twitter_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['report']