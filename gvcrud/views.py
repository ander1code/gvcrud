from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    View, CreateView, DetailView, UpdateView
)
# --------------------------------------------------------------------
from .models import NaturalPerson
from .form import LoginForm, SearchPersonForm, NaturalPersonForm
from .utils.reports import Reports
# --------------------------------------------------------------------

from django.db.models import Q

def home(request):
    return render(request, 'home/home.html', {})

@login_required(login_url="login-auth")
def choice_person(request):
    return render(request, 'person/choice.html', {})

# --------------------------------------------------------------------

def login_auth(request):
    if request.user.is_authenticated:
        messages.info(request, 'User already logged.')
        return redirect('person-choice')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request,'Successfully logged.')
                return redirect(reverse_lazy('person-choice')) 
            else:
                messages.error(request,'Invalid username and password.')
                return redirect('login-auth')
    else:
        form = LoginForm()
    return render(request, 'login/form.html', {'form':form})

def logoff(request):
    if not request.user.is_authenticated:
        messages.info(request, 'No user logged.')
        return redirect('person-choice')
    logout(request)
    messages.success(request, 'Successfully logout.')
    return redirect('home-person')

# --------------------------------------------------------------------

class NaturalPersonListView(LoginRequiredMixin, View):
    login_url = 'login-auth'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_list"] = False
        return context

    def get(self, request, *args, **kwargs):
        persons = NaturalPerson.objects.all()
        form = SearchPersonForm()
        return render(request, 'person/list.html', {'form': form, 'persons': persons})

    def post(self, request, *args, **kwargs):
        form = SearchPersonForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search'].strip()
            if search:
                persons = NaturalPerson.objects.filter(
                    Q(name__istartswith=search) | 
                    Q(cpf__icontains=search) | 
                    Q(email__icontains=search) 
                )
            else:
                persons = NaturalPerson.objects.all()
        else:
            persons = NaturalPerson.objects.all()
        return render(request, 'person/list.html', {'form': form, 'persons': persons})
        
class NaturalPersonCreateView(LoginRequiredMixin, CreateView):
    model = NaturalPerson
    form_class = NaturalPersonForm
    template_name = "person/form.html"
    login_url = 'login-auth'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_list"] = True 
        context["edition"] = False 
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Successfully created.')
        return reverse_lazy('natural-list')
    
class NaturalPersonDetailView(LoginRequiredMixin, DetailView):
    model = NaturalPerson
    template_name="person/detail.html"
    login_url = 'login-auth'
    context_object_name = 'person'

    def dispatch(self, request, *args, **kwargs):
        self.obj = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_list"] = True
        context["income_range_fmt"] = f"R$ {str(self.obj.income_range).replace(".",",")}" 
        return context

class NaturalPersonUpdateView(LoginRequiredMixin, UpdateView):
    model = NaturalPerson
    template_name="person/form.html"
    login_url = 'login-auth'
    form_class = NaturalPersonForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_list"] = True 
        context["edition"] = True
        context["picture_url"] = self.object.picture.url
        return context

    def post(self, request, *args, **kwargs):
        person = self.get_object()
        if 'delete' in request.POST:
            person.delete()
            messages.success(request,'Successfully deleted.')
            return redirect(reverse_lazy('natural-list')) 
        form = self.form_class(request.POST, request.FILES, instance=person)
        print(form.fields['picture'])
        if form.is_valid():
            form.instance.updated_at = timezone.now()
            form.save()
            messages.success(request,'Successfully edited.')
            return redirect(reverse_lazy('natural-list')) 
        return render(request, self.template_name, {'form': form, 'edition':True})


class NaturalPersonReportsView(View):

    def dispatch(self, request, *args, **kwargs):
        self.natural_persons = NaturalPerson.objects.all()  
        self.report = Reports(self.natural_persons)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = {}
        print(self.report.get_highest_income_person())
        context.update({
            'highest_income_person': self.report.get_highest_income_person(),
            'lowest_income_person': self.report.get_lowest_income_person(),
            'avg_income': self.report.avg_income,
            'max_income': self.report.max_income,
            'min_income': self.report.min_income,
            'people_above_avg': self.report.get_people_above_average_income(),
            'people_below_avg': self.report.get_people_below_average_income(),
            'people_equal_avg': self.report.get_people_with_average_income(),
            'male_count': self.report.count_by_gender('M'),
            'female_count': self.report.count_by_gender('F'),
            'other_count': self.report.count_by_gender('O'),
            'total_income': f"R$ {str(self.report.total_income_sum()).replace('.',',')}",
        })
        return context

    def get(self, request, *args, **kwargs):
        if self.natural_persons:
            context = self.get_context_data()
            return render(request, 'person/report.html', context)
        else:
            messages.info(request,'No records found for report creation.')
        return redirect(reverse_lazy('natural-list')) 

    
# --------------------------------------------------------------------    


    