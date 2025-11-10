from django import forms
# ------------------------------------------------
from .models import Person, NaturalPerson
from .utils.validator import Validator
# ------------------------------------------------

class LoginForm(forms.Form):
    
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter a username',
                'value': 'anderson',
                'class': 'form-control'
            }
        )
    )
    
    password = forms.CharField(
        max_length=20, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Enter a password',
                'value': '121181',
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False 

    def clean_username(self):
        return Validator().validate_username(self.cleaned_data.get('username'))

    def clean_password(self):
        return Validator().validate_password(self.cleaned_data.get('password'))
        
# ------------------------------------------------

class SearchPersonForm(forms.Form):
    search = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter a data for search',
                'class': 'form-control',
            }
        )
    )

# ------------------------------------------------

class PersonForm(forms.ModelForm):

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    email = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    status = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                 'class': 'form-check-input',
            'style': 'float: right; transform: scale(3); margin-right: 15px; cursor: pointer;',  # move o checkbox para a direita
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2,
                'style': 'resize: none;',
            }
        )
    )
 
    picture = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'style': 'cursor:pointer;'
            }
        )
    )

    class Meta:
        model = Person
        fields = (
            'name', 
            'email', 
            'picture',
            'status',
            'description'
        )

class NaturalPersonForm(PersonForm):

    cpf = forms.CharField(
        max_length=14,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    gender = forms.ChoiceField(
        choices=Validator().get_genders(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    birthday = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    income_range = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    )
     
    def __init__(self, *args, **kwargs):
        super(NaturalPersonForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False    
        if self.instance and self.instance.pk:
            self.fields['cpf'].widget.attrs.update({
                'readonly':'true',
            })
    

    class Meta(PersonForm.Meta):
        model = NaturalPerson
        fields = PersonForm.Meta.fields + (
            'cpf',
            'gender',
            'birthday', 
            'income_range'
        )
        widgets = {
            'cpf': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def clean_name(self):
        return Validator().validate_name(self.cleaned_data.get('name'))
    
    def clean_email(self):
        return Validator().validate_email(self.cleaned_data.get('email'), self.instance)
    
    def clean_picture(self):
        return Validator().validate_picture(self.cleaned_data.get('picture'))
    
    def clean_status(self):
        return Validator().validate_status(self.cleaned_data.get('status'))
    
    def clean_cpf(self):
        return Validator().validate_cpf(self.cleaned_data.get('cpf'))
    
    def clean_birthday(self):
        return Validator().validate_birthday(self.cleaned_data.get('birthday'))
    
    def clean_gender(self):
        return Validator().validate_gender(self.cleaned_data.get('gender'))
    
    def clean_income_range(self):
        return Validator().validate_income_range(self.cleaned_data.get('income_range'))

# ------------------------------------------------

class LegalPersonForm(PersonForm):
    pass