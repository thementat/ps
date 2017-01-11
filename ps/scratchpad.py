
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


ogr2ogr --config CARTODB_API_KEY 60dcbd897ae780f97db5090a7160f9a2d7c3222d -t_srs EPSG:4326 -f CartoDB "Carto:thementat" agg.json






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



from mls.models import Paragon_Mail
m = Paragon_Mail.objects.get(pk=5)
m.retrieve()

for field in fields:
    ftype = Listing._meta.get_field(field.name).get_internal_type()
    d = browser.find_element_by_xpath(field.location).get_attribute('innerText')
    if d == '':
        d = None
    elif ftype == 'IntegerField':
        non_decimal = re.compile(r'[^\d.]+')
        d = int(float(non_decimal.sub('', d)))
    elif ftype == 'DecimalField':
        non_decimal = re.compile(r'[^\d.]+')
        d = float(non_decimal.sub('', d))
    elif ftype == 'DateField':
        d = datetime.datetime.strptime(d, '%m/%d/%Y').strftime('%Y-%m-%d')
    
    fvalues[field.name] = d

if d == '':
    d = None
elif ftype == 'IntegerField':
    non_decimal = re.compile(r'[^\d.]+')
    d = int(float(non_decimal.sub('', d)))
elif ftype == 'Decimalfield':
    non_decimal = re.compile(r'[^\d.]+')
    d = float(non_decimal.sub('', d))
elif ftype == 'DateField':
    d = datetime.datetime.strptime(d, '%m/%d/%Y').strftime('%Y-%m-%d')


