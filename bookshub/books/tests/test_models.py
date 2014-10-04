from ...utils.tests import BaseTestCase
from ..models import Category, Book


class BookModelTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()

        Category.objects.create(name='other')

        self.owner = self.user
        self.category = Category.objects.all().first()
        self.isbn_10 = '218429436'
        self.isbn_13 = '1243567087t'
        self.title = 'Big bad wolf'
        self.price = '11.11'
        self.condition = 'new'
        self.quantity = 10
        self.author = 'Me'
        self.edition = '1st'
        self.description = 'best book around'
        self.publisher = 'my publisher'

        self.book = Book.objects.create(
            owner=self.owner,
            category=self.category,
            isbn_10=self.isbn_10,
            isbn_13=self.isbn_13,
            title=self.title,
            price=self.price,
            condition=self.condition,
            quantity=self.quantity,
            author=self.author,
            edition=self.edition,
            description=self.description,
            publisher=self.publisher
        )

    def test_book_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in Book model.
        """
        self.assertEqual(len(self.book._meta.fields), 17)
