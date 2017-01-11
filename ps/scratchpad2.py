
import os
import urllib
import base64
import json
import sys
import argparse
import requests

api_url = "https://%s.cartodb.com/api/v2/sql" % "thementat"
import_url = "https://%s.cartodb.com/api/v1/imports/?api_key=%s" % ("thementat", "60dcbd897ae780f97db5090a7160f9a2d7c3222d")
new_tables = []
internal_columns = internal_columns = ['created_at', 'updated_at', 'the_geom', 'the_geom_webmercator', 'cartodb_id']
type_map = {'string':'text', 'boolean': 'boolean', 'date': 'timestamp', 'number':'numeric'}

file = open('/Users/chrisbradley/output.json')
r = requests.post(import_url, files={'file': file})
data = json.load(file)

return requests.get(import_url).json()

complete = False
last_state = ''
while not complete: 
    import_status_url = "https://%s.cartodb.com/api/v1/imports/%s?api_key=%s" % ('thementat', data['item_queue_id'], "60dcbd897ae780f97db5090a7160f9a2d7c3222d")
    response = requests.get(import_status_url)
    d = response.json()
    if last_state!=d['state']:
        last_state=d['state']
        if d['state']=='uploading':
            self._log('Uploading file...')
        elif d['state']=='importing':
            self._log('Importing data...')
        elif d['state']=='complete':
            complete = True
            self._log('Table "%s" created' % d['table_name'])
    if d['state']=='failure':
        self._error(d['get_error_text']['what_about'])    
self.new_tables.append(d['table_name'])
return d['table_name']


class CartoDB:
    def __init__(self, options):
        # do stuff
        self.options = options
        self.api_url = "https://%s.carto.com/api/v2/sql" % (self.options['u'])
        self.import_url = "https://%s.carto.com/api/v1/imports/?api_key=%s" % (self.options['u'], self.options['k'])
        self.new_tables = []
        self.internal_columns = ['created_at', 'updated_at', 'the_geom', 'the_geom_webmercator', 'cartodb_id']
        self.type_map = {'string':'text', 'boolean': 'boolean', 'date': 'timestamp', 'number':'numeric'}
    def _log(self, message):
        if self.options['verbose'] == True:
            print(message)
    def _error(self, error):
        print(error)
        sys.exit()
    def sql_api(self, sql):
        # execute sql request over API
        params = {
            'api_key' : self.options["k"],
            'q'       : sql
        }
        r = requests.get(self.api_url, params=params)
        return r.json()
    def upload(self):
        # import a file
        # see https://gist.github.com/lbosque/5876697
        # returns new table name
        r = requests.post(self.import_url, files={'file': open(self.options['f'], 'rb')})
        data = r.json()
        if data['success']!=True:
            self._error("Upload failed")
        complete = False
        last_state = ''
        while not complete: 
            import_status_url = "https://%s.carto.com/api/v1/imports/%s?api_key=%s" % (self.options['u'], data['item_queue_id'], self.options['k'])
            response = requests.get(import_status_url)
            d = response.json()
            if last_state!=d['state']:
                last_state=d['state']
                if d['state']=='uploading':
                    self._log('Uploading file...')
                elif d['state']=='importing':
                    self._log('Importing data...')
                elif d['state']=='complete':
                    complete = True
                    self._log('Table "%s" created' % d['table_name'])
            if d['state']=='failure':
                self._error(d['get_error_text']['what_about'])    
        self.new_tables.append(d['table_name'])
        return d['table_name']
 
    def columns(self, table):
        sql = "SELECT * FROM %s LIMIT 0" % table 
        data = self.sql_api(sql)
        return data['fields']
 
    def add_column(self, table, name, coltype):
        sql = "ALTER TABLE %s ADD COLUMN %s %s" % (table, name, coltype)
        data = self.sql_api(sql)
        return True
 
    def overwrite(self, append=False):
        # upload new data
        new_table = self.upload()
        source_columns = self.columns(new_table)
        target_columns = self.columns(self.options['t'])
        insert_cols = {}
        alter_cols = []
        for c in source_columns.keys():
            if c in self.internal_columns:
                source_columns.pop(c, None)
            else:
                if c not in target_columns.keys():
                    insert_cols[c] = self.type_map[source_columns[c]['type']]
                    alter_cols.append(c)
                else: 
                    insert_cols[c] = self.type_map[target_columns[c]['type']]
        for c in alter_cols:
            self.add_column(self.options['t'], c, insert_cols[c])
        select_list = []
        for c,t in insert_cols.items():
            select_list.append( "%s::%s" % (c,t))
        sql = "INSERT INTO %s (the_geom, %s) " % (self.options['t'], ','.join(insert_cols.keys()))
        sql += "SELECT the_geom, %s FROM %s; " % (','.join(select_list), new_table)
        sql += "DROP TABLE %s" % new_table
        self._log("Writing data to %s and droppping %s" % (self.options['t'],new_table))
        if append==False:
            sql = "DELETE FROM %s; %s " % (self.options['t'], sql)
        data = self.sql_api(sql)
        if 'error' in data.keys():
            self._log('Overwrite failed, cleaning-up')
            sql = "DROP TABLE %s" % new_table
            self.sql_api(sql)
            return False
        else:
            return True
 
    def drop_table(self):
        # drop a table '
        self._log("Dropping table %s"  % self.options['t'])
        sql = "DROP TABLE %s" % self.options['t']
        data = self.sql_api(sql)
        if 'error' in data.keys():
            self._error(data['error'])
        return True
    
    def clear_rows(self):
        # clear all rows from a table
        self._log("Deleting all rows")
        sql = "DELETE FROM %s" % self.options['t']
        data = self.sql_api(sql)
        if 'error' in data.keys():
            self._error(data['error'])
        return True
 
    def export_table(self):
        self._log("Exporting new %s" % self.options['m'])
        params = {"format": self.options['m'], "api_key": self.options["k"],"q": "SELECT * FROM %s" % self.options["t"]}
        r = requests.get(self.api_url, params=params, stream=True)
        with open(self.options['l'], 'wb') as fd:
            for chunk in r.iter_content(10):
                fd.write(chunk)
        return True
    def clean_table(self):
        # clean up table for speed
        self._log("Cleaning up unused space")
        sql = "VACUUM FULL %s" % self.options['t']
        data = self.sql_api(sql)
        if 'error' in data.keys():
            self._error(data['error'])
        self._log("Optimizing existing indexes")
        sql = "ANALYZE %s" % self.options['t']
        data = self.sql_api(sql)
        if 'error' in data.keys():
            self._error(data['error'])
        return True