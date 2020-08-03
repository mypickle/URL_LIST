# packages
import requests
from bs4 import BeautifulSoup
import re
import csv
import json

# scraper class
class MailPhone:
    def fetch(self, url):
        print('\nHTTP Request  to URL : %s' % url, end='')

        # make HTTP GET request
        res = requests.get(url)

        print(' | Status Code: %s' % res.status_code)
        return res

    def parse(self, res):
        # parse content
        content = BeautifulSoup(res.text, 'lxml')

        # if data extraction logic is placed HERE IN THE CODE then we'll extracting emails
        # and phone numbers from the HOME page
        # Otherwise we can try to extract the link to the "Contact page" and try to extract data
        # from there as well

        # data structure
        try:
            email_phone = {
                'email': re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', content.get_text())[0],
                'phone': re.findall('(\d{3,4} \d{3,4} \d{3,4})', content.get_text())[0],

            }

            print('EXTRACT FROM HOME\n\n', json.dumps(email_phone, indent=2))
            self.to_csv(email_phone)
        except:
            email_phone = {
                'url': res.url,
                'email': '',
                'phone': ''
            }

        try:
            # extract contact data page URL
            contact_url = res.url[0:-1] + content.body.find('a', text=re.compile('Contact', re.IGNORECASE))['href']

            # request contact page
            res = self.fetch(contact_url)

            # parse contact HTML
            contact = BeautifulSoup(res.text, 'lxml')
            email = re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', contact.get_text())[0]
            phone = re.findall('(\d{3,4} \d{3,4} \d{3,4})', contact.get_text())[0]

            # if no data available on the home page try to extract it from contact page
            if email_phone['email'] == '' and email_phone['phone'] == '':
                try:
                    email_phone = {
                        'url': res.url,
                        'email': email,
                        'phone': phone
                    }

                except:
                    email_phone = {
                        'url': res.url,
                        'email': '',
                        'phone': ''
                    }

                print('EXTRACT FROM CONTACT\n\n', json.dumps(email_phone, indent=2))
                self.to_csv(email_phone)

        except:
            pass

    def to_csv(self, row):
        # append results to CSV file
        with open('../contacts.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writerow(row)

    def run(self):
        urls = ''
        with open('', 'r') as f:
            for line in f.read():
                urls += line

        urls = list(filter(None, urls.split('\n')))
        print(urls)

        for url in urls:
            res = self.fetch(url)
            self.parse(res)


if __name__ == '__main__':
    scraper = MailPhone()
    scraper.run()




