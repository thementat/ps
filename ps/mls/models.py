from django.db import models
from prop.models import Property
from django.dispatch import receiver
from django.db.models.signals import post_save

import imaplib
import email
import datetime
import re
from bs4 import BeautifulSoup
from selenium import webdriver
# Create your models here.


class Source(models.Model):
    code = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=50)
    
class Search(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, db_index=True)
    code = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=150)

class Listing(models.Model):
    source = models.ForeignKey(Source, db_index=True, on_delete=models.CASCADE)
    mlsn = models.CharField(max_length=50, null=True, db_index=True)
    property = models.ForeignKey('prop.Property', null=True, db_index=True, on_delete=models.SET_NULL)
    pid = models.CharField(max_length=50, null=True, db_index=True)
    status = models.CharField(max_length=25, null=True, db_index=True)
    list_price = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    sale_price = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    list_date = models.DateField(null=True)
    sale_date = models.DateField(null=True)
    dom = models.IntegerField(null=True)
    type = models.CharField(max_length=50, null=True)
    lot_size = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    style = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    year = models.IntegerField(null=True)
    construction = models.CharField(max_length=50, null=True)
    legal = models.CharField(max_length=250, null=True)
    sqft = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    sqft_a = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    sqft_m = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    sqft_e = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    sqft_bu = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    sqft_bf = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    sqft_b = models.DecimalField(null=True, max_digits=20, decimal_places=4)
    development_units = models.IntegerField(null=True)
    strata_units = models.IntegerField(null=True)
    
@receiver(post_save, sender=Property)
def update_Listing_Propertychange(sender, update_fields, created, instance, **kwargs):
    if created or update_fields is 'ext':
        
        # find all Listing objects where pid = new ext, and set property = new record
        #TODO: would this be simpler for us to manage at object creation?
        Listing.objects.filter(pid=instance.ext).update(property=instance)
                
class Paragon_Field(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=50, db_index=True)
    location = models.CharField(max_length=150, db_index=True)

class Paragon_Mail(models.Model):
    msg_id = models.IntegerField(null=True)
    sent_date = models.DateTimeField(null=True)
    search = models.ForeignKey(Search, on_delete=models.CASCADE, db_index=True)
    url = models.CharField(max_length=250, null=True)
    complete = models.BooleanField(default=False)
    
    def retrieve(self):
        src = Source.objects.get(code='bcp')
        browser = webdriver.Chrome('/Users/chrisbradley/git/ps/mls/chromedriver')
        browser.get(self.url)
        framesets = browser.find_elements_by_tag_name("frameset")
        frame_list = framesets[1].find_elements_by_tag_name("frame")[0]
        frame_data = framesets[2].find_elements_by_tag_name("frame")[1]
        browser.switch_to.frame(frame_list)
        all_a = browser.find_elements_by_tag_name('a')
        
        # get the field list
        fields = Paragon_Field.objects.filter(search=self.search)
        for index in range(0, len(all_a)):
            if index > 1:
                ftblrow = []
                ae = all_a[index]
                ae.click()
                mlsn = ae.get_attribute("text").strip("ML: ")
                browser.switch_to.default_content()
                browser.switch_to.frame(frame_data)
                
                # gather the data from the page
                # construct a dict for field values
                fvalues = {}
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
                    
                
                try:
                    prop = Property.objects.get(ext=fvalues['pid'])
                except:
                    prop = None
                fvalues['property'] = prop
                # create or update
                Listing.objects.update_or_create(
                    source=src, mlsn=mlsn,
                    defaults=fvalues)
                
                
                browser.switch_to.default_content()
                browser.switch_to.frame(frame_list)
                
        self.complete = True
        self.save()
                
        browser.quit()
        return True
        
    
    @classmethod
    def sync(cls):
        datetime.getdate = datetime.date(2016,8,23)
        M = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            M.login('relabemail@gmail.com', 'relabp@$$')
        except imaplib.IMAP4.error:
            print ('LOGIN FAILED!!! ')
            # ... exit or deal with failure...
        
        # get the mailbox
        rv, data = M.select()
        
        #Delete messages older than 80 days... the links will be stale
        deletebefore = datetime.datetime.today() - datetime.timedelta(days=80)
        typ, [msg_ids] = M.search(None, '(SUBJECT "Real Estate Listing Notification For R.E. Lab" SENTBEFORE ' + deletebefore.strftime('%d-%b-%Y') + ')')
        msg_ids = msg_ids.decode('utf-8')
        if len(msg_ids) != 0:
            msg_ids = ','.join(msg_ids.split())
            typ, response = M.store(msg_ids, '+FLAGS', r'(\Deleted)')
        
        # Get the remaining emails
        rv, msg_ids = M.search(None, '(SUBJECT "Real Estate Listing Notification For R.E. Lab")')
        msg_list = list(map(int, msg_ids[0].decode('utf-8').split()))
        
        # delete email records no longer in the mailbox
        Paragon_Mail.objects.exclude(msg_id__in=msg_list).delete()
        
        # iterate through the mail messages, and create/update Paragon_Mail objects       
        for msgid in msg_list:
            rv, data = M.fetch(str(msgid), '(RFC822)')
            if rv != 'OK':
                print('ERROR getting message ' + msgid)
            msg = email.message_from_bytes(data[0][1])
            soup = BeautifulSoup(msg.get_payload(decode=True), 'html.parser')
            search = Search.objects.get(code=soup.find('p').get_text().replace("\t", "").replace("\r\n", " "))
            url = soup.find('a')['href']
            senton = datetime.datetime.strptime(msg['Date'], '%d %b %Y %H:%M:%S %z')
            #TODO: sort out timezone warning
            Paragon_Mail.objects.update_or_create(
                msg_id=msgid,
                defaults={'sent_date' : senton.strftime('%Y-%m-%d %H:%M:%S.%f'), 'search': search, 'url': url})
            
        M.close()
        M.logout()
        
        
        
