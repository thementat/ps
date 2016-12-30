
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource
from django.db import connection
from prop.models import Muni, Parcel, Lot, Property, Value, Zone, Plan, Policy
from impo.models import Source, Source_Link
from impo.models import IParcel, IZone, IPolicy, ILot, IValue, IProperty, IValue, IAddress

Parcel.objects.all().delete()
Lot.objects.all().delete()
Property.objects.all().delete()
Value.objects.all().delete()
Zone.objects.all().delete()
Policy.objects.all().delete()



Source.objects.get(pk=2).get_data()
Source.objects.get(pk=2).groom()
Parcel.merge(Muni.objects.get(pk=1))
Source.objects.get(pk=5).get_data()
Source.objects.get(pk=5).groom()
Lot.merge(Muni.objects.get(pk=1))
Source.objects.get(pk=3).get_data()
Source.objects.get(pk=3).groom()
Property.merge()
Source.objects.get(pk=4).get_data()
Source.objects.get(pk=4).groom()
Value.merge()
Source.objects.get(pk=13).get_data()
Source.objects.get(pk=13).groom()
Zone.merge(Muni.objects.get(pk=1))



Source.objects.get(pk=6).get_data()
Source.objects.get(pk=6).groom()
Parcel.merge(Muni.objects.get(pk=2))
Source.objects.get(pk=7).get_data()
Source.objects.get(pk=7).groom()
Lot.merge(Muni.objects.get(pk=2))
Source.objects.get(pk=8).get_data()
Source.objects.get(pk=8).groom()
Property.merge()
Source.objects.get(pk=9).get_data()
Source.objects.get(pk=9).groom()
Value.merge()
Source.objects.get(pk=14).get_data()
Source.objects.get(pk=14).groom()
Zone.merge(Muni.objects.get(pk=2))


Source.objects.get(pk=12).get_data()
Source.objects.get(pk=12).groom()
Source.objects.get(pk=1).get_data()
Source.objects.get(pk=1).groom()
Parcel.merge(Muni.objects.get(pk=3))



Source.objects.get(pk=16).get_data()

Lot.merge(Muni.objects.get(pk=3))
Source.objects.get(pk=10).get_data()
Source.objects.get(pk=10).groom()
Property.merge()
Source.objects.get(pk=11).get_data()
Source.objects.get(pk=11).groom()
Value.merge()
Source.objects.get(pk=15).get_data()
Source.objects.get(pk=15).groom()
Zone.merge(Muni.objects.get(pk=3))


all_p = Parcel.objects.order_by('-street_number').distinct('num')
all_p = Parcel.objects.all()

Parcel.objects.update(street_type=street[street[::-1].find(' ')+1:], street=street[:street[::-1].find(' ')])









from django.db.models import Sum
from django.contrib.gis.db.models.functions import Area, Intersection, Transform
from django.contrib.gis.geos import Point, MultiPolygon, GEOSGeometry
from django.contrib.gis.db.models import Union
from prop.models import Muni, Lot, Parcel, Zone, Plan, Policy, Parcel_Zone, Parcel_Policy


# create a fictitious zone & policy for testing by using geometries from parcels or lots
m = Muni.objects.get(pk=1)

z = Zone.objects.get(pk=4)



p = Parcel.objects.get(pk=266659)
p2 = Parcel(muni=m, ext='test', geom=p.geom)


z = Zone(muni=m, code='test', geom=MultiPolygon(Parcel.objects.filter(street='WALNUT GROVE', street_number=9012).aggregate(Union('geom')).get('geom__union')))
z2 = Zone(muni=m, code='test', geom=MultiPolygon(Parcel.objects.filter(street='WALNUT GROVE', street_number=9045).aggregate(Union('geom')).get('geom__union')))


agg_zone = impoZone.objects.values('code', 'name', 'url').annotate(geom=Union('geom'))
for zone in agg_zone:
    obj, created = Zone.objects.update_or_create(
                    muni=muni, code=zone['code'], 
                    defaults={'name': zone['name'],
                              'url' : zone['url'],
                              'geom' : zone['geom']})
    print(time.time()-t)


l = Lot(muni=m, ext='test')
l.save()

Parcel.objects.filter(street='WALNUT GROVE', street_number=9012).update(lot=l)
Parcel.objects.filter(street='WALNUT GROVE', street_number=9045).update(lot=l)           
                
# to aggregate zone data cor lots:
pz = Parcel_Zone.objects.filter(parcel__in=Parcel.objects.filter(lot=l))
area = pz.values('zone').annotate(area=Sum('area'))

cursor.execute("""INSERT INTO impo_ilot (grp, txt)
                                SELECT    txt2
                                        , txt
                                FROM    impo_iparcel
                                        """)



from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource
lm = LayerMapping(eval(self.model_name), fileloc, mapping)
                lm.save()

for n, v in enumerate(Source_Link.objects.filter(source=self)):
                    mapping[v.model_col] = v.source_col
                lm = LayerMapping(eval(self.model_name), fileloc, mapping)
                lm.save()


import requests
import tempfile
import shutil
from os import listdir
import csv

s = Source.objects.get(pk=17)

request = requests.get(s.location, stream=True)
#was the request OK?
#if request.status_code != requests.codes.ok:
    # TODO: Nope, error handling, skip file etc etc etc
#    continue

# Get the filename from the url, used for saving later
file_name = self.location.split('/')[-1]

# Create a temporary file
tfile = tempfile.NamedTemporaryFile()
# Read the streamed image in sections
for block in request.iter_content(1024 * 8):
    # If no more file then stop
    if not block:
        break
    # Write image block to temporary file
    tfile.write(block)
    tfile.seek(0)
# unzip the file if necessary
fileloc = tfile.name
if self.location.split('.')[-1] == 'zip':
    tdir = tempfile.TemporaryDirectory()
    shutil.unpack_archive(tfile.name, tdir.name, format='zip')
    if self.source_type == 'shp':
        # there are often several files in the shapefile zip.  we just want the .shp
        fileloc = tdir.name + '/' + '.'.join(self.location.rsplit('.', 1)[0].rsplit('/')[-1].rsplit('_',1))
    else:
        fileloc = tdir.name + '/' + listdir(tdir.name)[0]
else:
    pass
else:
fileloc = self.location



