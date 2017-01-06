# from django.db import models

#--------------------------------------------------------------
#Version History
#
# 20161208 - renamed the import tables
#--------------------------------------------------------------
from django.db import connection

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, MultiPolygon
from django.contrib.gis.utils import LayerMapping
import requests
import tempfile
import shutil
from os import listdir
import csv
from django.apps import apps
import re


# Create your models here.


class Source(models.Model):
    muni = models.ForeignKey('prop.Muni', on_delete=models.CASCADE, db_index=True)
    model_name = models.CharField(max_length=50)
    iparam = models.IntegerField(null=True)
    source_type = models.CharField(max_length=20, null=True)
    location = models.CharField(max_length=250, null=True)
    update_date = models.DateField(null=True)
    
        
    def new_data(self):
        "returns true if updates are available to the Source"
        if self.update_date == self.update_date:
            return True
        else:
            return False
    
    def get_data(self):
        "updates the relevant model with the source data"
        if self.source_type == None:
            return
        
        if self.location[0:4] == 'http':
            #download the file
            request = requests.get(self.location, stream=True)
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
        
        #TODO:test for updated data
        if self.new_data() == False:
            pass
        else:
            if self.source_type == 'ArcGIS':
                pass
            elif self.source_type == 'csv':
                mapping = {}
                eval(self.model_name + '.objects.all().delete()')
                for n, v in enumerate(Source_Link.objects.filter(source=self)):
                    mapping[v.model_col] = v.source_col
                dataReader = csv.reader(open(fileloc), delimiter=',')
                header = dataReader.__next__()
                for row in dataReader:
                    if row[0] != header[0]:
                        modname = apps.get_model(app_label='impo', model_name=self.model_name)
                        mod = modname()
                        for m, s in mapping.items():
                            if row[header.index(s)] == '':
                                dat = None
                            elif mod._meta.get_field(m).get_internal_type() == 'CharField':
                                dat = row[header.index(s)]
                            else:
                                dat = re.sub('[^0-9]','',row[header.index(s)].rsplit('.')[0])
                            setattr(mod, m, dat)
                        mod.save()
                        

            elif self.source_type == 'csvll':
                #csv file with long/lat data (some Surrey Data uses this)
                mapping = {}
                eval(self.model_name + '.objects.all().delete()')
                for n, v in enumerate(Source_Link.objects.filter(source=self)):
                    if v.model_col != 'long' and v.model_col != 'lat':
                        mapping[v.model_col] = v.source_col
                longcol = Source_Link.objects.filter(imp=self, model_col='long').get().source_col
                latcol = Source_Link.objects.filter(imp=self, model_col='lat').get().source_col
                
                dataReader = csv.reader(open(fileloc), delimiter=',')
                header = dataReader.__next__()
                for row in dataReader:
                    if row[0] != header[0]:
                        modname = apps.get_model(app_label='impo', model_name=self.model_name)
                        mod = modname()
                        for m, s in mapping.items():
                            if row[header.index(s)] == '':
                                dat = None
                            elif mod._meta.get_field(m).get_internal_type() == 'CharField':
                                dat = row[header.index(s)]
                            else:
                                dat = re.sub('[^0-9]','',row[header.index(s)].rsplit('.')[0])
                            setattr(mod, m, dat)
                        mod.geom = Point(float(row[header.index(latcol)]), float(row[header.index(longcol)]))
                        mod.save()
                    
            elif self.source_type == None:
                pass
                        
            else:
                # assume it will be a GDAL compatible file format
                l = self.iparam
                if l is None:
                    l = 0
                mapping = {}
                eval(self.model_name + '.objects.all().delete()')
                for n, v in enumerate(Source_Link.objects.filter(source=self)):
                    mapping[v.model_col] = v.source_col
                lm = LayerMapping(eval(self.model_name), fileloc, mapping, layer=l)
                lm.save()
    
    def groom(self):
        modname = apps.get_model(app_label='impo', model_name=self.model_name)
        mod = modname()
        tablename = mod._meta.db_table
        cursor = connection.cursor()
        if self.muni.name == 'Township of Langley':
            if self.model_name == 'IParcel':
                # separate the street names from street types
                cursor.execute("UPDATE " + tablename + " SET street_type = RIGHT(street, STRPOS(REVERSE(street), ' ') - 1)")
                cursor.execute("UPDATE " + tablename + " SET street = SUBSTRING(street, 1, LENGTH(street) - STRPOS(REVERSE(street), ' '))")
                # clean data
                cursor.execute("""UPDATE """ + IParcel._meta.db_table + """
                                SET    street = NULLIF(street, '')
                                        , street_prefix = NULLIF(street_prefix, '')
                                        , street_suffix = NULLIF(street_suffix, '')
                                        , street_type = NULLIF(street_type, '')
                                        , unit = NULLIF(unit, '')
                                        , postal = NULLIF(postal, '')
                                        , txt = NULLIF(txt, '')
                                        , txt2 = NULLIF(txt2, '')
                                        , txt3 = NULLIF(txt3, '')
                                        , street_number = NULLIF(street_number, 0)
                                        , geom = ST_MakeValid(geom)
                                        """)
                # move the objectid from num to txt
                cursor.execute("""UPDATE """ + IParcel._meta.db_table + """
                                SET    txt = num""")
                
                # insert data to lot
                ILot.objects.all().delete()
                cursor.execute("""INSERT INTO """ + ILot._meta.db_table + """ (grp, txt)
                                SELECT    a.grp
                                        , p.txt
                                FROM    (SELECT    CAST(MIN(CAST(txt AS bigint)) + COUNT(txt)*100000000000000 AS character varying) as grp, street, street_number, street_type
                                        FROM    impo_iparcel
                                        WHERE    street IS NOT NULL
                                        GROUP BY street, street_number, street_type) a
                                JOIN    impo_iparcel p
                                        ON a.street = p.street
                                        AND a.street_number = p.street_number
                                        AND a.street_type = p.street_type
                                    """)
                
                # update parcel_id where available
                cursor.execute("""UPDATE    impo_iparcel
                        SET    parcel_id = p.id
                        FROM    prop_parcel p
                        JOIN    impo_iparcel ip
                                ON ip.txt = p.ext
                                AND p.depdate IS NULL
                        """)

            if self.model_name == 'ILot':
                cursor = connection.cursor()
                # populate the internally generated Parcel ids
                cursor = connection.cursor()
                cursor.execute("""UPDATE """ + ILot._meta.db_table + """ t
                                SET     parcel_id = p1.id
                                FROM     prop_parcel p1
                                WHERE    t.txt = p1.ext""")
                # populate the internally generated Lot ids
                cursor.execute("""UPDATE """ + ILot._meta.db_table + """ t
                                SET     parcel_id = p1.id
                                FROM     prop_lot p1
                                WHERE    t.grp = p1.ext""")
                                
            if self.model_name == 'IProperty':
                
                cursor = connection.cursor()
                # Delete duplicate PIDs
                cursor.execute("""DELETE FROM """ + IProperty._meta.db_table + """ p
                                USING impo_iproperty a
                                WHERE p.txt = a.txt
                                    AND p.id < a.id""")
                
                # fill in point values
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """ SET geom = ST_GeomFromText('POINT(' || SUBSTRING(txt3, POSITION(', ' in txt3) + 2, CHAR_LENGTH(txt3) - POSITION(', ' in txt3) - 2) || ' ' || SUBSTRING(txt3, 2, POSITION(', ' in txt3) - 2) || ')', 4326)""")
                #bind values to parcels based on geometry
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """ r
                                SET parcel_id = p.id
                                FROM    prop_parcel p
                                WHERE    ST_Intersects(r.geom, p.geom)""")
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """
                                SET    street = NULLIF(street, '')
                                        , street_prefix = NULLIF(street_prefix, '')
                                        , street_suffix = NULLIF(street_suffix, '')
                                        , street_type = NULLIF(street_type, '')
                                        , unit = NULLIF(unit, '')
                                        , postal = NULLIF(postal, '')""")
                
                # Delete NULL PIDs
                cursor.execute("""DELETE FROM """ + IProperty._meta.db_table + """ p
                                WHERE p.txt IS NULL""")
                # TODO: fill in missing address bits for parcels and properties
                
            if self.model_name == 'IValue':
                cursor = connection.cursor()
                #delete those with no PID
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """
                                SET    valdate = NULLIF(valdate, '')
                                        , txt = NULLIF(txt, '')
                                        """)
                IValue.objects.filter(txt__isnull=True).delete()
                
                # aggregate properties with multiple assessment rolls
                cursor.execute("""INSERT INTO """ + IValue._meta.db_table + """ (landval, impval, txt, valdate)
                                SELECT      SUM(landval)
                                            , SUM(impval)
                                            , txt
                                            , 'Agg'
                                FROM        """ + IValue._meta.db_table + """ 
                                GROUP BY    txt 
                                HAVING     COUNT(txt) > 1""")    
                cursor.execute("""DELETE FROM """ + IValue._meta.db_table + """ d
                                WHERE    d.txt IN (SELECT txt
                                                    FROM """ + IValue._meta.db_table + """ 
                                                    GROUP BY txt
                                                    HAVING COUNT(txt) > 1)
                                AND d.valdate IS NULL""")
                # attach the property_id
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """ v
                                SET property_id = r.id
                                FROM    prop_property r
                                JOIN    prop_parcel p
                                        ON r.parcel_id = p.id
                                        AND p.muni_id = """ + str(1) + """
                                WHERE    v.txt = r.ext""")
                # fill in val
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """ SET val = landval + impval""")
                #delete those with no property_id
                IValue.objects.filter(property__isnull=True).delete()
                # set the date
                # TODO: find the year from somewhere
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """ SET valdate = '2016-07-01'""")

            if self.model_name == 'IZone':
                #TODO: insert some tests to ensure that the meta-data is the same across code
                cursor = connection.cursor()
                #delete those with no PID
                cursor.execute("""UPDATE """ + IZone._meta.db_table + """
                                SET    geom = ST_MakeValid(geom)
                                        """)

        if self.muni.name == 'Vancouver':
            if self.model_name == 'IParcel':
                
                #first attempt at djano code for street name repair...
                #dp = ['N', 'E', 'S', 'W', 'NE', 'NW', 'SE', 'SW']
                #Parcel.objects.filter(reduce(operator.or_, (Q(street__startswith=x + ' ') for x in dp))).update()

                # separate the street names from street types etc
                cursor.execute("""UPDATE """ + IParcel._meta.db_table + """
                                SET     street_prefix =  SUBSTRING(street, 1, STRPOS(street, ' ') - 1)
                                    , street = SUBSTRING(street, STRPOS(street, ' ') + 1)
                                WHERE    SUBSTRING(street, 1, STRPOS(street, ' ')) IN ('N ', 'E ', 'S ', 'W ', 'NE ', 'NW ', 'SE ', 'SW ')
                                    """)
                cursor.execute("""UPDATE """ + IParcel._meta.db_table + """
                                SET    street = SUBSTRING(street, 1, CHAR_LENGTH(street) - STRPOS(REVERSE(street), ' '))
                                    , street_suffix =  RIGHT(street, STRPOS(REVERSE(street), ' ') - 1)
                                WHERE    RIGHT(street, STRPOS(REVERSE(street), ' ') - 1) IN ('NORTH', 'SOUTH')
                                    """)
                cursor.execute("""UPDATE """ + IParcel._meta.db_table + """
                                SET    street = SUBSTRING(street, 1, CHAR_LENGTH(street) - STRPOS(REVERSE(street), ' '))
                                    , street_type = RIGHT(street, STRPOS(REVERSE(street), ' ') - 1)
                                WHERE    street LIKE '% %'
                                    AND street NOT LIKE 'THE CASTINGS'
                                    """)
                cursor.execute("""UPDATE """ + IParcel._meta.db_table + """
                                SET    street_number = CAST(txt3 AS integer)
                                WHERE    txt3 ~ '^[0-9]'
                                """)

                # null data
                cursor.execute("""UPDATE """ + IParcel._meta.db_table + """
                                SET    street = NULLIF(street, '')
                                        , street_prefix = NULLIF(street_prefix, '')
                                        , street_suffix = NULLIF(street_suffix, '')
                                        , street_type = NULLIF(street_type, '')
                                        , unit = NULLIF(unit, '')
                                        , postal = NULLIF(postal, '')
                                        , txt = NULLIF(txt, '')
                                        , txt2 = NULLIF(txt2, '')
                                        , txt3 = NULLIF(txt3, '')
                                        , street_number = NULLIF(street_number, 0)
                                        , geom = ST_MakeValid(geom)
                                        """)
                
                IParcel.objects.filter(txt__isnull=True).delete()
                
                # insert data to lot
                ILot.objects.all().delete()
                cursor.execute("""INSERT INTO """ + ILot._meta.db_table + """ (grp, txt)
                                SELECT    txt2
                                        , txt
                                FROM    impo_iparcel
                                        """)
                
                # update parcel_id where available
                cursor.execute("""UPDATE    impo_iparcel
                        SET    parcel_id = p.id
                        FROM    prop_parcel p
                        JOIN    impo_iparcel ip
                                ON ip.txt = p.ext
                                AND p.depdate IS NULL
                        """)

            if self.model_name == 'ILot':
                cursor = connection.cursor()
                # populate the internally generated Parcel ids
                cursor = connection.cursor()
                cursor.execute("""UPDATE """ + ILot._meta.db_table + """ t
                                SET     parcel_id = p1.id
                                FROM     prop_parcel p1
                                WHERE    t.txt = p1.ext""")
                # populate the internally generated Lot ids
                cursor.execute("""UPDATE """ + ILot._meta.db_table + """ t
                                SET     parcel_id = p1.id
                                FROM     prop_lot p1
                                WHERE    t.grp = p1.ext""")
        
        

            if self.model_name == 'IProperty':
                cursor = connection.cursor()
                # separate the street names from street types etc
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """
                                SET     street_prefix =  RIGHT(street, STRPOS(REVERSE(street), ' ')-1)
                                    , street =  LEFT(street, CHAR_LENGTH(street)-STRPOS(REVERSE(street), ' '))
                                WHERE    RIGHT(street, STRPOS(REVERSE(street), ' ')-1) IN ('N', 'E', 'S', 'W', 'NE', 'NW', 'SE', 'SW')
                                    """)
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """
                                SET    street = SUBSTRING(street, 1, CHAR_LENGTH(street) - STRPOS(REVERSE(street), ' '))
                                    , street_suffix =  RIGHT(street, STRPOS(REVERSE(street), ' ') - 1)
                                WHERE    RIGHT(street, STRPOS(REVERSE(street), ' ') - 1) IN ('NORTH', 'SOUTH')
                                    """)
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """
                                SET    street = SUBSTRING(street, 1, CHAR_LENGTH(street) - STRPOS(REVERSE(street), ' '))
                                    , street_type = RIGHT(street, STRPOS(REVERSE(street), ' ') - 1)
                                WHERE    street LIKE '% %'
                                    AND street NOT LIKE 'THE CASTINGS'
                                    """)

                # Delete duplicate PIDs
                cursor.execute("""DELETE FROM """ + IProperty._meta.db_table + """ p
                                USING impo_iproperty a
                                WHERE p.txt = a.txt
                                    AND p.id < a.id""")
                
                #bind values to parcels based on txt2
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """ r
                                SET parcel_id = p.id
                                FROM    prop_parcel p
                                WHERE    p.ext2 = r.txt2""")
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """
                                SET    street = NULLIF(street, '')
                                        , street_prefix = NULLIF(street_prefix, '')
                                        , street_suffix = NULLIF(street_suffix, '')
                                        , street_type = NULLIF(street_type, '')
                                        , unit = NULLIF(unit, '')
                                        , postal = NULLIF(postal, '')""")
                # Delete NULL PIDs
                
                IProperty.objects.filter(txt__isnull=True).delete()
                # TODO: fill in missing address bits for parcels and properties
                
            if self.model_name == 'IValue':
                cursor = connection.cursor()
                #delete those with no PID
                
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """
                                SET    valdate = NULLIF(valdate, '')
                                        , txt = NULLIF(txt, '')
                                        """)
                IValue.objects.filter(txt__isnull=True).delete()
                
                
                # aggregate properties with multiple assessment rolls
                cursor.execute("""INSERT INTO """ + IValue._meta.db_table + """ (landval, impval, txt, valdate)
                                SELECT      SUM(landval)
                                            , SUM(impval)
                                            , txt
                                            , 'Agg'
                                FROM        """ + IValue._meta.db_table + """ 
                                GROUP BY    txt 
                                HAVING     COUNT(txt) > 1""")    
                cursor.execute("""DELETE FROM """ + IValue._meta.db_table + """ d
                                WHERE    d.txt IN (SELECT txt
                                                    FROM """ + IValue._meta.db_table + """ 
                                                    GROUP BY txt
                                                    HAVING COUNT(txt) > 1)
                                AND d.valdate IS NULL""")
                # attach the property_id
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """ v
                                SET property_id = r.id
                                FROM    prop_property r
                                JOIN    prop_parcel p
                                        ON r.parcel_id = p.id
                                        AND p.muni_id = """ + str(2) + """
                                WHERE    v.txt = r.ext""")
                # fill in val
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """ SET val = landval + impval""")
                #delete those with no property_id
                IValue.objects.filter(property__isnull=True).delete()
                # set the date
                # TODO: find the year from somewhere
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """ SET valdate = '2016-07-01'""")
            
            if self.model_name == 'IZone':
                #TODO: insert some tests to ensure that the meta-data is the same across code
                cursor = connection.cursor()
                #delete those with no PID
                cursor.execute("""UPDATE """ + IZone._meta.db_table + """
                                SET    geom = ST_MakeValid(geom)
                                        """)
            
        if self.muni.name == 'Surrey':
            if self.model_name == 'IParcel':
                cursor = connection.cursor()
                # separate the street names from street types
                cursor.execute("UPDATE " + tablename + " SET street_type = RIGHT(street, STRPOS(REVERSE(street), ' ') - 1)")
                cursor.execute("UPDATE " + tablename + " SET street = SUBSTRING(street, 1, LENGTH(street) - STRPOS(REVERSE(street), ' '))")
                # clean data
                cursor.execute("""UPDATE """ + IParcel._meta.db_table + """
                                SET    street = NULLIF(street, '')
                                        , street_prefix = NULLIF(street_prefix, '')
                                        , street_suffix = NULLIF(street_suffix, '')
                                        , street_type = NULLIF(street_type, '')
                                        , unit = NULLIF(unit, '')
                                        , postal = NULLIF(postal, '')
                                        , txt = NULLIF(txt, '')
                                        , txt2 = NULLIF(txt2, '')
                                        , txt3 = NULLIF(txt3, '')
                                        , street_number = NULLIF(street_number, 0)
                                        , geom = ST_MakeValid(geom)
                                        """)
                # move the objectid from num to txt
                cursor.execute("""UPDATE """ + IParcel._meta.db_table + """
                                SET    txt = num""")
                
                # insert data to lot
                ILot.objects.all().delete()
                cursor.execute("""INSERT INTO """ + ILot._meta.db_table + """ (grp, txt)
                                SELECT    a.grp
                                        , p.txt
                                FROM    (SELECT    CAST(MIN(CAST(txt AS bigint)) + COUNT(txt)*100000000000000 AS character varying) as grp, street, street_number, street_type
                                        FROM    impo_iparcel
                                        WHERE    street IS NOT NULL
                                        GROUP BY street, street_number, street_type) a
                                JOIN    impo_iparcel p
                                        ON a.street = p.street
                                        AND a.street_number = p.street_number
                                        AND a.street_type = p.street_type
                                    """)
                
                # Delete duplicate txt
                cursor.execute("""DELETE FROM """ + IParcel._meta.db_table + """ p
                                USING """ + IParcel._meta.db_table + """ a
                                WHERE p.txt = a.txt
                                    AND p.id < a.id""")
                
                # update parcel_id where available
                cursor.execute("""UPDATE impo_iparcel ip
                                SET    parcel_id = p.id
                                FROM    prop_parcel p
                                WHERE ip.txt = p.ext
                                    AND p.muni_id = """ + self.muni_id + """
                                    AND p.depdate IS NULL
                        """)
                
                # insert data to lot
                ILot.objects.all().delete()
                cursor.execute("""INSERT INTO """ + ILot._meta.db_table + """ (grp, txt)
                                SELECT    txt
                                        , txt
                                FROM    impo_iparcel
                                        """)

            if self.model_name == 'IAddress':
                cursor = connection.cursor()
                cursor.execute("""UPDATE """ + IAddress._meta.db_table + """ 
                                SET street_type = UPPER(street_type)
                                    , street = UPPER(street)""")
                
                
                
                #Fill in the address data in the IParcel table                    
                cursor.execute("""UPDATE impo_iparcel p
                                SET unit = NULLIF(i.unit, '')
                                    , street_number = i.street_number
                                    , street_prefix = NULLIF(i.street_prefix, '')
                                    , street = NULLIF(i.street, '')
                                    , street_type = NULLIF(i.street_type, '')
                                    , street_suffix = NULLIF(i.street_suffix, '')
                                    , postal = NULLIF(i.postal, '')
                                    , txt2 = i.txt
                                FROM    """ + IAddress._meta.db_table + """ i
                                WHERE    ST_Intersects(i.geom, p.geom)""")
                                    
                
            
            if self.model_name == 'ILot':
                cursor = connection.cursor()
                
                #the only parcels that need aggregating those that are strata properties
                
                
                #Delete non-strata
                cursor.execute("""DELETE FROM """ + ILot._meta.db_table + """ 
                                WHERE NOT txt = 'Strata'""")
                 
                #Delete stratas that only contain one parcel
                cursor.execute("""DELETE FROM """ + ILot._meta.db_table + """ i
                                USING     (SELECT    l.grp, COUNT(p.id) as co
                                        FROM    impo_ilot l
                                        JOIN    prop_parcel p
                                            ON ST_Contains(l.geom, p.geom)
                                        GROUP BY l.grp) g
                                WHERE    g.grp = i.grp
                                        AND g.co = 1""")
                
                #insert aggregate lots
                cursor.execute("""INSERT INTO """ + ILot._meta.db_table + """ (grp, txt, parcel_id, lot_id)
                                SELECT    i.grp
                                        , p.ext
                                        , p.id
                                        , l.id
                                FROM    """ + ILot._meta.db_table + """ i
                                JOIN    prop_parcel p
                                        ON ST_Contains(i.geom, p.geom)
                                LEFT JOIN prop_lot l
                                        ON l.ext = i.grp""")
                
                #insert single lots
                cursor.execute("""INSERT INTO """ + ILot._meta.db_table + """ (grp, txt, parcel_id, lot_id)
                                SELECT    p.ext AS grp
                                    , p.ext AS txt
                                    , p.id AS parcel_id
                                    , l.id AS lot_id
                                FROM    prop_parcel p
                                LEFT JOIN impo_ilot i
                                    ON p.ext = i.txt
                                LEFT JOIN    prop_lot l
                                    ON l.ext = p.ext
                                WHERE i.id IS NULL
                                    AND p.muni_id = 3""" + str(self.muni.id))
                
                ILot.objects.filter(txt='Strata').delete()
                
                # populate the internally generated Parcel ids
                cursor = connection.cursor()
                cursor.execute("""UPDATE """ + ILot._meta.db_table + """ t
                                SET     parcel_id = p1.id
                                FROM     prop_parcel p1
                                WHERE    t.txt = p1.ext
                                        AND p1.muni_id = """ + str(self.muni.id))
                # populate the internally generated Lot ids
                cursor.execute("""UPDATE """ + ILot._meta.db_table + """ t
                                SET     parcel_id = p1.id
                                FROM     prop_lot p1
                                WHERE    t.grp = p1.ext
                                        AND p1.muni_id = """ + str(self.muni.id))
        
        
                                
            if self.model_name == 'IProperty':
                
                cursor = connection.cursor()
                
                IProperty.objects.filter(txt3__in=['City Road', 'Dedicated Road']).delete()
                
                #bind records to parcels based on txt2 
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """ r
                                SET parcel_id = p.id
                                FROM    prop_parcel p
                                WHERE    RIGHT(p.ext, 10) = REPLACE(r.txt2, '-', '')
                                        AND p.muni_id = """ + str(self.muni.id))
                
                #bind records to parcels based on num where txt3 is  Strata
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """ r
                                SET parcel_id = p.id
                                FROM    prop_parcel p
                                WHERE    p.ext2 = CAST(r.num AS character varying)
                                        AND r.txt3 = 'Standard Strata'
                                        AND p.muni_id = """ + str(self.muni.id))
                
                #bind records to parcels based on txt2 parcel_id is still null
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """ r
                                SET parcel_id = p.id
                                FROM    prop_parcel p
                                WHERE    p.ext2 = CAST(r.num AS character varying)
                                        AND r.parcel_id IS NULL
                                        AND p.muni_id = 3""") + str(self.muni.id)
                
                
                
                cursor.execute("""UPDATE """ + IProperty._meta.db_table + """
                                SET    street = NULLIF(street, '')
                                        , street_prefix = NULLIF(street_prefix, '')
                                        , street_suffix = NULLIF(street_suffix, '')
                                        , street_type = NULLIF(street_type, '')
                                        , unit = NULLIF(unit, '')
                                        , postal = NULLIF(postal, '')""")
                
                # Delete where parcel_id IS NULL
                IProperty.objects.filter(parcel__isnull=True).delete()

                # Delete NULL PIDs
                IProperty.objects.filter(txt__isnull=True).delete()
                # Delete duplicate PIDs
                cursor.execute("""DELETE FROM """ + IProperty._meta.db_table + """ p
                                USING impo_iproperty a
                                WHERE p.txt = a.txt
                                    AND p.id < a.id""")

                # TODO: fill in missing address bits for parcels and properties
                
            if self.model_name == 'IValue':
                cursor = connection.cursor()
                #delete those with no PID
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """
                                SET    valdate = NULLIF(valdate, '')
                                        , txt = NULLIF(txt, '')
                                        , txt2 = NULLIF(txt2, '')
                                        """)
                IValue.objects.filter(txt__isnull=True).delete()
                
                # Delete duplicate Folios
                cursor.execute("""DELETE FROM """ + IValue._meta.db_table + """ p
                                USING """ + IValue._meta.db_table + """ a
                                WHERE p.txt2 = a.txt2
                                    AND p.id < a.id""")
                
                # aggregate properties with multiple assessment rolls
                cursor.execute("""INSERT INTO """ + IValue._meta.db_table + """ (landval, impval, txt, valdate)
                                SELECT      SUM(landval)
                                            , SUM(impval)
                                            , txt
                                            , 'Agg'
                                FROM        """ + IValue._meta.db_table + """ 
                                GROUP BY    txt 
                                HAVING     COUNT(txt) > 1""")    
                cursor.execute("""DELETE FROM """ + IValue._meta.db_table + """ d
                                WHERE    d.txt IN (SELECT txt
                                                    FROM """ + IValue._meta.db_table + """ 
                                                    GROUP BY txt
                                                    HAVING COUNT(txt) > 1)
                                AND d.valdate IS NULL""")
                # attach the property_id
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """ v
                                SET property_id = r.id
                                FROM    prop_property r
                                JOIN    prop_parcel p
                                        ON r.parcel_id = p.id
                                        AND p.muni_id = """ + str(self.muni.id) + """
                                WHERE    v.txt = r.ext""")
                # fill in val
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """ SET val = landval + impval""")
                #delete those with no property_id
                IValue.objects.filter(property__isnull=True).delete()
                # set the date
                # TODO: find the year from somewhere
                cursor.execute("""UPDATE """ + IValue._meta.db_table + """ SET valdate = '2016-07-01'""")

            if self.model_name == 'IZone':
                #TODO: insert some tests to ensure that the meta-data is the same across code
                cursor = connection.cursor()
                
                #make geometries valid
                cursor.execute("""UPDATE """ + IZone._meta.db_table + """
                                SET    geom = ST_MakeValid(geom)
                                        """)
                
                #clean data
                cursor.execute("""UPDATE """ + IZone._meta.db_table + """
                                SET    code = 'RM-30'
                                WHERE    code = 'RM30'
                                """)
                
                #fix screwed up urls
                cursor.execute("""UPDATE """ + IZone._meta.db_table + """
                                SET    url = LEFT(url, LENGTH(url) - STRPOS(REVERSE(url), '=') + 1) || REPLACE(code, '-', '')
                                """)
                
                
                
                #alter CD zone codes
                cursor.execute("""UPDATE """ + IZone._meta.db_table + """
                                SET    code = code || ' (' || REPLACE(txt, 'B/L ', '') || ')'
                                WHERE    code = 'CD'
                                """)
                
                
                

