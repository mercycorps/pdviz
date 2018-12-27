import datetime

def prepare_related_donor_fields_to_lookup_fields(params, prefix):
    """
    Prefix each key in the URL params with 'grants__' so that Donor's related entries
    in Grant table are filtered by following the relationship in reverse fashion
    """

    kwargs = {}
    for k in params:
        if k == 'format':
            pass
        elif k == 'region':
            if prefix == 'countries__grants__':
                kwargs['countries__region__in'] = params[k].split(',')
            else:
                kwargs[prefix + 'countries__region__in'] = params[k].split(',')
        elif k == 'country':
            if prefix == 'countries__grants__':
                kwargs['countries__country_id__in'] = params[k].split(',')
            else:
                kwargs[prefix + 'countries__country_id__in'] = params[k].split(',')
        elif k == 'donor':
            if prefix == 'donors__grants__':
                kwargs['donors__donor_id__in'] = params[k].split(',')
            else:
                kwargs[prefix + 'donor_id__in'] = params[k].split(',')
        elif k == 'donor_department':
            kwargs[prefix + 'donor__donordepartment__in'] = params[k].split(',')
        elif k == 'sector':
            kwargs[prefix + 'sectors__sector_id'] = params[k]
        elif k == 'subsector':
            kwargs[prefix + 'subsectors__subsector_id'] = params[k]
        elif k == 'methodology':
            kwargs[prefix + 'methodologies__methodology_id'] = params[k]
        elif k == 'theme':
            kwargs[prefix + 'themes__theme_id'] = params[k]
        elif k == 'submission_date_from':
            kwargs[prefix + 'submission_date__gt'] = params[k]
        elif k == 'submission_date_to':
            kwargs[prefix + 'submission_date__lt'] = params[k]
        elif k == 'grants_amount_min':
            kwargs[prefix + 'amount_usd__gte'] = params[k]
        elif k == 'grants_amount_max':
            kwargs[prefix + 'amount_usd__lte'] = params[k]
        elif k == 'status':
            kwargs[prefix + 'status__in'] = params[k].split(',')
        else:
            kwargs[prefix + k] = params[k]

    # Grants submission_date is not specified then, by default, restrict it to the last three years
    if not prefix + 'submission_date__gt' in kwargs and not prefix + 'submission_date__lt' in kwargs:
        today_date  = datetime.datetime.now()
        date_3_years_ago = str(datetime.date(today_date.year -3 , today_date.month, 1))
        kwargs[prefix + 'submission_date__gt'] = date_3_years_ago

    # Do not show donors that have no Grants
    if prefix:
        kwargs[prefix + 'isnull'] = False
    return kwargs
