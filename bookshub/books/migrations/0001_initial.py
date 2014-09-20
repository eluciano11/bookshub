# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'books_category', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
        ))
        db.send_create_signal(u'books', ['Category'])

        # Adding model 'Book'
        db.create_table(u'books_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Category'])),
            ('isbn_10', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('isbn_13', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('quantity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal(u'books', ['Book'])

        # Adding model 'Review'
        db.create_table(u'books_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
            ('review', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'books', ['Review'])

        # Adding model 'Image'
        db.create_table(u'books_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'books', ['Image'])

        # Adding model 'Viewed'
        db.create_table(u'books_viewed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
        ))
        db.send_create_signal(u'books', ['Viewed'])

        # Adding model 'Requested'
        db.create_table(u'books_requested', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='requested', max_length=10)),
            ('isbn10', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('isbn13', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('extra_data', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'books', ['Requested'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'books_category')

        # Deleting model 'Book'
        db.delete_table(u'books_book')

        # Deleting model 'Review'
        db.delete_table(u'books_review')

        # Deleting model 'Image'
        db.delete_table(u'books_image')

        # Deleting model 'Viewed'
        db.delete_table(u'books_viewed')

        # Deleting model 'Requested'
        db.delete_table(u'books_requested')


    models = {
        u'books.book': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['books.Category']"}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn_10': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'isbn_13': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'quantity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'books.category': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'})
        },
        u'books.image': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Image'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['books.Book']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'books.requested': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Requested'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_data': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn10': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'isbn13': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'requested'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'books.review': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Review'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['books.Book']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'review': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'books.viewed': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Viewed'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['books.Book']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
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
            'token_version': ('django.db.models.fields.CharField', [], {'default': "'224c0cbe-d94d-4246-ab19-66d1bdb92481'", 'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'twitter_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['books']