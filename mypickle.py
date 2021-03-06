from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class MyPickleLinks:

    def __init__(self):
        firefox_options = Options()
        firefox_options.headless = True
        self.driver = webdriver.Firefox(executable_path=r'D:\Data Projects\Python Projects\JetBrains\geckodriver',
                                        options=firefox_options)
        self.base_url = 'https://mypickle.org/national-support-results/?wpv_filter_submit=Go&wpv_aux_current_post_id' \
                        '=13821&wpv_view_count=13850-TCPID13821&wpv-relationship-filter-support-category= '
        self.query_url_list = []
        self.link_list = []

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
            query_link = self.base_url + str(v)
            self.query_url_list.append(query_link)
            print(query_link)

        for link in self.query_url_list:
            self.driver.get(link)
            self.driver.implicitly_wait(4)
            links_for_check = self.driver.find_elements_by_class_name('NSlistingarea')

            for check_link in links_for_check:

                try:
                    link_query = check_link.find_element_by_class_name('service-header1').find_element_by_tag_name(
                        'a').get_attribute('href')
                    self.link_list.append(link_query)
                    print(link_query)

                except:
                    print('Error')

        with open('Mypickle Url List.txt', 'w') as fp:
            fp.write('\n'.join(str(item) for item in self.link_list))


if __name__ == '__main__':
    lll = MyPickleLinks()
    lll.url_crawler()
