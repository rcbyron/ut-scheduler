import json
import atexit
import logging
import pymysql.cursors

from urllib.parse import urljoin, urlencode, urlparse, parse_qs
from scrapy import Spider, Request, FormRequest
from datetime import datetime as dt

log_file = 'classes_crawler.log'
log_level = logging.DEBUG
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

ut_eid = '' # OMITTED
ut_pass = '' # OMITTED

mysql_config = {
    'user': 'conzor',
    'password': '', # OMITTED
    'host': 'scheduler-db-instance-cluster.cluster-ccte9d66nm8j.us-west-1.rds.amazonaws.com',
    'database': 'schedulerdb',
    # 'user': os.environ['RDS_USERNAME'],
    # 'password': os.environ['RDS_PASSWORD'],
    # 'host': os.environ['RDS_HOSTNAME'],
    # 'db': os.environ['RDS_DB_NAME'],
    'port': 3306,
    'cursorclass': pymysql.cursors.DictCursor,
}
cnx = pymysql.connect(**mysql_config)
atexit.register(cnx.close)

# Intialize logging
logger = logging.getLogger('ut_api')
logger.setLevel(log_level)
formatter = logging.Formatter(log_format)
fh = logging.FileHandler(log_file)
ch = logging.StreamHandler()
fh.setLevel(logging.DEBUG)
ch.setLevel(logging.ERROR)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


