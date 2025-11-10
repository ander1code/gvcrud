from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator,  MaxValueValidator
from django.db.models import UniqueConstraint, CheckConstraint, Q, F
from .utils.validator import Validator

class Person(models.Model):
    name = models.CharField(
        verbose_name='Name', 
        blank=False, null=False, 
        max_length=50, 
        validators=[
            MinLengthValidator(4)
        ]
    )

    email = models.EmailField(
        verbose_name='E-mail', 
        blank=False, 
        null=False, 
        max_length=50
    )
    
    picture = models.ImageField(
        verbose_name='Picture', 
        blank=True, 
        null=True, 
        upload_to='person/natural'
    )

    status = models.BooleanField(
        verbose_name='Status', 
        blank=False, 
        null=False
    )

    description = models.CharField(
        verbose_name='Description', 
        blank=True, 
        null=True, 
        max_length=200
    )

    created_at = models.DateTimeField(
        verbose_name='Created At', 
        blank=False, 
        null=False, 
        auto_now=False, 
        editable=False,
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='Updated At', 
        blank=True, 
        null=True, 
        auto_now=True, 
        auto_now_add=False
    )

    class Meta:
        db_table = 'person'
        managed = True
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        constraints = [
            UniqueConstraint(
                fields=['email'], 
                name='unq_person_email', 
                violation_error_message='E-mail already is registered.'
            ),
            CheckConstraint(
                check=Q(updated_at__isnull=True) | Q(updated_at__gte=F('created_at')), 
                name='chk_person_updated_at', 
                violation_error_message='"updated_at" date cannot be earlier than "created_at" date.'
            )
        ]
  
class NaturalPerson(Person):

    cpf = models.CharField(
        verbose_name='CPF', 
        blank=False, 
        null=False, 
        max_length=11, 
        validators=[Validator().validate_cpf]
    )

    gender = models.CharField(
        verbose_name='Gender', 
        blank=False, 
        null=False, max_length=1, 
        choices=Validator().get_genders, 
        validators=[Validator().validate_gender]
    )

    birthday = models.DateField(
        verbose_name='Birthday', 
        blank=False, 
        null=False, 
        validators=[Validator().validate_birthday]
    )

    income_range = models.DecimalField(
        verbose_name="Income Range",
        max_digits=12,
        decimal_places=2,
        blank=False, 
        null=False, 
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999999999.99)
        ]
    )

    def save(self, *args, **kwargs):
       if self.pk:
           old = NaturalPerson.objects.get(pk=self.pk)
           self.cpf = old.cpf
       super(NaturalPerson, self).save(*args, **kwargs)

    def __str__(self):
        return "f{self.pk}: {self.cpf}, {self.name}" 

    class Meta:
        ordering = ['-created_at']
        db_table = 'natural_person'
        managed = True
        verbose_name = 'Natural Person'
        verbose_name_plural = 'Natural Persons'
        constraints = [
            UniqueConstraint(fields=['cpf'], name="unq_naturalperson_cpf", violation_error_message='CPF already is registered.'),
            CheckConstraint(
                check=Q(gender='M') | Q(gender='F') | Q(gender='O'), 
                name='chk_naturalperson_gender', 
                violation_error_message='Invalid gender.'
            ),
            CheckConstraint(
                check=Q(income_range__gte=0) & Q(income_range__lte=9999999999.99),
                name='chk_naturalperson_income_range',
                violation_error_message='Invalid income range.'
            )
        ]
    
class LegalPerson(Person):
    pass
