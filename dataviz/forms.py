from django.urls import reverse_lazy

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

from .models import *

class GrantDonorFilterForm(forms.Form):
    '''
    IMPORTANT:  If you add a field to the filters, you probably also want to include the field in the
    prepare_related_donor_fields_to_lookup_fields function.
    '''
    region = forms.ModelChoiceField(
        queryset = Region.objects.all(),
        required = False,
        #empty_label = u'-- Region --',
        empty_label = None,
        widget = forms.SelectMultiple(),
    )
    country = forms.ModelChoiceField(
        queryset = Country.objects.all(),
        required = False,
        empty_label = None,
        widget = forms.SelectMultiple(),
    )
    donor = forms.ModelChoiceField(
        queryset = Donor.objects.all(),
        required = False,
        empty_label = None,
        widget = forms.SelectMultiple(),
    )
    donor_department = forms.ModelChoiceField(
        queryset=DonorDepartment.objects.all(),
        required=False,
        empty_label=None,
        widget=forms.SelectMultiple(),
    )
    submission_date_from = forms.DateField(
        label = u'From Submission Date',
        required = False,
        widget = forms.DateInput()
    )
    submission_date_to = forms.DateField(
        label = u'To Submission Date',
        required = False,
    )
    grants_amount_min = forms.IntegerField(
        label = u'Dollar value minimum',
        required = False,
    )
    grants_amount_max = forms.IntegerField(
        label = u'Dollar value maximum',
        required = False,
    )
    sector = forms.ModelChoiceField(
        queryset = Sector.objects.all(),
        empty_label = '',
        required = False,
    )
    subsector = forms.ModelChoiceField(
        queryset = SubSector.objects.all(),
        empty_label = '',
        required = False,
    )
    theme = forms.ModelChoiceField(
        queryset = Theme.objects.all(),
        empty_label = '',
        required = False,
    )
    methodology = forms.ModelChoiceField(
        queryset = Methodology.objects.all(),
        empty_label = '',
        required = False,
    )

    status = forms.ChoiceField(
        choices = [(status['status'], status['status']) for status in Grant.objects.filter(status__isnull=False).values('status').distinct().order_by('status')],
        required = False,
        widget = forms.SelectMultiple(),
    )
    hq_admin = forms.ChoiceField(
        choices = [(hq['hq_admin'], hq['hq_admin']) for hq in Grant.objects.filter(hq_admin__isnull=False).exclude(hq_admin__exact = '').exclude(hq_admin__exact='Hong Kong').values('hq_admin').distinct().order_by('hq_admin')],
        required = False,
        widget = forms.SelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.html5_required = True
        self.helper.form_id = "grants_donor_filter_form"
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('region', css_class="input-sm"),
            Field('country', css_class="input-sm"),
            Field('donor', css_class="input-sm"),
            Field('donor_department', css_class="input-sm"),
            #Field(AppendedText('submission_date_from', '<span class="glyphicon glyphicon-calendar"></span>'), placeholder="From Submission date", css_class="input-sm"),
            Field('submission_date_from', placeholder="Submission date from...", css_class="input-sm"),
            Field('submission_date_to', placeholder="Submission date to...", css_class="input-sm"),
            Field('grants_amount_min', placeholder = 'Dollar value minimum', css_class='input-sm'),
            Field('grants_amount_max', placeholder = 'Dollar value maximum', css_class='input-sm'),
            Field('sector', css_class='input-sm'),
            Field('subsector', css_class='input-sm'),
            Field('theme', css_class='input-sm'),
            Field('methodology', css_class='input-sm'),
            Field('status', css_class='input-sm'),
            Field('hq_admin', css_class='input-sm'),
        )
        self.helper.form_method = 'get'
        self.helper.form_action = '/global/'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-sm'))
        self.helper.add_input(Reset('reset', 'Clear', css_id='id_search_form_reset_btn', css_class='btn-warning btn-sm'))
        super(GrantDonorFilterForm, self).__init__(*args, **kwargs)
        