class ClassesSpider(Spider):
    """Dis spider crawls the UT course schedule for courses & classes."""
    name = "classes"
    start_urls = ['https://login.utexas.edu/login/UI/Login']
    home_url = 'https://utdirect.utexas.edu/apps/registrar/course_schedule/20182/'
    fields = []
    courses = []
    classes = []
    course_id = 0

    def get_course_query_url(self, field, level, open_only=True, web_only=False):
        """Gets the url for the desired courses (e.g. field=ACC, level=U)

        level can be "U" upper division or "L" lower division.
        """
        query_params = {"fos_fl": field,
                        "level": level,
                        "ccyys": "20179",
                        "search_type_main": "FIELD"}

        if open_only:   query_params["open"] = "Y"
        if web_only:    query_params["web"] = "Y"

        return self.home_url + "results?" + urlencode(query_params)

    def parse(self, response):
        """Generate login form request."""
        return FormRequest.from_response(
            response,
            formdata={'IDToken1': ut_eid, 'IDToken2': ut_pass},
            callback=self.after_login
        )

    def after_login(self, response):
        """Check login succeed before continuing."""
        if "authentication failed" in str(response.body):
            logging.error("Login failed.")
            return

        return Request(url=self.home_url, callback=self.redirect1)

    def redirect1(self, response):
        """Follow form redirect."""
        return FormRequest.from_response(response, callback=self.redirect2)

    def redirect2(self, response):
        """Follow another form redirect."""
        return FormRequest.from_response(response, callback=self.get_fields)

    def get_fields(self, response):
        """Yield pages for all fields (upper & lower division)."""
        self.fields = response.xpath('//select[@id="fos_fl"]//option/@value').extract()[1:]
        for field in self.fields:
            lower_url = self.get_course_query_url(field, "L")
            upper_url = self.get_course_query_url(field, "U")
            yield Request(url=lower_url, callback=self.get_classes_for_field)
            yield Request(url=upper_url, callback=self.get_classes_for_field)


    def get_classes_for_field(self, response):
        """Build UT Classes from the yielded 'field' pages."""
        table_items = response.xpath('//table[@class="rwd-table results"]/tbody/tr')
        current_course = {'id': ClassesSpider.course_id}
        for item in table_items:
            # Get current course
            new_course_name = item.xpath('.//td[@class="course_header"]/h2/text()').extract_first()
            if new_course_name:
                current_course = self.get_new_course(new_course_name.strip().replace("  ", " "))

                if current_course['name'] in self.courses:
                    logging.warning("Duplicate adding of " + current_course['name'])

                self.courses.append(current_course)
                continue

            # Get times & info for current course
            self.build_class(item, current_course)

        # Recursively get the next page if it exists
        next_page_link = response.xpath('//a[@id="next_nav_link"]/@href').extract_first()
        if next_page_link:
            next_page_link = urljoin(response.url, next_page_link)
            return Request(url=next_page_link, callback=self.get_classes_for_field)

    @staticmethod
    def get_new_class(unique, course):
        print(course['name'] + " (" + unique + ")")
        ut_class = {"unique": int(unique), "course_id": course['id'],
                    'days1': None, 'start_time1': None, 'end_time1': None, 'room1': None,
                    'days2': None, 'start_time2': None, 'end_time2': None, 'room2': None, 'flags': None}

        return ut_class

    @staticmethod
    def get_new_course(name, desc=""):
        ClassesSpider.course_id += 1
        course = {'id': ClassesSpider.course_id, 'name': name, 'field': name[:3], 'description': desc, 'online': False, 'hours': 0}

        if name[-3:].lower() == "-wb":
            course['online'] = True

        if name[4].isdigit():
            course['hours'] = int(name[5])

        return course

    def parse_times(self, ut_class, item):
        time_rows = item.xpath('.//td[@data-th="Hour"]/span/text()').extract()
        if len(time_rows) > 0:
            times = time_rows[0].replace(' ', '').split('-')
            time_24_0 = dt.strptime(times[0].replace('.', '').upper(), "%I:%M%p")
            time_24_1 = dt.strptime(times[1].replace('.', '').upper(), "%I:%M%p")
            ut_class['start_time1'] = dt.strftime(time_24_0, "%H:%M")
            ut_class['end_time1'] = dt.strftime(time_24_1, "%H:%M")
        if len(time_rows) > 1:
            times = time_rows[1].replace(' ', '').split('-')
            time_24_0 = dt.strptime(times[0].replace('.', '').upper(), "%I:%M%p")
            time_24_1 = dt.strptime(times[1].replace('.', '').upper(), "%I:%M%p")
            ut_class['start_time2'] = dt.strftime(time_24_0, "%H:%M")
            ut_class['end_time2'] = dt.strftime(time_24_1, "%H:%M")

    def build_class(self, item, course):
        """Build a UT Class given the item HTML and current course."""
        unique = item.xpath('.//td[@data-th="Unique"]/a/text()').extract_first()
        if unique and unique.isdigit():
            ut_class = self.get_new_class(unique, course)

            ut_class['instructor'] = item.xpath('.//td[@data-th="Instructor"]/text()').extract_first()
            ut_class['status'] = item.xpath('.//td[@data-th="Status"]/text()').extract_first()

            days = item.xpath('.//td[@data-th="Days"]/span/text()').extract()
            if len(days) > 0:
                ut_class['days1'] = days[0]
            if len(days) > 1:
                ut_class['days2'] = days[1]

            self.parse_times(ut_class, item)

            rooms = item.xpath('.//td[@data-th="Room"]/span/text()').extract()
            if len(rooms) > 0:
                ut_class['room1'] = rooms[0]
            if len(rooms) > 1:
                ut_class['room2'] = rooms[1]

            flags = item.xpath('.//td[@data-th="Flags"]//li/@class').extract()
            ut_class['flags'] = ','.join(filter(None, flags))

            self.classes.append(ut_class)


    def closed(self, reason):
        """Save class data once scraped."""

        # Save to local data.json file
        logging.info("Writing changes to data.json...")
        with open('data.json', 'w') as f:
            json.dump(self.courses, f)
        logging.info("Complete!")

        # Save to MySQL
        logging.info("Writing changes to MySQL...")
        with cnx.cursor() as cursor:

            count = 0

            for course in self.courses:
                sql = "REPLACE INTO `courses` (`id`, `name`, `field`, `description`, `hours`, `online`) " + \
                      "VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (course['id'], course['name'], course['field'],
                                     course['description'], course['hours'], course['online']))
                count += 1
                if count % 10 is 0:
                    logging.info("Committing courses...")
                    cnx.commit()

            for ut_class in self.classes:
                sql = "REPLACE INTO `classes` (`unique`, `course_id`, `instructor`, `status`, " + \
                                  "`days1`, `start_time1`, `end_time1`, `room1`, " + \
                                  "`days2`, `start_time2`, `end_time2`, `room2`, `flags`) " + \
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (ut_class['unique'], ut_class['course_id'], ut_class['instructor'], ut_class['status'],
                                     ut_class['days1'], ut_class['start_time1'], ut_class['end_time1'], ut_class['room1'],
                                     ut_class['days2'], ut_class['start_time2'], ut_class['end_time2'], ut_class['room2'], ut_class['flags']))
                count += 1
                if count % 10 is 0:
                    logging.info("Committing classes...")
                    cnx.commit()

        logging.info("Complete!")
