from faker import Faker

fake = Faker("pt_BR")


class TenantFactory:
    """Gera dados de tenant para testes."""

    @staticmethod
    def build(**kwargs):
        data = {
            "name": fake.company(),
            "slug": fake.slug(),
            "email": fake.company_email(),
        }
        data.update(kwargs)
        return data


class UserFactory:
    """Gera dados de usuário para testes."""

    @staticmethod
    def build(**kwargs):
        data = {
            "name": fake.name(),
            "email": fake.email(),
            "password": "senha12345",
            "role": "admin",
        }
        data.update(kwargs)
        return data


class ServiceFactory:
    """Gera dados de serviço para testes."""

    @staticmethod
    def build(**kwargs):
        data = {
            "name": fake.bs(),
            "description": fake.sentence(),
            "duration_minutes": 60,
            "price": 20000,
        }
        data.update(kwargs)
        return data
