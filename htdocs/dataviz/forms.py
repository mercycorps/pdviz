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
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        #self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.html5_required = True
        self.helper.form_id = "grants_donor_filter_form"
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('region', id='region_dropdown', css_class="input-sm"),
            Field('country', id='country_dropdown', css_class="input-sm"),
            Field('submission_date_from', placeholder="From", css_class="input-sm"),
            Field('submission_date_to', placeholder="To", css_class="input-sm col-sm-2"),
        )
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Submit', css_id="ok", css_class='btn-sm'))
        self.helper.add_input(Reset('rest', 'Reset', css_class='btn-warning btn-sm'))
        super(GrantDonorFilterForm, self).__init__(*args, **kwargs)