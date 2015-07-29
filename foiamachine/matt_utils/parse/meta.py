def get_field_headers():
    """ 
    need to regenerate
    fresh every file we process
    to identify field headers
    """

    field_headers = {
                     'last_name' : { 
                                     'indices' : set(), 
                                     'keywords': ['last', 'name','employee'], # TODO: still need to disambiguate multiple name fields
                                     'required': True, # there's going to be at least one 'name' field
                                     'reported': True,
                                     'title_case'   : True,
                                    },  
                     'first_name' : { 
                                     'indices' : set(), 
                                     'keywords': ['first', 'fname'],
                                     'required': False, # one name field will go to the last name
                                     'reported': True,
                                     'title_case'   : True,
                                    },  
                     'salary':      {   
                                     'indices' : set(), 
                                     'keywords': ['salar', 'pay', 'wage','amount','annual','total'],
                                     'required': True,
                                     'reported': True,
                                     'title_case'   : False,
                                    },  
                     'hourly':      {   
                                     'indices' : set(), 
                                     'keywords': ['hour'],
                                     'required': False,
                                     'reported': False,
                                     'title_case'   : False,
                                    },
                     'title' :      {
                                     'indices' : set(),
                                     'keywords': ['title', 'position', 'job','classification'],
                                     'required': False,
                                     'reported': True,
                                     'title_case'   : True,
                                    },
                     'department' : {
                                     'indices' : set(),
                                     'keywords': ['department', 'dept' ],
                                     'required': False,
                                     'reported': True,
                                     'title_case'   : True,
                                    },
                     'start_date' : {
                                     'indices' : set(),
                                     'keywords': ['start', 'hire', 'date'],
                                     'required': False,
                                     'reported': True,
                                     'title_case'   : False,
                                    },
                    }

    return field_headers

