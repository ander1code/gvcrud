from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError

# --------------------------------------------------------------------

class Validator(object):
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Validator, cls).__new__(cls)
        return cls.__instance
    
    def get_genders(self):
        return (('M','Male'),('F','Female'),('O','Other'))
    
    def validate_username(self, data):
        if not data or not data.strip():
            raise ValidationError('Username is empty.')
        validator = RegexValidator(
            regex=r"^\S+$", 
            message='Invalid username format. Spaces are not allowed.'
        )
        validator(data)
        return data
    
    def validate_password(self, data):
        if not data or not data.strip():
            raise ValidationError('Password is empty.')
        return data

    def validate_name(self, data):
        if not data or not data.strip():
            raise ValidationError('Name is empty.')
        if len(data) < 4: 
            raise ValidationError('Name must be at least 4 characters long.')
        if len(data) > 50: 
            raise ValidationError('Name cannot exceed 50 characters.')
        return data

    def validate_email(self, data, instance=None):
        if not data or not data.strip():
            raise ValidationError('E-mail is empty.')
        validator = EmailValidator(message='Invalid e-mail.')
        validator(data)
        from ..models import Person
        person = Person.objects.filter(email__iexact=data).first()
        if person and (instance is None or instance.pk != person.pk):
            raise ValidationError('E-mail already is registered.')
        return data

    def __validate_cpf_number(self, cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            return False
        if cpf == cpf[0] * 11:
            return False
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        return int(cpf[9]) == digito1 and int(cpf[10]) == digito2

    def validate_cpf(self, data):
        if not data or not data.strip():
            raise ValidationError('CPF is empty.')
        validator = RegexValidator(r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$', message='Invalid CPF.')
        validator(data)
        data = data.replace(".","").replace("-","")
        if not self.__validate_cpf_number(data):
            raise ValidationError('Invalid CPF.')
        return data
    
    def validate_gender(self, data):
        if not data or not data.strip():
            raise ValidationError('Gender is empty.')
        data = data.strip().upper()
        if not data in ['M','F','O']:
            raise ValidationError('Invalid gender.')
        return data
    
    def validate_birthday(self, data):
        if not data:
            raise ValidationError('Birthday is empty.')
        from datetime import date
        today = date.today()
        if data > date(today.year - 18, today.month, today.day):
            raise ValidationError('Invalid birthday.')
        return data
    
    def validate_status(self, data):
        if data is None:
            raise ValidationError('Status is empty.')
        if not isinstance(data, bool):
            raise ValidationError('Status must be True or False.')
        return data
    
    def validate_picture(self, data):
        if not data:
            raise ValidationError('Picture is empty.')
        return data
    
    def __format_decimal(self, data):
        from decimal import Decimal
        data = data.replace("R", "").replace("$", "").replace(" ", "")
        data = data.replace(".", "").replace(",", ".")
        return Decimal(data)
    
    def validate_income_range(self, data):
        from decimal import Decimal
        if not data:
            raise ValidationError('Income range is empty.')
        if data is None:
            raise ValidationError('Income range is empty.')
       
        data = self.__format_decimal(data)
        
        validator = RegexValidator(regex=r"^\d{1,10}\.\d{2}$",message='Invalid income range.')
        validator(data)
        if Decimal(data) < 0:
            raise ValidationError('Invalid income range.')
        if Decimal(data) > 9999999999.99:
            raise ValidationError('Invalid income range.')
        return data
        
# --------------------------------------------------------------------        
