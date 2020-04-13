from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.template.defaultfilters import slugify

class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("book:person_detail", kwargs={ "id_person": self.id })

    def __str__(self):
        return f'{self.surname}, {self.name}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.surname+" "+self.name)
        super(Person, self).save(*args, **kwargs)
 

class Phone(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True)
    phone = models.IntegerField(validators=[
        MaxValueValidator(999999999, message='Numer telefonu moze miec maksymalnie 9 cyfr!')
    ])

    def __str__(self):
        return f'{self.person.name} {self.person.surname} - {self.phone}'


class Email(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return f'{self.person.name} {self.person.surname} - {self.email}'