# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Offer'
        db.create_table(u'offers_offer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('quantity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal(u'offers', ['Offer'])

        # Adding model 'Image'
        db.create_table(u'offers_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['offers.Offer'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'offers', ['Image'])


    def backwards(self, orm):
        # Deleting model 'Offer'
        db.delete_table(u'offers_offer')

        # Deleting model 'Image'
        db.delete_table(u'offers_image')


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
        u'offers.image': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['offers.Offer']"})
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
            'token_version': ('django.db.models.fields.CharField', [], {'default': "'ee252a35-7990-4b6c-b3ae-fd322f7ad3b7'", 'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'twitter_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['offers']