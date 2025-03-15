from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import UserRegistrationForm

# Create your views here.

class RegistrationView(FormView):
    template_name = 'registration_form.html'
    form_class = UserRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        submitted_data = form.cleaned_data
        
        new_form = self.form_class()
        
        return render(self.request, self.template_name, {
            'form': new_form,
            'submitted_data': submitted_data
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submitted_data'] = None
        return context
