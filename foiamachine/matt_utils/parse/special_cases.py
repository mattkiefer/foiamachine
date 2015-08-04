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
         608, # need to check ascii encode issue
         855, # isbe core dump
         246, # dupe of 245
         863, # dupe of 858
        ]


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
          'last_name': 1,
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
          'last_name': 1,
          'first_name': 2,
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
          # TODO: wtf 
          'attachment_id': 465, #
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
          'attachment_id': None, #316, #
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
          'attachment_id': 388, #
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
          'attachment_id': 124, #
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
                 # TODO: csvlook | head -n 20 
          'attachment_id':347, #
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
          'attachment_id': 51, #
          'first_data_line_number': None,
          'last_name': 1, #
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
          # TODO: wtf no names
          'attachment_id':None, # 297, #
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
          # TODO: wtf no names
          'attachment_id': 289, # 297, #
          'first_data_line_number': None,
          'last_name': 0, #
          'first_name': None, 
          'middle_initial': None,
          'title': 2, 
          'department': 3,
          'salary': 4, #
          'hourly': None,
          'start_date': None,
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
          'salary': 6, #
          'hourly': None,
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




]



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

