def get_field_headers():
    """ 
    need to regenerate
    fresh every file we process
    to identify field headers
    """

    field_headers = {
                     'last_name' : { 
                                     'indices' : [], 
                                     'keywords': ['last', 'name','employee'], # TODO: still need to disambiguate multiple name fields
                                     'required': True, # there's going to be at least one 'name' field
                                     'reported': True,
                                     'title_case'   : True,
                                    },  
                     'first_name' : { 
                                     'indices' : [], 
                                     'keywords': ['first', 'fname'],
                                     'required': False, # one name field will go to the last name
                                     'reported': True,
                                     'title_case'   : True,
                                    },  
                     'salary':      {   
                                     'indices' : [], 
                                     'keywords': ['salary', 'pay', 'wage','amount','annual','total'],
                                     'required': True,
                                     'reported': True,
                                     'title_case'   : False,
                                    },  
                     'hourly':      {   
                                     'indices' : [], 
                                     'keywords': ['hour'],
                                     'required': False,
                                     'reported': False,
                                     'title_case'   : False,
                                    },
                     'title' :      {
                                     'indices' : [],
                                     'keywords': ['title', 'position', 'job','classification'],
                                     'required': True,
                                     'reported': True,
                                     'title_case'   : True,
                                    },
                     'department' : {
                                     'indices' : [],
                                     'keywords': ['department', 'dept' ],
                                     'required': True,
                                     'reported': True,
                                     'title_case'   : True,
                                    },
                     'start_date' : {
                                     'indices' : [],
                                     'keywords': ['start', 'hire', 'date'],
                                     'required': False,
                                     'reported': True,
                                     'title_case'   : False,
                                    },
                    }

    return field_headers

