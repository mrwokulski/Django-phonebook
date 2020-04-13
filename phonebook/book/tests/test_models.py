from django.test import TestCase
from ..models import Person, Email, Phone

class PersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Person.objects.create(name='Jan', surname='Kowalski')

    def test_name_label(self):
        person = Person.objects.get(id=1)
        name_label = person._meta.get_field('name').verbose_name
        self.assertEquals(name_label, 'name')

    def test_surname_label(self):
        person = Person.objects.get(id=1)
        surname_label = person._meta.get_field('surname').verbose_name
        self.assertEquals(surname_label, 'surname')

    def test_name_max_length(self):
        person = Person.objects.get(id=1)
        max_length = person._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_surname_max_length(self):
        person = Person.objects.get(id=1)
        max_length = person._meta.get_field('surname').max_length
        self.assertEquals(max_length, 50)

    def test_person_to_string(self):
        person = Person.objects.get(id=1)
        _str = person.__str__
        self.assertEquals(_str, f'{person.surname}, {person.name}')
        
class PhoneModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Phone.objects.create('123456789')
        Person.objects.create(name='Jan', surname='Kowalski')
    