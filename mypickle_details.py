from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd


class MyPickleDetails:

    def __init__(self):
        firefox_options = Options()
        firefox_options.headless = True
        self.driver = webdriver.Firefox(executable_path=r'D:\Data Projects\Python Projects\JetBrains\geckodriver',
                                        options=firefox_options)
        self.base_url = 'https://mypickle.org/national-support-results/?wpv_filter_submit=Go&wpv_aux_current_post_id' \
                        '=13821&wpv_view_count=13850-TCPID13821&wpv-relationship-filter-support-category= '
        
        self.query_url_list = []
        self.link_list = []
        self.details = []
        
    def url_crawler(self):
        
        category_id = {'crime': 11871,
                       'Health and care': 11378,
                       'Housing': 11381,
                       'Money and benefits': 11385,
                       'Pets and animals': 11386,
                       'Relationships and family': 11382,
                       'Something else': 11388,
                       'Wellbeing and happiness': 11383,
                       'Work and study': 11384,
                       'Your rights': 11387}

        for k, v in category_id.items():
            self.query_link = self.base_url + str(v)
            self.query_url_list.append(self.query_link)
            print(self.query_link)

        for link in self.query_url_list:
            self.driver.get(link)
            self.driver.implicitly_wait(4)
            links_for_check = self.driver.find_elements_by_class_name('NSlistingarea')

            for check_link in links_for_check:

                link_query = ''
                service_header = ''
                provider_details = ''
                service_description = ''
                contact = ''

                all_titles = {}

                try:
                    link_query = check_link.find_element_by_class_name('service-header1').find_element_by_tag_name(
                        'a').get_attribute('href')
                    all_titles['link_query'] = link_query
                    print(link_query)

                except:
                    print('Error link_query')
                    pass

                try:
                    provider_details = check_link.find_element_by_class_name('provider-details').text
                    all_titles['provider_details'] = provider_details
                    print(provider_details)

                except:
                    print('Error provider_details')
                    pass

                try:
                    service_description = check_link.find_element_by_class_name('service-description').text
                    all_titles['service_description'] = service_description
                    print(service_description)

                except:
                    print('Error service_description')
                    pass

                try:
                    contact = check_link.find_element_by_class_name('contact').text
                    all_titles['contact'] = contact
                    print(contact)

                except:
                    print('Error contact')
                    pass

                self.details.append(all_titles)

    def details_file(self):

        df_details = pd.DataFrame(self.details)
        df_details.to_csv('Mypickle Details.csv')
        print(df_details)


if __name__ == '__main__':
    lll = MyPickleDetails()
    lll.url_crawler()
    lll.details_file()
