"""
no matter how hard
you try sometimes you just got
to hard code some shit
"""



def set_order_single_name(data_row, attachment):
    """
    dumbasses put names
    in one big field leaving me
    to sort it all out
    TODO: just return bool and transform in transform
    """
    # hard-code attachment IDs ... fun right?????
    first_name_first = [49, 365, 366]    
    last_name_first = [373]

    space_delimited = data_row['last_name'].split(' ')

    if attachment.id in first_name_first:
        if len(space_delimited) == 2: # easy enough
            data_row['first_name'] = space_delimited[0]
            data_row['last_name'] = space_delimited[1]
        elif len(space_delimited[1]) == 1 or (len(space_delimited[1]) == 2 and space_delimited[1][1] == '.'): # likely middle initial
            data_row['first_name'] = ' '.join(space_delimited[0:2])
            data_row['last_name'] = ' '.join(space_delimited[2:])
        else:
            data_row['first_name'] = space_delimited[0]
            data_row['last_name'] = ' '.join(space_delimited[1:])

    elif attachment.id in last_name_first:
        if len(space_delimited) == 2: # easy enough
            data_row['last_name'] = space_delimited[0]
            data_row['first_name'] = space_delimited[1]
        else:
            if len(space_delimited) > 2: # could be anything but we're just taking the first string element and calling it last name
                data_row['last_name'] = space_delimited[0]
                data_row['first_name'] = ' '.join(space_delimited[1:])

    return data_row



def check_if_special(att_id,field_headers,cases):
    """
    populate header
    indices for special case
    attachments 'cases'
    """
    for case in cases:
        if att_id == case['attachment_id']:
            for field in case:
                if field in field_headers:
                    field_headers[field]['indices'].append(case[field])
            return field_headers
    return None


cases = [
         {
          'attachment_id': None,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': None,
          'first_name': None,
          'middle_initial': None,
          'title': None,
          'department': None,
          'salary': None,
          'hourly': None,
          'start_date': None,
         },
         {
          'attachment_id': 64,
          'first_data_line_number': None,
          'last_name': 0,
          'first_name': 1,
          'middle_initial': 2,
          'title': 3,
          'department': 4,
          'salary': 6,
          'hourly': 5,
          'start_date': 7
         },
         {
          'attachment_id': 249,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 0,
          'first_name': 1,
          'middle_initial': None,
          'title': 3,
          'department': 8,
          'salary': 6,
          'hourly': 7,
          'start_date': 4,
         },
         {
          'attachment_id': 281,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 2,
          'first_name': 3,
          'middle_initial': None,
          'title': 1,
          'department': 0,
          'salary': 6,
          'hourly': None,
          'start_date': 4,
         },
        ]
