from django.core.urlresolvers import reverse_lazy

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

from .models import *

class GrantDonorFilterForm(forms.Form):
    region = forms.ModelChoiceField(
        queryset = Region.objects.all(),
        required = False,
        empty_label = u'-- Filter by Region --',
        widget = forms.Select(),
    )
    country = forms.ModelChoiceField(
        queryset = Country.objects.none(),
        required = False,
        empty_label = u'-- Filter by Country --',
        widget = forms.Select(),
    )
    submission_date_from = forms.DateField(
        label = u' From Submission Date',
        required = False,
        
    )
    submission_date_to = forms.DateField(
        label = u' To Submission Date',
        required = False,
    )
    grants_count = forms.IntegerField(
        label= u'# Grants',
        required = False,
    )
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        #self.helper.label_class = 'col-sm-0'
        #self.helper.field_class = 'col-sm-1'
        #self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.html5_required = True
        self.helper.form_id = "grants_donor_filter_form"
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('region', css_class="input-sm"),
            Field('country', css_class="input-sm"),
            Field('submission_date_from', placeholder="From Submission date", css_class="input-sm"),
            Field('submission_date_to', placeholder="To Submission date", css_class="input-sm"),
            Field('grants_count', placeholder = '# Grants',css_class='input-sm'),
        )
        self.helper.form_method = 'get'
        self.helper.form_action = '/global/'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-sm'))
        self.helper.add_input(Reset('reset', 'Reset', css_class='btn-warning btn-sm'))
        super(GrantDonorFilterForm, self).__init__(*args, **kwargs)