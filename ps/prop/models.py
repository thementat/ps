# from django.db import models

#--------------------------------------------------------------
#Version History
#
# 20161119 - Changing the Parcel Lot relationship to a simple one to many
# 20161120 - Added Zoning
# 20161202 - Added some signals to update parcel_zone  and parcel_policy relationships
# 20161206 - Fixed the Parcel import to get rid of bulk updating and raw sql
# 20161206 - removed the geometry firld from lots, and added a derived field
# 20161206 - got rid of the policybound and zonebound tables
# 20161208 - renamed the import tables
#--------------------------------------------------------------

# Create your models here.

from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.db.models import Union 
from django.contrib.gis.db.models.functions import Area, Intersection, Transform
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from impo.models import IParcel, ILot, IZone, IPolicy, IProperty, IValue


class Muni(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    srid = models.IntegerField(null=True)
    
    def download_sources(self):
        pass
    
class Lot(models.Model):
    muni = models.ForeignKey(Muni, on_delete=models.CASCADE, db_index=True)
    ext = models.CharField(max_length=50, null=True, db_index=True)
    
    @property
    def geom(self):
        geometry =  Parcel.objects.filter(lot=self).aggregate(Union('geom')).get('geom__union')
        if geometry.geom_type == 'Polygon':
            geometry = MultiPolygon(geometry)
        return geometry

    @classmethod
    def merge(cls, m):
        
        #delete lots where parcels don't exist
        ILot.objects.filter(parcel__isnull=True).delete()
        
        #delete lots from deprecated parcels (just protection...)
        Lot.objects.filter(parcel__depdate__isnull=False).delete()
        
        #delete lot if the makeup of its corresponding parcel_lot changes
        #delete where there are missing parcels in the new Imp_Lot
        Lot.objects.filter(parcel__ilot__isnull=True).delete()
        
        #delete where there are new parcels in the new Imp_Lot
        #TODO: check this... I think there should be t3.id = prop_parcel.lot_id AND T3.
        Lot.objects.filter(ilot__lot__parcel__isnull=True).delete()
        
        # now delete lots that no longer exist in the Imp_Lot table
        Lot.objects.filter(ilot__isnull=True).delete()
        
        # create the aggregated lots
        il = ILot.objects.all()
        
        nl = [] # new lots
        np = [] # new parcels
        pg = [] # parcels, grouped by lot
        for grp in il.values('grp').distinct():
            parcelgroup = Parcel.objects.filter(ilot__grp=grp['grp']).distinct() #grab a group of Parcel objects
            nl.append(Lot(muni=m, ext=grp['grp'])) 
            pg.append(parcelgroup)
        nl = Lot.objects.bulk_create(nl)   
        for n, l in enumerate(nl):
            pg[n].update(lot=l)
        
class Zone(models.Model):
    muni = models.ForeignKey(Muni, on_delete=models.CASCADE, db_index=True)
    code = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=250, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    min_area = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    min_width = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    min_depth = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    fsr = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    uph = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    height = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    
    @classmethod
    def merge(cls, muni):
        
        agg_zone = IZone.objects.values('code', 'name', 'url').annotate(geom=Union('geom'))
        for zone in agg_zone:
            if zone['geom'].geom_type == 'Polygon':
                zone['geom'] = MultiPolygon(zone['geom'])
            
            obj, created = Zone.objects.update_or_create(
                            muni=muni, code=zone['code'], 
                            defaults={'name': zone['name'],
                                      'url' : zone['url'],
                                      'geom' : zone['geom']})

@receiver(post_save, sender=Zone)
def update_Parcel_Zone_Zonechange(sender, update_fields, created, instance, **kwargs):
    if created or update_fields is 'geom':
                
        # find all Parcel objects that intersect the new Zone
        all_p = (Parcel.objects.filter(muni=instance.muni).filter(geom__intersects=instance.geom)
                    .annotate(area=Area(Transform(Intersection('geom', instance.geom), instance.muni.srid))))
        
        # Find all existing Parcel_Zone relationships
        epz = Parcel_Zone.objects.filter(parcel__muni=instance.muni, zone=instance)
        
        #delete any previously existing Parcel_Zone objects that are no longer used
        epz.exclude(parcel__in=all_p).delete() 
        
        for p in all_p:
            if p.area.sq_m > 1:
                obj, created = Parcel_Zone.objects.update_or_create(
                    parcel=p, zone=instance, 
                    defaults={'area': p.area.sq_m})

class Plan(models.Model):
    muni = models.ForeignKey(Muni, on_delete=models.CASCADE, db_index=True)
    code = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=150, null=True)
    priority = models.IntegerField(null=True)
    
