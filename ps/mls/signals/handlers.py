'''
Created on Jan 12, 2017

@author: chrisbradley
'''

from django.db.models import F
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from mls.models import Listing
from prop.models import Parcel_Zone, Zone, Parcel, Property, Use, Street

@receiver(post_save, sender=Listing)
def test_subdividable_lot(sender, update_fields, created, instance, **kwargs):
    subdividable = False
    if (created 
        and instance.status=='Active' 
        and instance.title=='Freehold NonStrata'
        and instance.property is not None):
            # Get all zones where property has enough area zoned for subdivision
            all_z = Zone.objects.filter(parcel_zone__parcel__property=instance.property, parcel_zone__area__gt=F('min_area') * 2)
            
            #for all single family zones
            for z in all_z:
                #test for minimum frontage requirement
                if 'SF' in list(Use.objects.filter(zone=z).values_list('code', flat=True)):
                    
                    #get nearby useable streets, and the lot width as measured from the street
                    # this is approximated by buffering the street to 7.5m + distance to lot, 
                    # and measuring the distance between the points at the edges of the intersection
                    all_s = Street.objects.raw(
                        """SELECT    s.*
                                    , ST_Distance(
                                        ST_PointN(ST_Intersection(ST_Boundary(ST_Buffer(ST_Transform(s.geom, 26910), 7.5 + ST_Distance(ST_Transform(p.geom, m.srid), ST_Transform(s.geom, m.srid)))), 
                                            ST_Transform(p.geom, 26910)), 1)
                                        , ST_PointN(ST_Intersection(ST_Boundary(ST_Buffer(ST_Transform(s.geom, 26910), 7.5 + ST_Distance(ST_Transform(p.geom, m.srid), ST_Transform(s.geom, m.srid)))), 
                                            ST_Transform(p.geom, 26910)), ST_NPoints(ST_Intersection(ST_Boundary(ST_Buffer(ST_Transform(s.geom, 26910), 7.5 + ST_Distance(ST_Transform(p.geom, m.srid), ST_Transform(s.geom, m.srid)))), 
                                            ST_Transform(p.geom, 26910))))
                                            ) AS width
                                FROM    prop_parcel p
                                JOIN    prop_muni m
                                    ON m.id = p.muni_id
                                JOIN     prop_street s
                                    ON ST_Intersects(ST_Transform(ST_Buffer(ST_Transform(p.geom, m.srid), 40), 4326), s.geom)
                                    AND s.type IN ('Road', 'Frontage Road', 'Street Lane')
                                WHERE    p.id = %s""", [instance.property.parcel.id])
                    
                    for s in all_s:
                        if s.width > 2 * z.min_width:
                            subdividable = True
                            
    if subdividable == True:
        pass
        
                    
                    
                    
                


if __name__ == '__main__':
    pass