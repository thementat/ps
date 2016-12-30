
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource
from django.db import connection
from prop.models import Muni, Parcel, Lot, Property, Value, Zone, Plan, Policy
from impo.models import Source, Source_Link
from impo.models import IParcel, IZone, IPolicy, ILot, IValue, IProperty, IValue, IAddress

Source.objects.get(pk=17).getdata()