class Source_Link(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, db_index=True)
    source_col = models.CharField(max_length=50)
    model_col = models.CharField(max_length=50)
    
class IParcel(models.Model):
    # Temporarily holds IParcel objects prior to import
    parcel = models.ForeignKey('prop.Parcel', null=True, db_index=True, on_delete=models.SET_NULL)
    txt = models.CharField(max_length=50, null=True, db_index=True)
    txt2 = models.CharField(max_length=50, null=True, db_index=True)
    txt3 = models.CharField(max_length=50, null=True, db_index=True)
    num = models.BigIntegerField(null=True, db_index=True)
    num2 = models.DecimalField(null=True, max_digits=20, decimal_places=10, db_index=True) 
    num3 = models.DecimalField(null=True, max_digits=20, decimal_places=10, db_index=True) 
    unit = models.CharField(max_length=20, null=True)
    street_number = models.IntegerField(null=True)
    street_prefix = models.CharField(max_length=20, null=True)
    street = models.CharField(max_length=50, null=True)
    street_type = models.CharField(max_length=20, null=True)
    street_suffix = models.CharField(max_length=20, null=True)
    postal = models.CharField(max_length=20, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    
class ILot(models.Model):
    # Temporarily holds tie objects ==> linked parcels
    parcel = models.ForeignKey('prop.Parcel', null=True, db_index=True, on_delete=models.SET_NULL)
    lot = models.ForeignKey('prop.Lot', null=True, db_index=True, on_delete=models.SET_NULL)
    grp = models.CharField(max_length=50, null=True, db_index=True) #external (or internally generated) identifier for grouping
    txt = models.CharField(max_length=50, null=True, db_index=True) #identifier for parcel
    geom = models.MultiPolygonField(srid=4326, null=True)
    
class IAddress(models.Model):
    # Temporarily holds address objects prior to import
    parcel = models.ForeignKey('prop.Parcel', null=True, db_index=True, on_delete=models.SET_NULL)
    txt = models.CharField(max_length=50, null=True, db_index=True) #external identifier
    num = models.BigIntegerField(null=True) #external identifier
    unit = models.CharField(max_length=20, null=True)
    street_number = models.IntegerField(null=True)
    street_prefix = models.CharField(max_length=20, null=True)
    street = models.CharField(max_length=50, null=True)
    street_type = models.CharField(max_length=20, null=True)
    street_suffix = models.CharField(max_length=20, null=True)
    postal = models.CharField(max_length=20, null=True)
    geom = models.PointField(srid=4326, null=True)  

class IProperty(models.Model):
    # Temporarily holds property objects prior to import
    parcel = models.ForeignKey('prop.Parcel', null=True, db_index=True, on_delete=models.SET_NULL)
    txt = models.CharField(max_length=50, null=True, db_index=True) 
    txt2 = models.CharField(max_length=50, null=True, db_index=True) 
    txt3 = models.CharField(max_length=50, null=True, db_index=True) 
    num = models.BigIntegerField(null=True)
    num2 = models.DecimalField(null=True, max_digits=20, decimal_places=10) 
    num3 = models.DecimalField(null=True, max_digits=20, decimal_places=10) 
    unit = models.CharField(max_length=20, null=True)
    street_number = models.IntegerField(null=True)
    street_prefix = models.CharField(max_length=20, null=True)
    street = models.CharField(max_length=50, null=True)
    street_type = models.CharField(max_length=20, null=True)
    street_suffix = models.CharField(max_length=20, null=True)
    postal = models.CharField(max_length=20, null=True)
    geom = models.PointField(srid=4326, null=True) #some municipalities only provide a geographic link to parcels
    
class IValue(models.Model):
    property = models.ForeignKey('prop.Property', null=True, db_index=True, on_delete=models.SET_NULL)
    valdate = models.CharField(max_length=50, null=True)
    landval = models.BigIntegerField(null=True)
    impval = models.BigIntegerField(null=True)
    val = models.BigIntegerField(null=True)
    txt = models.CharField(max_length=50, null=True, db_index=True) #external identifier
    txt2 = models.CharField(max_length=50, null=True, db_index=True) #external identifier
    num = models.BigIntegerField(null=True) #external identifier
    geom = models.PointField(srid=4326, null=True) #some municipalities only provide a geographic link to parcels
    
class IZone(models.Model):
    code = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=150, null=True)
    url = models.CharField(max_length=250, null=True)
    txt = models.CharField(max_length=50, null=True, db_index=True)
    txt2 = models.CharField(max_length=50, null=True, db_index=True)
    txt3 = models.CharField(max_length=50, null=True, db_index=True)
    txt4 = models.CharField(max_length=50, null=True, db_index=True)
    num = models.BigIntegerField(null=True)
    num2 = models.DecimalField(null=True, max_digits=20, decimal_places=10) 
    num3 = models.DecimalField(null=True, max_digits=20, decimal_places=10) 
    geom = models.MultiPolygonField(srid=4326, null=True)

class IPolicy(models.Model):
    code = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=150, null=True)
    url = models.CharField(max_length=250, null=True)
    txt = models.CharField(max_length=50, null=True, db_index=True)
    txt2 = models.CharField(max_length=50, null=True, db_index=True)
    txt3 = models.CharField(max_length=50, null=True, db_index=True)
    num = models.BigIntegerField(null=True)
    num2 = models.DecimalField(null=True, max_digits=20, decimal_places=10) 
    num3 = models.DecimalField(null=True, max_digits=20, decimal_places=10) 
    geom = models.MultiPolygonField(srid=4326, null=True)
 

