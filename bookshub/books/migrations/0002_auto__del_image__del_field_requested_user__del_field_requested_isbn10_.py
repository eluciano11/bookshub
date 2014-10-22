# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Image'
        db.delete_table(u'books_image')

        # Deleting field 'Requested.user'
        db.delete_column(u'books_requested', 'user_id')

        # Deleting field 'Requested.isbn10'
        db.delete_column(u'books_requested', 'isbn10')

        # Deleting field 'Requested.isbn13'
        db.delete_column(u'books_requested', 'isbn13')

        # Adding field 'Requested.isbn_10'
        db.add_column(u'books_requested', 'isbn_10',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'Requested.isbn_13'
        db.add_column(u'books_requested', 'isbn_13',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=13, blank=True),
                      keep_default=False)

        # Adding field 'Requested.count'
        db.add_column(u'books_requested', 'count',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)

        # Adding M2M table for field user on 'Requested'
        m2m_table_name = db.shorten_name(u'books_requested_user')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('requested', models.ForeignKey(orm[u'books.requested'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['requested_id', 'user_id'])

        # Deleting field 'Book.description'
        db.delete_column(u'books_book', 'description')

        # Deleting field 'Book.end_date'
        db.delete_column(u'books_book', 'end_date')

        # Deleting field 'Book.start_date'
        db.delete_column(u'books_book', 'start_date')

        # Deleting field 'Book.owner'
        db.delete_column(u'books_book', 'owner_id')

        # Deleting field 'Book.price'
        db.delete_column(u'books_book', 'price')

        # Deleting field 'Book.condition'
        db.delete_column(u'books_book', 'condition')

        # Deleting field 'Book.quantity'
        db.delete_column(u'books_book', 'quantity')

        # Adding field 'Book.score'
        db.add_column(u'books_book', 'score',
                      self.gf('django.db.models.fields.FloatField')(default=0.0, null=True),
                      keep_default=False)

        # Adding field 'Book.image'
        db.add_column(u'books_book', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(default='hi.png', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Image'
        db.create_table(u'books_image', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
        ))
        db.send_create_signal(u'books', ['Image'])

        # Adding field 'Requested.user'
        db.add_column(u'books_requested', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['users.User']),
                      keep_default=False)

        # Adding field 'Requested.isbn10'
        db.add_column(u'books_requested', 'isbn10',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'Requested.isbn13'
        db.add_column(u'books_requested', 'isbn13',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Deleting field 'Requested.isbn_10'
        db.delete_column(u'books_requested', 'isbn_10')

        # Deleting field 'Requested.isbn_13'
        db.delete_column(u'books_requested', 'isbn_13')

        # Deleting field 'Requested.count'
        db.delete_column(u'books_requested', 'count')

        # Removing M2M table for field user on 'Requested'
        db.delete_table(db.shorten_name(u'books_requested_user'))

        # Adding field 'Book.description'
        db.add_column(u'books_book', 'description',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=140),
                      keep_default=False)

        # Adding field 'Book.end_date'
        db.add_column(u'books_book', 'end_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Book.start_date'
        db.add_column(u'books_book', 'start_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 10, 22, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Book.owner'
        db.add_column(u'books_book', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['users.User']),
                      keep_default=False)

        # Adding field 'Book.price'
        db.add_column(u'books_book', 'price',
                      self.gf('django.db.models.fields.DecimalField')(default=1.1, max_digits=5, decimal_places=2),
                      keep_default=False)

        # Adding field 'Book.condition'
        db.add_column(u'books_book', 'condition',
                      self.gf('django.db.models.fields.CharField')(default='new', max_length=10),
                      keep_default=False)

        # Adding field 'Book.quantity'
        db.add_column(u'books_book', 'quantity',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'Book.score'
        db.delete_column(u'books_book', 'score')

        # Deleting field 'Book.image'
        db.delete_column(u'books_book', 'image')


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
        u'books.requested': {
            'Meta': {'ordering': "('-modified_at', '-created_at')", 'object_name': 'Requested'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'count': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_data': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn_10': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'isbn_13': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'requested'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.User']", 'symmetrical': 'False'})
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
            'token_version': ('django.db.models.fields.CharField', [], {'default': "'bf335f95-6b7e-41cc-91a4-24d6c023e881'", 'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'twitter_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['books']