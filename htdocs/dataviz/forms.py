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
    submission_date_from = forms.DateField(
        label = u' From Submission Date',
        required = False,
        widget = forms.DateInput()
    )
    submission_date_to = forms.DateField(
        label = u' To Submission Date',
        required = False,
    )
    #grants_count = forms.IntegerField(
    #    label= u'# Grants',
    #    required = False,
    #)
    grants_amount = forms.IntegerField(
        label = u'Proposals greater than $ Amount',
        required = False,
    )
    sector = forms.ChoiceField(
        choices =(),
        required = False,
    )
    subsector = forms.ChoiceField(
        choices = (),
        required = False,
    )
    theme = forms.ChoiceField(
        choices = (),
        required = False,
    )
    methodology = forms.ChoiceField(
        choices = (),
        required = False,
    )
    status = forms.ChoiceField(
        choices = (),
        required = False,
    )
    hq_admin = forms.ChoiceField(
        choices = (),
        required = False,
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
            #Field(AppendedText('submission_date_from', '<span class="glyphicon glyphicon-calendar"></span>'), placeholder="From Submission date", css_class="input-sm"),
            Field('submission_date_from', placeholder="From Submission date", css_class="input-sm"),
            Field('submission_date_to', placeholder="To Submission date", css_class="input-sm"),
            #Field('grants_count', placeholder = 'donors with X number of proposals',css_class='input-sm'),
            Field('grants_amount', placeholder = 'proposals greater than $ amount', css_class='input-sm'),
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
        self.helper.add_input(Reset('reset', 'Reset', css_id='id_search_form_reset_btn', css_class='btn-warning btn-sm'))
        super(GrantDonorFilterForm, self).__init__(*args, **kwargs)
        choices_hq_admin = [("", "--HQadmin--"),]
        choices =  [(hq['hq_admin'], hq['hq_admin']) for hq in Grant.objects.filter(hq_admin__isnull=False).exclude(hq_admin__exact = '').exclude(hq_admin__exact='Hong Kong').values('hq_admin').distinct()]
        choices.sort()
        choices_hq_admin.extend(choices)
        self.fields['hq_admin'] = forms.ChoiceField(choices=choices_hq_admin, required=False)

        status_choices = [("", "--Funding Status--"),]
        choices = None
        choices = [(status['status'], status['status']) for status in Grant.objects.filter(status__isnull=False).values('status').distinct()]
        choices.sort()
        status_choices.extend(choices)
        self.fields['status'] = forms.ChoiceField(choices=status_choices, required=False)

        sector_choices = [("", "--Sector--"),]
        choices = None
        choices = [(sector.sector_id, sector.name) for sector in Sector.objects.all()]
        sector_choices.extend(choices)
        self.fields['sector'] = forms.ChoiceField(choices=sector_choices, required=False)

        subsector_choices = [("", "--Area of Focus--"),]
        choices = None
        choices = [(subsector.subsector_id, subsector.name) for subsector in SubSector.objects.all()]
        subsector_choices.extend(choices)
        self.fields['subsector'] = forms.ChoiceField(choices=subsector_choices, required=False)

        theme_choices = [("", "--Theme--"),]
        choices = None
        choices = [(theme.theme_id, theme.name) for theme in Theme.objects.all()]
        theme_choices.extend(choices)
        self.fields['theme'] = forms.ChoiceField(choices=theme_choices, required=False)

        methodology_choices = [("", "--Methodology--"),]
        choices = None
        choices = [(methodology.methodology_id, methodology.name) for methodology in Methodology.objects.all()]
        methodology_choices.extend(choices)
        self.fields['methodology'] = forms.ChoiceField(choices=methodology_choices, required=False)





