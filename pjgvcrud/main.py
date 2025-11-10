from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_cpf(data):
    def validate_cpf_number(cpf: str):
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

    if not data or not data.strip():
        print('CPF is empty.')
    validator = RegexValidator(r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$', message='Invalid CPF.') # simple validation!
    validator(data)
    if not validate_cpf_number(data):
        print('Invalid CPF.')
    print(data)

validate_cpf('07963085782')