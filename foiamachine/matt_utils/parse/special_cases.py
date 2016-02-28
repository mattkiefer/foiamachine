"""
no matter how hard
you try sometimes you just got
to hard code some shit
"""

# skip these att ids
# during testing for
# commented reasons
skips = [
         #167,507,595,803,855, # good? just take awhile? double-check ...
         #608, # need to check ascii encode issue
         855, # isbe core dump
         246, # dupe of 245
         863, # dupe of 858
         409, # dupe of 901
         892, # field
        ]

# hard-code attachment IDs ... fun right?????
first_name_first = [49, 365, 366, 709, 412, 748]    
last_name_first = [373, 51, 284]


def set_order_single_name(data_row, attachment):
    """
    dumbasses put names
    in one big field leaving me
    to sort it all out
    TODO: just return bool and transform in transform
    """

    space_delimited = data_row['last_name'].split(' ')
    # hack!
    if '/' in data_row['last_name']:
        data_row['first_name'] = data_row['last_name'].split('/')[1]
        data_row['last_name'] = data_row['last_name'].split('/')[0]

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


def skip(attachment):
    """
    some attachments just
    don't play well and need to skip
    to keep it going
    """
    if attachment.id in skips:
        return True

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
                    field_headers[field]['indices'].add(case[field])
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
         {
          'attachment_id': 803,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 0,
          'first_name': None,
          'middle_initial': None,
          'title': 3,
          'department': 5,
          'salary': 6,
          'hourly': None,
          'start_date': 1,
         },
         {
          'attachment_id': 38,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 0,
          'first_name': None,
          'middle_initial': None,
          'title': 1,
          'department': 2,
          'salary': 6,
          'hourly': None,
          'start_date': 1,
         },
         {
          'attachment_id': 167,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 0,
          'first_name': None,
          'middle_initial': None,
          'title': 2,
          'department': 3,
          'salary': 4,
          'hourly': None,
          'start_date': 1,
         },
         {
          'attachment_id': 856,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 0,
          'first_name': 1,
          'middle_initial': None,
          'title': 4,
          'department': 3,
          'salary': 7,
          'hourly': None,
          'start_date': 10,
         },
         {
          'attachment_id': 546,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 0,
          'first_name': None,
          'middle_initial': None,
          'title': 4,
          'department': 1,
          'salary': 7,
          'hourly': None,
          'start_date': 5,
         },
         {
          'attachment_id': 430,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 0,
          'first_name': 1,
          'middle_initial': None,
          'title': 3,
          'department': 4,
          'salary': 5,
          'hourly': None,
          'start_date': 7,
         },
         {
          'attachment_id': 414,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 1,
          'first_name': None,
          'middle_initial': None,
          'title': 3,
          'department': 4,
          'salary': 5,
          'hourly': 6,
          'start_date': 7,
         },
         {
          'attachment_id': 507,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 0,
          'first_name': 1,
          'middle_initial': 2,
          'title': 3,
          'department': 4,
          'salary': 5,
          'hourly': None,
          'start_date': 7,
         },
         {
          'attachment_id':860,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 2,
          'first_name': 1,
          'middle_initial': None,
          'title': 4,
          'department': 5,
          'salary': 3,
          'hourly': None,
          'start_date': 6,
         }
         ,
         {
          'attachment_id':539,
          'first_data_line_number': None, # don't need this with good validation
          'last_name': 2,
          'first_name': 1,
          'middle_initial': None,
          'title': 4,
          'department': 5,
          'salary': 3,
          'hourly': None,
          'start_date': 6,
         },
         {
          # TODO: sanity check start dates
          # probably cant fix this
          'attachment_id': 362, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 2, 
          'middle_initial': None,
          'title': 4, #
          'department': 3,
          'salary': 5, #
          'hourly': 6,
          'start_date': None,
         },


         {
          # TODO: wtf is matter with this
          'attachment_id': 470, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 4, #
          'department': 5,
          'salary': 7, #
          'hourly': 6,
          'start_date': 8,
         },


         
         {
          # TODO: wft
          'attachment_id':66, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 3, #
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: goofy header unreadable
          'attachment_id': None, # 552
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, #
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },


         {
          'attachment_id':767, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 0, 
          'middle_initial': 1,
          'title': 3, #
          'department': 5,
          'salary':6, #
          'hourly': None,
          'start_date': None,
         },



         {
                 # TODO: head -n 20 to see full headers 
          'attachment_id':736, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, #
          'department': None,
          'salary': 6, #
          'hourly': None,
          'start_date': 2,
         },



         {
                 # TODO: wtf
          'attachment_id': 700, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, #
          'department': 2,
          'salary': 1, #
          'hourly': None,
          'start_date': 4,
         },

         {
          'attachment_id':417, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 3, 
          'middle_initial': None,
          'title': 0, #
          'department': 7,
          'salary': 5, #
          'hourly': 4,
          'start_date': 6,
         }, 


         {
          # TODO: 
          'attachment_id':188, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, #
          'department': 5,
          'salary': 2, #
          'hourly': 3,
          'start_date': 1,
         },

   


         {
          # TODO: wtf 
          'attachment_id': None, # 603, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, #
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id':502, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, #
          'department': None,
          'salary': 5, #
          'hourly': 4,
          'start_date': 6,
         },




         {
          # TODO: wtf looks like field layout
          'attachment_id': None, #329, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, #
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 468, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 2, 
          'middle_initial': 4,
          'title': 6, #
          'department': 7,
          'salary': 10, #
          'hourly': 9,
          'start_date': 8,
         },




         {
          # TODO: wtf looks ok
          'attachment_id':None, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, #
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: field layout
          'attachment_id': 316, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, #
          'department': 1,
          'salary': 3, #
          'hourly': None,
          'start_date': 2,
         },



         {
          # TODO: field layout 
          'attachment_id':None, # 45,
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, #
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },




         {
          # TODO: wtf looks good
          'attachment_id':460, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 8, #
          'department': 2,
          'salary': 4, #
          'hourly': 5,
          'start_date': 6,
         },


         {
          # TODO:  
          'attachment_id': 194, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, #
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': 5,
         },




         {
          # TODO: wtf no names???
          'attachment_id': 245,
          'first_data_line_number': None,
          'last_name': 8, #
          'first_name': 11, 
          'middle_initial': None,
          'title': None, #
          'department': 32,
          'salary': 23, #
          'hourly': None,
          'start_date': 18,
         },


         {
          # TODO: 
          'attachment_id': None, #388 # shit this is wronggggg id
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, #
          'department': 3,
          'salary': 5, #
          'hourly': None,
          'start_date': 2,
         },



         {
          # TODO: 
          'attachment_id': None, #124, # wrong id
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 2,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },




         {
          # TODO: 
          'attachment_id': 51, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 4,
          'salary': 1, #
          'hourly': 2,
          'start_date': 3,
         },




         {
          # TODO: 
          'attachment_id':401, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': None, 
          'department': 2,
          'salary': 5, #
          'hourly': 4,
          'start_date': 3,
         },


         {
          # TODO: wtf field headers dont align
          'attachment_id': 212, 
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 4, #
          'hourly': 5,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 237,#
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 0,
          'salary': 4, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 54, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 7, 
          'department': None,
          'salary': 5, #
          'hourly': 4,
          'start_date': None,
         },






         {
          # TODO: 
          'attachment_id': 788, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 6, #
          'hourly': 5,
          'start_date': 3,
         },




         {
          # TODO: 
          'attachment_id':180, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 4, #
          'hourly': None,
          'start_date': 7,
         },




         {
          # TODO: head -n 20 # might be field layout view 
          'attachment_id':None, # 56
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 370, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 3,
          'salary': 9, #
          'hourly': 8,
          'start_date': 7,
         },




         {
          # TODO: 
          'attachment_id':68, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': None, 
          'department': 4,
          'salary':7, #
          'hourly': 6,
          'start_date': 5,
         },


         {
          # TODO: # record layout view 
          'attachment_id':None, # 47
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: wtf doesn't comply no salaries 
          'attachment_id':None, # 746
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 484, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 5, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id':630, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': None, 
          'department': 2,
          'salary': 5, #
          'hourly': 4,
          'start_date': 6,
         },



         {
          # TODO: 
          'attachment_id': 467, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 4, #
          'hourly': None,
          'start_date': 0,
         },




         {
          # TODO: 
          'attachment_id':224, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': None, #
          'hourly':4,
          'start_date': None,
         },


         {
          # TODO: wtf record layout
          'attachment_id': None, # 408
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },




         {
          # TODO: 
          'attachment_id':197, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 7, #
          'hourly': 6,
          'start_date': 5,
         },



         {
          # TODO: 
          'attachment_id': 525, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 2,
          'salary': 4, #
          'hourly': 3,
          'start_date': 5,
         },

  


         {
          # TODO: wtf
          'attachment_id': None,#789, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },





         {
          # TODO: 
          'attachment_id':613, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 5,
          'salary': 2, #
          'hourly': 3,
          'start_date': 1,
         },





         {
          # TODO: wtf
          'attachment_id': None, # 152 #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },






         {
          # TODO: 
          'attachment_id': 287, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 0, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': 2,
         },



         {
          # TODO: 
          'attachment_id': 136, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 1,
          'salary': 3, #
          'hourly': None,
          'start_date': 4,
         },



         {
          # TODO: wtf last column
          'attachment_id': 858, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 3, #
          'hourly': 2,
          'start_date': 4,
         },




         {
          # TODO: dupe of 858
          'attachment_id': None, #863, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },




         {
          # TODO: 
          'attachment_id': 561, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 4,
          'salary': 2, #
          'hourly': 1,
          'start_date': 5,
         },



         {
          # TODO: 
          'attachment_id': 670, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 0, 
          'department': None,
          'salary': 8, #
          'hourly': 5,
          'start_date': 3,
         },





         {
          # TODO: 
          'attachment_id': 222, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 6, 
          'department': None,
          'salary': 5, #
          'hourly': None,
          'start_date': 2,
          },



         {
          # TODO: 
          'attachment_id': 359, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 2,
          'salary': 4, #
          'hourly': None,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 48, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': 6,
          'salary': 10, #
          'hourly': None,
          'start_date': 8,
         },




         {
          # TODO: 
          'attachment_id': 292, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 6, #
          'hourly': None,
          'start_date': 5,
         },




         {
          # TODO: 
          'attachment_id': 380, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 4, #
          'hourly': 5,
          'start_date': 6,
         },




         {
          # TODO: 
          'attachment_id': 621, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },



         {
          # TODO: wtf no salaries
          'attachment_id': None, # 177, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 5,
          'salary': None, #
          'hourly': None,
          'start_date': 6,
         },



         {
          # TODO: 
          'attachment_id': 299, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 4, #
          'hourly': None,
          'start_date': 3,
         },

         {
          # TODO: 
          'attachment_id': 310, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': 1,
         },


         {
          # TODO: 
          'attachment_id': 775, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 5,
          'salary': 6, #
          'hourly': None,
          'start_date': 7,
         },


         {
          # TODO: 
          'attachment_id': 338, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 5, #
          'hourly': None,
          'start_date': 1,
         },


         {
          # TODO: 
          'attachment_id': 641, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 4, #
          'hourly': None,
          'start_date': 5,
         },


         {
          # TODO:  wtf not even close
          'attachment_id': None, # 649, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO:  
          'attachment_id': 351,
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 469, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: investigate 'something wrong with headers' 
          'attachment_id':471, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': 0,
         },


         {
          # TODO: investigate 
          'attachment_id': 59, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 2, #
          'hourly': None,
          'start_date': 5,
         },



         {
          # TODO: 
          'attachment_id':None, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 212, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 4, #
          'hourly': 5,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id':287, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 0, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': 2,
         },





         {
          # TODO: 
          'attachment_id': 225, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 6, 
          'department': 7,
          'salary': 4, #
          'hourly': 5,
          'start_date': 2,
         },


         {
          # TODO: 
          'attachment_id': 730, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': 4,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id': 968, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': None,
          'salary': 6, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 506, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 4, #
          'hourly': None,
          'start_date': 5,
         },



         {
          # TODO: 
          'attachment_id': 465, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': 7,
          'start_date': 8,
         },


         {
          # TODO: 
          'attachment_id': 624, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 347, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 2, 
          'middle_initial': None,
          'title': None, 
          'department': 3,
          'salary': 5, #
          'hourly': 6,
          'start_date': 7,
         },


         {
          # TODO: 
          'attachment_id':951, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id':229, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': 6,
          'start_date': 5,
         },



         {
          # TODO: 
          'attachment_id': 600, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 3, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 961, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 44, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 5,
          'salary': 3, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 914, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 7, #
          'hourly': None,
          'start_date': 11,
         },


         {
          # TODO: 
          'attachment_id': 496, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 4, 
          'department': 5,
          'salary': 7, #
          'hourly': None,
          'start_date': 8,
         },



         {
          # TODO: 
          'attachment_id':910, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 909, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': 4,
         },

         {
          # TODO: 
          'attachment_id': 93, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 7, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 911, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 177, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 5,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 283, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': 2,
          'salary': 5, #
          'hourly': 6,
          'start_date': 3,
         },



         {
          # TODO: 
          'attachment_id':936, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 5, #
          'hourly': None,
          'start_date': 4,
         },



         {
          # TODO: 
          'attachment_id': 912, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 709, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': 5,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 289, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


#

         {
          # TODO: 
          'attachment_id': 39, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 3, #
          'hourly': 4,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id': 51, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 4,
          'salary': 1, #
          'hourly': 2,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 76, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 3,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 120, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': 3,
          'salary': 5, #
          'hourly': 7,
          'start_date': 1,
         },


         {
          # TODO: 
          'attachment_id': 131, #
          'first_data_line_number': None,
          'last_name': 3, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 4, 
          'department': 5,
          'salary': 8, #
          'hourly': 7,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 148, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 4, 
          'department': 5,
          'salary': 10, #
          'hourly': 9,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id':159, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id': 162, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': 0,
          'salary': 3, #
          'hourly': None,
          'start_date': 2,
         },



         {
          # TODO: 
          'attachment_id': 192, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 5, 
          'department': 4,
          'salary': 8, #
          'hourly': 9,
          'start_date': 6,
         },



         {
          # TODO: 
          'attachment_id':196, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': None,
          'salary': 3, #
          'hourly': 2,
          'start_date': None, # 0
         },


         {
          # TODO: 
          'attachment_id': 214, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 4, 
          'department': 3,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 242, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 6, #
          'hourly': 5,
          'start_date': None, # 4
         },


         {
          # TODO: 
          'attachment_id': 255, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 2, 
          'middle_initial': 3,
          'title': 6, 
          'department': 8,
          'salary': 10, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 337, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': 2,
          'title': 4, 
          'department': 5,
          'salary': 7, #
          'hourly': 6,
          'start_date': 8,
         },


         {
          # TODO: 
          'attachment_id': 361, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': 2,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },

         {
          # TODO: 
          'attachment_id': 366, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 3, #
          'hourly': 4,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id': 388, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 6, #
          'hourly': 5,
          'start_date': 1,
         },

         {
          # TODO: 
          'attachment_id': 389, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 2,
          'salary': 6, #
          'hourly': None,
          'start_date': None, #8
         },


         {
          # TODO: 
          'attachment_id': 414, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': 6,
          'start_date': 7,
         },


         {
          # TODO: 
          'attachment_id': 436, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 5, 
          'department': 6,
          'salary': 3, #
          'hourly': None,
          'start_date': 7,
         },


         {
          # TODO: 
          'attachment_id': 477, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 4, #
          'hourly': 5,
          'start_date': None, #0
         },


         {
          # TODO: 
          'attachment_id': 482, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 7, 
          'department': 6,
          'salary': 3, #
          'hourly': 4,
          'start_date': 2,
         },


         {
          # TODO: 
          'attachment_id': 485, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': 6,
          'start_date': None, #7
         },

         {
          # TODO: 
          'attachment_id': 516, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 6, #
          'hourly': 4,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 520, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 5, 
          'department': 3,
          'salary': 7, #
          'hourly': 6,
          'start_date': 4,
         },

         {
          # TODO: 
          'attachment_id': None,#670, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 0, 
          'department': None,
          'salary': 8, #
          'hourly': 5,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 726, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': 5,
          'salary': 3, #
          'hourly': None,
          'start_date': 2,
         },


         {
          # TODO: 
          'attachment_id': 756, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': 6,
          'start_date': 7,
         },


         {
          # TODO: 
          'attachment_id': 762, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title':4, 
          'department': 2,
          'salary': 5, #
          'hourly': 6,
          'start_date': None, #3
         },


         {
          # TODO: 
          'attachment_id': 763, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 4, #
          'hourly': None,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 783, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 5, #
          'hourly': 6,
          'start_date': 7,
         },


         {
          # TODO: 
          'attachment_id': 789, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 4,
          'salary': 8, #
          'hourly': None,
          'start_date': None, #10
         },

         {
          # TODO: 
          'attachment_id': 801, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': None, #
          'hourly': 5,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 813, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 4, #
          'hourly': None,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 832, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': None,
          'salary': 3, #
          'hourly': 2,
          'start_date': None, #0
         },


         {
          # TODO: 
          'attachment_id': 845, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 5, #
          'hourly': 6,
          'start_date': 4,
         },

         {
          # TODO: 
          'attachment_id': 854, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 0,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 861, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 5,
          'salary': 3, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 864, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 3, #
          'hourly': 2,
          'start_date': None, #4
         },


         {
          # TODO: 
          'attachment_id': 866, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 4,
          'salary': 6, #
          'hourly': None,
          'start_date': 8,
         },

         {
          # TODO: 
          'attachment_id': 869, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 4, #
          'hourly': 3,
          'start_date': 2,
         },


         {
          # TODO: 
          'attachment_id': 939, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 1,
          'salary': 4, #
          'hourly': None,
          'start_date': None, #2
         },


         {
          # TODO: 
          'attachment_id': 955, #
          'first_data_line_number': None,
          'last_name': 6, #
          'first_name': 5, 
          'middle_initial': None,
          'title': 4, 
          'department': None,
          'salary': 9, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id':960, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 4,
          'salary': None, #
          'hourly': 1,
          'start_date': 2,
         },


         {
          # TODO: 
          'attachment_id': 966, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': 2,
         },






         {
          # TODO: 
          'attachment_id': 128, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': None, 
          'department': 2,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': None, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id':None, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: wtf
          'attachment_id': 977, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 2, 
          'middle_initial': None,
          'title': 5, 
          'department': 6,
          'salary': 7, #
          'hourly': None,
          'start_date': 8,
         },



         {
          # TODO: 
          'attachment_id': 978, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 907, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id':990, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 4, 
          'department': 2,
          'salary': 7, #
          'hourly': 6,
          'start_date': 8,
         },



         {
          # TODO: 
          'attachment_id': 986, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': 5,
         },



         {
          # TODO: 
          'attachment_id': None, #741, # looks like paid to date
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 4, #
          'hourly': None,
          'start_date': 3,
         },



         {
          # TODO: 
          'attachment_id': 962, #
          'first_data_line_number': None,
          'last_name': 6, #
          'first_name': 5, 
          'middle_initial': None,
          'title': 4, 
          'department': None,
          'salary': 9, #
          'hourly': 10,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 975, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 0,
          'salary': 4, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 849, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 5, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 838, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 11, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 834, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 3, 
          'middle_initial': 4,
          'title': 6, 
          'department': 7,
          'salary': 9, #
          'hourly': None,
          'start_date': 10,
         },

         {
          # TODO: 
          'attachment_id': 49, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 4, #
          'hourly': None,
          'start_date': 3,
         },

         {
          # TODO: 
          'attachment_id': 814, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 4, #
          'hourly': None,
          'start_date': 3,
         },



         {
          # TODO: 
          'attachment_id': 36, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 4, #
          'hourly': 5,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 62, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 5, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 72, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 6, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 78, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },



         {
          # TODO: 
          'attachment_id': 80, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },



         {
          # TODO: 
          'attachment_id': 209, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': 3,
         },



         {
          # TODO: 
          'attachment_id': 228, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 4, #
          'hourly': 3,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 306, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 5, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 307, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 309, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': 3,
         },



         {
          # TODO: 
          'attachment_id': 314, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 357, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 364, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 5, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 369, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 371, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },



         {
          # TODO: 
          'attachment_id': 375, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },



         {
          # TODO: 
          'attachment_id': 386, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': None,
          'salary': 5, #
          'hourly': 6,
          'start_date': 7,
         },


         {
          # TODO: 
          'attachment_id': 392, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 5, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 395, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id': 400, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 4, #
          'hourly': None,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 437, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 2, 
          'middle_initial': 1,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6
         },


         {
          # TODO: 
          'attachment_id': 463, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 2, #
          'hourly': None,
          'start_date': 1,
         },


         {
          # TODO: 
          'attachment_id': 493, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 2, 
          'middle_initial': None,
          'title': 4, 
          'department': 5,
          'salary': 6, #
          'hourly': None,
          'start_date': 7,
         },


         {
          # TODO: 
          'attachment_id': 534, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 542, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 3, 
          'department':4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 592, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': 5,
         },



         {
          # TODO: 
          'attachment_id': 648, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 3, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 650, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 6,
          'salary': 8, #
          'hourly': None,
          'start_date': 10,
         },


         {
          # TODO: 
          'attachment_id': 663, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 675, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 827, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 3, 
          'middle_initial': 4,
          'title': 6, 
          'department': 7,
          'salary': 9, #
          'hourly': None,
          'start_date': 10,
         },


         {
          # TODO: 
          'attachment_id': 871, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 6, 
          'department': 8,
          'salary': 10, #
          'hourly': None,
          'start_date': 12,
         },


         {
          # TODO: 
          'attachment_id': 343, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 487, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 0,
          'salary': 4, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 653, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 2, 
          'middle_initial': None,
          'title': 4, 
          'department': 6,
          'salary': 8, #
          'hourly': None,
          'start_date': 10,
         },


         {
          # TODO: 
          'attachment_id': 712, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 6, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 82, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 508, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 995, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 4, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 106, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id': 150, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 2,
          'salary': 5, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 195, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 5,
          'salary': 7, #
          'hourly': 6,
          'start_date': 3,
         },

         {
          # TODO: 
          'attachment_id': 538, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 8, 
          'department': None,
          'salary': 4, #
          'hourly': None,
          'start_date': 6,
         },

         {
          # TODO: 
          'attachment_id':1042, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 14, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 518, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': 1,
         },



         {
          # TODO: 
          'attachment_id': 227, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 5, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': None , #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 387, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 6, #
          'hourly': 5,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 152, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 1043, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 7, #
          'hourly': 6,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 1044, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 2, 
          'middle_initial': None,
          'title': 4, 
          'department': 3,
          'salary': 6, #
          'hourly': 5,
          'start_date': 8,
         },


         {
          # TODO: 
          'attachment_id': 1046, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 3, #
          'hourly': None,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id': 1049, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 6, 
          'department': 4,
          'salary': 7, #
          'hourly': 8,
          'start_date': 3,
         },


         {
          # TODO:  
          'attachment_id': 944, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 5, 
          'department': None,
          'salary': 7, #
          'hourly': None,
          'start_date': 3,
         },



         {
          # TODO: 
          'attachment_id': 784, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 1050, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 1, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 1051, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': None, #
          'hourly': 2,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 213, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1052, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 4, #
          'hourly': 3,
          'start_date': 5,
         },

         {
          # TODO: 
          'attachment_id': 1053, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 6, #
          'hourly': None,
          'start_date': 4,
         },

         {
          # TODO: 
          'attachment_id': 346, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 5, #
          'hourly': None,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 344, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 1, #
          'hourly': 2,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id': 490, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1008, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 5,
          'salary': None, #
          'hourly': 2,
          'start_date': 3,
         },
         

         {
          # TODO: 
          'attachment_id': 1018, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 1030, #
          'first_data_line_number': None,
          'last_name': 7, #
          'first_name': 10, 
          'middle_initial': None,
          'title': 31, 
          'department': None,
          'salary': 29, #
          'hourly': 26,
          'start_date': 18,
         },


         {
          # TODO: 
          'attachment_id': 1032, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 5, 
          'department': None,
          'salary': 6, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1038, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 412, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': 5,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1002, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 5,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1020, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 3, 
          'department': 4,
          'salary': 6, #
          'hourly': None,
          'start_date': 5,
         },

         {
          # TODO: 
          'attachment_id': 1024, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 1001, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 7, #
          'hourly': 3,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id': 243, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 7, 
          'department': 4,
          'salary': 8, #
          'hourly': 6,
          'start_date': 3,
         },


         {
          # TODO: 
          'attachment_id': 1072, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 2, 
          'middle_initial': 3,
          'title': 7, 
          'department': 8,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },


         {
          # TODO: 
          'attachment_id':1074, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 1, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: bad one where tabula page #s specified 
          'attachment_id': 835, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': None,
          'salary': 5, #
          'hourly': None,
          'start_date': 2,
         },


         {
          # TODO: 
          'attachment_id': 971, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title':10, 
          'department': None,
          'salary': 19, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: wtf ... why do salary, last name and title share indices? 
          'attachment_id':1091, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': 5,
         },

         {
          # TODO: 
          'attachment_id': 1093, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 3, #
          'hourly': 4,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1096, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': 3, 
          'department': 2,
          'salary': 4, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 1098, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 1,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1097, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1107, #
          'first_data_line_number': 2,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 5,
          'salary': 4, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 1103, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 1106, #
          'first_data_line_number': None,
          'last_name': 3, #
          'first_name': 4, 
          'middle_initial': 5,
          'title': 2, 
          'department': 1,
          'salary': 7, #
          'hourly': None,
          'start_date': 6,
         },

         {
          # TODO: 
          'attachment_id': 1108, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': None,
          'salary': 7, #
          'hourly': None,
          'start_date': 5,
         },

         {
          # TODO: 
          'attachment_id': 1113, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': None, 
          'department': 4,
          'salary': 9, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 558, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 7, #
          'hourly': 6,
          'start_date': 5,
         },

         {
          # TODO: 
          'attachment_id': 1040, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1116, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': 3, 
          'middle_initial': 4,
          'title': 6, 
          'department': 1,
          'salary': 7, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 1120, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 984, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': 7, 
          'department': 8,
          'salary': 14, #
          'hourly': None,
          'start_date': 4,
         },


         {
          # TODO: 
          'attachment_id': 566, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 4, #
          'hourly': 3,
          'start_date': 2,
         },

         {
          # TODO: 
          'attachment_id': 86, #
          'first_data_line_number': None,
          'last_name': 3, #
          'first_name': 1, 
          'middle_initial': 2,
          'title': None, 
          'department':7,
          'salary': 9, #
          'hourly': None,
          'start_date': 4,
         },

         {
          # TODO: 
          'attachment_id': 595, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 3, 
          'department': 1,
          'salary': 7, #
          'hourly': None,
          'start_date': 5,
         },



         {
          # TODO: 
          'attachment_id': 438, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 3, #
          'hourly': None,
          'start_date': 4,
         },

         {
          # TODO: 
          'attachment_id': 647, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 4, 
          'department': 7,
          'salary': 8, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 124, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': 1,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 696, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': 7, 
          'department': 6,
          'salary': 5, #
          'hourly': 4,
          'start_date': 2,
         },


         {
          # TODO: 
          'attachment_id': 748, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': None,
          'salary': 4, #
          'hourly': None,
          'start_date': 3,
         },

         {
          # TODO: 
          'attachment_id': 820, #
          'first_data_line_number': None,
          'last_name': 4, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 5, #
          'hourly': None,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 822, #
          'first_data_line_number': None,
          'last_name': 2, #
          'first_name': None, 
          'middle_initial': None,
          'title': 6, 
          'department': None,
          'salary': 3, #
          'hourly': 4,
          'start_date': 5,
         },


         {
          # TODO: 
          'attachment_id': 900, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': 5,
          'start_date': None,
         },


         {
          # TODO: 
          'attachment_id': 921, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 1, #
          'hourly': 3,
          'start_date': 2,
         },




         {
          # TODO: 
          'attachment_id': 940, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 0, 
          'middle_initial': None,
          'title': 7, 
          'department': 6,
          'salary': 5, #
          'hourly': 4,
          'start_date': 2,
         },


         {
          # TODO: 
          'attachment_id': 335, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': 5, 
          'department': 6,
          'salary': 3, #
          'hourly': 4,
          'start_date': 7,
         },


         {
          # TODO: 
          'attachment_id': 1123, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': None,
          'salary': 2, #
          'hourly': None,
          'start_date': None,
         },



         {
          # TODO: 
          'attachment_id': 1036, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': 2, 
          'middle_initial': None,
          'title': 3, 
          'department': 4,
          'salary': 5, #
          'hourly': None,
          'start_date': 6,
         },



         {
          # TODO: 
          'attachment_id': 1065, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 1,
          'salary': 3, #
          'hourly': None,
          'start_date': None,
         },

         {
          # TODO: 
          'attachment_id': 58, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 1, 
          'department': 2,
          'salary': 8, #
          'hourly': None,
          'start_date': 3,
         },

         {
          # TODO: 
          'attachment_id': 1124, #
          'first_data_line_number': None,
          'last_name': 1, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': 7, #
          'hourly': None,
          'start_date': 2,
         },

         {
          # TODO: wtf dept 
          'attachment_id': 1125, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': 1, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': 5,
          'start_date': 6,
         },

]


special_case_ids = [x['attachment_id'] for x in cases]

"""
### SAMPLE CONFIG ###



         {
          # TODO: 
          'attachment_id':None, #
          'first_data_line_number': None,
          'last_name': None, #
          'first_name': None, 
          'middle_initial': None,
          'title': None, 
          'department': None,
          'salary': None, #
          'hourly': None,
          'start_date': None,
         },



"""

