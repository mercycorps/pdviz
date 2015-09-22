
def prepare_related_donor_fields_to_lookup_fields(params):
    """
    Prefix each key in the URL params with 'grants__' so that Donor's related entries 
    in Grant table are filtered by following the relationship in reverse fashion
    """
    kwargs = {}
    for k,v in params.iteritems():
        if k == 'format':
            pass
        elif k == 'region':
            kwargs['grants__countries__' + k] = v
        elif k == 'sector':
            kwargs['grants__sectors__' + k] = v
        elif k == 'country':
            kwargs['grants__countries__country_id'] = v
        elif k == 'grants_count':
            pass
        elif k == 'submission_date_from':
            kwargs['grants__submission_date__gt'] = v
        elif k == 'submission_date_to':
            kwargs['grants__submission_date__lt'] = v
        else:
            kwargs['grants__' + k] = v

        # Do not show donors that have no Grants
        kwargs['grants__isnull'] = False
    return kwargs