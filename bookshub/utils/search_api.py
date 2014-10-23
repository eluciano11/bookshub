import urllib2
import json

from django.conf import settings

isbndb_url = 'http://isbndb.com/api/v2/json/' + str(
    settings.ISBNDB_API_KEY) + '/'


class SearchWrapper:

    def search_isbndb_api(self, search_by, value):

        final_url = None
        search = search_by.lower()

        if search == 'isbn_13' or search == 'isbn_10':
            final_url = isbndb_url + 'book/' + str(value)
        elif search == 'title':
            title = value.replace(' ', '+')
            final_url = isbndb_url + 'books?q=' + str(title)
        elif search == 'author':
            print 'hello'
            author = value.replace(' ', '+')
            final_url = isbndb_url + 'books?q=' + str(
                author) + '&i=author_name'

        print final_url
        if final_url:
            request = urllib2.urlopen(final_url)
            data = json.load(request)
            return create_json(data, search_by)


def create_json(data, search_by):
    data_list = []

    for d in data['data']:
        author = []

        if d['author_data']:
            print 'aqui'
            for a in d['author_data']:
                author.append(a['name'])

        print 'hello ' + str(search_by.lower() == 'author')
        print author
        print 'is there an author? ' + str(len(author))

        if search_by.lower() == 'author' and len(author) > 0:
            info = {
                'author': author,
                'title': d['title'],
                'isbn_10': d['isbn10'],
                'isbn_13': d['isbn13'],
                'publisher': d['publisher_name'],
                'edition': d['edition_info']
            }
            data_list.append(info)

        elif search_by.lower() != 'author':
            info = {
                'author': author,
                'title': d['title'],
                'isbn_10': d['isbn10'],
                'isbn_13': d['isbn13'],
                'publisher': d['publisher_name'],
                'edition': d['edition_info']
            }
            data_list.append(info)

        json_format = json.dumps(data_list)

    return json_format
