# IPython log file

from matt_utils.parse.parse_attachments import init_parse
agencies = """Bellwood
Bloom Township
Broadview
Brookfield
Burlington
Burnham
Charleston
Chicago State University
Crystal Lake
Dekalb
Dekalb County
Elmwood Park
Forest View
Fox River Grove
Grayslake
Green Oaks
Hazel Crest
Hometown
Indian Head Park
Justice
Knox County
Lake County (IN)
Lasalle
Lasalle County
Lemont Township
Lincolnshire
Livingston County
Lockport
Markham
Mason County
North Barrington
Northbrook
Northlake
Oak Lawn
Palos Park
Palos Township
Piatt County
Regional Transportation Authority
Richton Park
Ringwood
Robbins
Roselle
Shelby County
South Chicago Heights
Spring Grove
Stark County
Stickney
Stickney Township
Volo
Wadsworth
Wayne County
West Chicago
Western Springs""".split('\n')
agencies
len(agencies)
get_ipython().magic(u'pinfo %history')
get_ipython().magic(u'history -g history')
get_ipython().magic(u'history -g histoz')
get_ipython().magic(u'pinfo %history')
get_ipython().magic(u'pinfo %hist')
get_ipython().magic(u'hist -g get_agency_attachments')
get_ipython().magic(u'hist -g import get_agency_attachments')
from matt_utils.responses.response_report import get_agency_attachments
len(agencies)
for agency in agencies:
    a = Agency.object.get(name=agency)
    for att in get_agency_attachments(a):
        print att.id
        
from apps.agency.models import Agency       
att_ids = []
for agency in agencies:
    try:
        a = Agency.objects.get(name__icontains=agency)
        for ext in get_agency_attachments(a):
            if 'xls' in ext:
                for att in get_agency_attachments(a)[ext]:
                    att_ids.append(att.id)                
    except Exception, e:
        print '*Exception:', agency, e
        
len(att_ids)
att_ids
get_ipython().magic(u'logstart problem_xls.py')
exit()