class Policy(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, db_index=True)
    code = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=150, null=True)
    url = models.IntegerField(null=True)
    fsr = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    uph = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    height = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    geom = models.MultiPolygonField(srid=4326, null=True)
    zone = models.ManyToManyField(Zone, db_index=True)
    
    @classmethod
    def merge(cls, muni):
        
        agg_policy = IPolicy.objects.values('plan_id', 'code', 'name', 'url').annotate(geom=Union('geom'))
        for policy in agg_policy:
            obj, created = Policy.objects.update_or_create(
                            muni=muni, plan=['plan_id'], code=policy['code'], 
                            defaults={'name': policy['name'],
                                      'url' : policy['url'],
                                      'geom' : policy['geom']})
    
@receiver(post_save, sender=Policy)
def update_Parcel_Policy_Policychange(sender, update_fields, created, instance, **kwargs):
    if created or update_fields is 'geom':
                
        # find all Parcel objects that intersect the new Policy
        all_p = (Parcel.objects.filter(muni=instance.plan.muni).filter(geom__intersects=instance.geom)
                    .annotate(area=Area(Transform(Intersection('geom', instance.geom), instance.plan.muni.srid))))
        
        # Find all existing Parcel_Policy relationships
        epp = Parcel_Policy.objects.filter(parcel__muni=instance.plan.muni, policy=instance)
        
        #delete any previously existing Parcel_Policy objects that are no longer used
        epp.exclude(parcel__in=all_p).delete() 
        
        for p in all_p:
            if p.area.sq_m > 1:
                obj, created = Parcel_Policy.objects.update_or_create(
                    parcel=p, policy=instance, 
                    defaults={'area': p.area.sq_m})

class Parcel(models.Model):
    muni = models.ForeignKey(Muni, on_delete=models.CASCADE, db_index=True)
    lot = models.ForeignKey(Lot, on_delete=models.SET_NULL, db_index=True, null=True)
    zone = models.ManyToManyField(Zone, through='Parcel_Zone', blank=True)
    policy = models.ManyToManyField(Policy, through='Parcel_Policy', blank=True)
    ext = models.CharField(max_length=50, null=True, db_index=True) 
    ext2 = models.CharField(max_length=50, null=True, db_index=True) 
    unit = models.CharField(max_length=20, null=True)
    street_number = models.IntegerField(null=True)
    street_prefix = models.CharField(max_length=20, null=True)
    street = models.CharField(max_length=50, null=True)
    street_type = models.CharField(max_length=20, null=True)
    street_suffix = models.CharField(max_length=20, null=True)
    postal = models.CharField(max_length=20, null=True)
    depdate = models.DateField(null=True)
    geom = models.MultiPolygonField(srid=4326)
    
    @classmethod
    def merge(cls, muni):
        cursor = connection.cursor()
        
                
                
        
        all_ip = IParcel.objects.all()
        
        #deprecate parcels not in import
        Parcel.objects.filter(muni=muni, depdate__isnull=True).filter(iparcel__isnull=True).update(depdate=datetime.date.today())
        
        #get or create all new parcels, and save if changed
        for ip in all_ip:
            obj, created = Parcel.objects.update_or_create(
                id=ip.parcel_id, 
                defaults={'muni' : muni
                          , 'ext' : ip.txt
                          , 'ext2' : ip.txt2
                          , 'unit' : ip.unit
                          , 'street_number' : ip.street_number
                          , 'street_prefix' : ip.street_prefix
                          , 'street' : ip.street
                          , 'street_type' : ip.street_type
                          , 'street_suffix' : ip.street_suffix
                          , 'postal' : ip.postal
                          , 'geom' : ip.geom})

        
        
@receiver(post_save, sender=Parcel)
def update_Parcel_Zone_Parcel_Policy_Parcelchange(sender, update_fields, created, instance, **kwargs):
    if created or update_fields is 'geom':
        
        # find all Zone objects that intersect the new Parcel
        all_z = (Zone.objects.filter(muni=instance.muni).filter(geom__intersects=instance.geom)
                    .annotate(area=Area(Transform(Intersection('geom', instance.geom), instance.muni.srid))))
        
        # Find all existing Parcel_Zone relationships
        epz = Parcel_Zone.objects.filter(parcel=instance, zone__muni=instance.muni)
        
        #delete any previously existing Parcel_Zone objects that are no longer used
        epz.exclude(zone__in=all_z).delete() 
        
        for z in all_z:
            if z.area.sq_m > 1:
                obj, created = Parcel_Zone.objects.update_or_create(
                    parcel=instance, zone=z, 
                    defaults={'area': z.area.sq_m})

        # find all Policy objects that intersect the new Parcel
        all_p = (Policy.objects.filter(plan__muni=instance.muni).filter(geom__intersects=instance.geom)
                    .annotate(area=Area(Transform(Intersection('geom', instance.geom), instance.muni.srid))))
        
        # Find all existing Parcel_Policy relationships
        epp = Parcel_Policy.objects.filter(parcel=instance, policy__plan__muni=instance.muni)
        
        #delete any previously existing Parcel_Zonebound objects that are no longer used
        epp.exclude(policy__in=all_p).delete() 
        
        for p in all_p:
            if p.area.sq_m > 1:
                obj, created = Parcel_Policy.objects.update_or_create(
                    parcel=instance, policy=p, 
                    defaults={'area': p.area.sq_m})

