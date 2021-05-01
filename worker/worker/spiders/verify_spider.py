import json

from urllib.parse import urljoin, urlencode
from scrapy import Spider, Request, FormRequest
from scrapy.selector import HtmlXPathSelector


class VerifyScheduleSpider(Spider):
    name = "verify"
    start_urls = ['https://login.utexas.edu/login/UI/Login']
    home_url = 'https://utdirect.utexas.edu/apps/registrar/course_schedule/20179/'
    fields = []
    courses = {}

    def get_url(self, field, level):
        query_params = {"fos_fl": field, "level": level, "ccyys": "20179", "search_type_main": "FIELD"}
        return self.home_url + "results?" + urlencode(query_params)

    def parse(self, response):
        return FormRequest.from_response(
            response,
            formdata={'IDToken1': '', 'IDToken2': ''}, # OMITTED username - password
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in str(response.body):
            self.logger.error("Login failed")
            return
        else:
            return Request(url=self.home_url, callback=self.redirect1)

    def redirect1(self, response):
        return FormRequest.from_response(response, callback=self.redirect2)

    def redirect2(self, response):
        return FormRequest.from_response(response, callback=self.get_fields)

    def get_fields(self, response):
        self.fields = response.xpath('//select[@id="fos_fl"]//option/@value').extract()[1:]
        for field in self.fields[:2]:
            lower_url = self.get_url(field, "L")
            upper_url = self.get_url(field, "U")
            yield Request(url=lower_url, callback=self.get_classes)
            yield Request(url=upper_url, callback=self.get_classes)

    def get_classes(self, response):
        # with open("neat3.html", "wb") as f:
        #     f.write(response.body)
        # print(response.body)

        table_items = response.xpath('//table[@class="rwd-table results"]/tbody/tr')
        current_course = ""
        for item in table_items:

            # Get current course
            new_course_name = item.xpath('.//td[@class="course_header"]/h2/text()').extract_first()
            if new_course_name:
                current_course = new_course_name.strip()
                if current_course not in self.courses:
                    self.courses[current_course] = []
                    print(current_course)
                continue

            # Get times & info for current course
            unique = item.xpath('.//td[@data-th="Unique"]/a/text()').extract_first()
            if unique and unique.isdigit():
                ut_class = {"unique": int(unique), "course": current_course}
                ut_class['instructor'] = item.xpath('.//td[@data-th="Instructor"]/text()').extract_first()
                ut_class['status'] = item.xpath('.//td[@data-th="Status"]/text()').extract_first()

                ut_class['days'] = []
                for day_set in item.xpath('.//td[@data-th="Days"]/span/text()').extract():
                    ut_class['days'].append(day_set)

                ut_class['times'] = []
                for time_set in item.xpath('.//td[@data-th="Hour"]/span/text()').extract():
                    ut_class['times'].append(time_set)

                ut_class['rooms'] = []
                for time_set in item.xpath('.//td[@data-th="Room"]/span/text()').extract():
                    ut_class['rooms'].append(time_set)

                self.courses[current_course].append(ut_class)

        # Recursively get the next page if it exists
        next_page_link = response.xpath('//a[@id="next_nav_link"]/@href').extract_first()
        if next_page_link:
            next_page_link = urljoin(response.url, next_page_link)
            return Request(url=next_page_link, callback=self.get_classes)

    def closed(self, reason):
        with open('data.json', 'w') as f:
            json.dump(self.courses, f)
        # print(self.courses)
