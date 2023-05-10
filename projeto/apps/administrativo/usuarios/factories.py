import factory
from django.contrib import auth
from factory import django


class UsuarioFactory(django.DjangoModelFactory):

    class Meta:
        model = auth.get_user_model()
        django_get_or_create = ('username', 'email')

    username = factory.Faker('first_name')
    password = factory.Faker('ean')

    @factory.lazy_attribute
    def email(self):
        return '{}@domain.com'.format(self.username)