class Parcel_Zone(models.Model):
    #TODO: add a unique constraint on parcel & zone
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, db_index=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, db_index=True)
    area = models.DecimalField(null=True, max_digits=20, decimal_places=4)

class Parcel_Policy(models.Model):
    #TODO: add a unique constraint on parcel & policy
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, db_index=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, db_index=True)
    area = models.DecimalField(null=True, max_digits=20, decimal_places=4)

class Property(models.Model):
    # represents an owned unit
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, db_index=True)
    ext = models.CharField(max_length=50, null=True, db_index=True) #external identifier
    ext2 = models.CharField(max_length=50, null=True, db_index=True) #external identifier
    unit = models.CharField(max_length=20, null=True)
    street_number = models.IntegerField(null=True)
    street_prefix = models.CharField(max_length=20, null=True)
    street = models.CharField(max_length=50, null=True)
    street_type = models.CharField(max_length=20, null=True)
    street_suffix = models.CharField(max_length=20, null=True)
    postal = models.CharField(max_length=20, null=True)

    @classmethod
    def merge(cls):
        cursor = connection.cursor()
        ##modify any changed properties (not sure if this ever happens)
        cursor.execute("""UPDATE """ + Property._meta.db_table + """ p 
                        SET    ext = ip.txt
                            , ext2 = ip.txt2
                            , unit = ip.unit
                            , street_number = ip.street_number
                            , street_prefix = ip.street_prefix
                            , street = ip.street
                            , street_type = ip.street_type
                            , street_suffix = ip.street_type
                            , postal = ip.postal
                        FROM    impo_iproperty ip
                        WHERE    p.id = ip.parcel_id
                            AND (p.ext <> ip.txt
                            OR p.ext2 <> ip.txt2
                            OR p.unit <> ip.unit
                            OR p.street_number <> ip.street_number
                            OR p.street_prefix <> ip.street_prefix
                            OR p.street <> ip.street
                            OR p.street_type <> ip.street_type
                            OR p.street_suffix <> ip.street_type
                            OR p.postal <> ip.postal)""")
        
        # delete any parcels that no longer exist
        Property.objects.filter(parcel__iproperty__isnull=True).delete()
        
        # create new properties
        cursor.execute("""INSERT INTO """ + Property._meta.db_table + """ 
                                (parcel_id
                                , ext
                                , ext2
                                , unit
                                , street_number
                                , street_prefix
                                , street
                                , street_type
                                , street_suffix
                                , postal)
                        SELECT  ip.parcel_id
                                , ip.txt
                                , ip.txt2
                                , ip.unit
                                , ip.street_number
                                , p.street_prefix
                                , p.street
                                , p.street_type
                                , p.street_suffix
                                , ip.postal
                        FROM    """ + IProperty._meta.db_table + """ ip
                        JOIN    """ + Parcel._meta.db_table + """ p
                                ON ip.parcel_id = p.id
                        LEFT JOIN """ + Property._meta.db_table + """ o
                                ON o.ext = ip.txt
                        WHERE    ip.parcel_id IS NOT NULL
                                AND o.ext IS NULL""")
            
class Value(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_index=True)
    valdate = models.DateField(null=True)
    landval = models.BigIntegerField(null=True)
    impval = models.BigIntegerField(null=True)
    val = models.BigIntegerField(null=True)
    valsrc = models.CharField(max_length=20, null=True)
    
    
    @classmethod
    def merge(cls):
        cursor = connection.cursor()
        
        

        
        
        ##modify any changed values (not sure if this ever happens)
        cursor.execute("""UPDATE """ + Value._meta.db_table + """ p 
                        SET valdate = CAST(ip.valdate AS date)
                            , landval = ip.landval
                            , impval = ip.impval
                            , val = ip.val
                        FROM    """ + IValue._meta.db_table + """ ip
                        WHERE    p.property_id = ip.property_id
                            AND p.valdate = CAST(ip.valdate AS date)
                            """)
        
        # delete any parcels that no longer exist
        # TODO: deprecate
        # Value.objects.filter(property__imp_property__isnull=True).delete()
        
        # create new values
        cursor.execute("""INSERT INTO """ + Value._meta.db_table + """ 
                                (property_id
                                , valdate
                                , landval
                                , impval
                                , val
                                )
                        SELECT  ip.property_id
                                , CAST(ip.valdate AS date)
                                , ip.landval
                                , ip.impval
                                , ip.val
                        FROM    """ + IValue._meta.db_table + """ ip
                        LEFT JOIN """ + Value._meta.db_table + """ o
                                ON o.valdate = CAST(ip.valdate AS date)
                                AND o.property_id = ip.property_id
                        WHERE    o.property_id IS NULL""")



