import json
import atexit
import traceback
import logging
import pymysql.cursors
import falcon

from falcon_cors import CORS
from datetime import datetime, timedelta

allowed_origins = []  # ['http://localhost:63343']

log_file = 'backend.log'
log_level = logging.DEBUG
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

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

cnx = None

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


def ensure_mysql_connection():
    """Safely ensure that the mysql connection is still open (it times out)."""
    global cnx
    if cnx:
        if cnx.open:
            return
        cnx.close()
    cnx = pymysql.connect(**mysql_config)
    atexit.register(cnx.close)


class UTClass:
    """Models a UT Class based on a dict object of times, course id, etc."""
    def __init__(self, c):
        self.c = c

    def conflicts(self, other_class):
        """Check if class times conflict."""
        return self.c['course_id'] == other_class.c['course_id'] or \
               (self.c['start_time1'] and other_class.c['start_time1'] and
                (self.c['start_time1'] <= other_class.c['end_time1'] and self.c['end_time1'] >= other_class.c['start_time1'])) or \
               (self.c['start_time1'] and other_class.c['start_time2'] and
                (self.c['start_time1'] <= other_class.c['end_time2'] and self.c['end_time1'] >= other_class.c['start_time2'])) or \
               (self.c['start_time2'] and other_class.c['start_time1'] and
                (self.c['start_time2'] <= other_class.c['end_time1'] and self.c['end_time2'] >= other_class.c['start_time1'])) or \
               (self.c['start_time2'] and other_class.c['start_time2'] and
                (self.c['start_time2'] <= other_class.c['end_time2'] and self.c['end_time2'] >= other_class.c['start_time2']))

    def __str__(self):
        return str(self.c['unique'])


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code."""
    if isinstance(obj, UTClass):
        return obj.c

    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, timedelta):
        return (datetime.min + obj).time().isoformat()

    return str(type(obj))


def get_sql(sql):
    """Wrapper for getting SQL query information."""
    with cnx.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        if cursor.rowcount is not 0:
            return result
        return None


def conflicts_with_path(ut_class, path):
    """Check if class conflicts with other classes in path."""
    for class_in_path in path:
        if ut_class.conflicts(class_in_path):
            return True
    return False


def helper(start, visited_courses, visited_classes, path, possible_classes):
    """Helper method for generating possible class schedules."""
    if conflicts_with_path(start, path):
        return

    # Mark the current nodes as visited and store in path
    visited_courses[start.c['course_id']] = True
    visited_classes[start.c['unique']] = True
    path.append(start)

    # If path length reached, add it to schedules
    if len(path) >= len(possible_classes.keys()):
        yield list(path)
    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        for course_id in possible_classes.keys():
            if course_id in visited_courses:
                continue

            classes = possible_classes[course_id]
            for ut_class in classes:
                next_class = ut_class
                if next_class.c['course_id'] not in visited_courses or \
                    next_class.c['unique'] not in visited_classes:
                    for schedule in helper(next_class, visited_courses, visited_classes, path, possible_classes):
                        yield schedule

    # Remove current vertex from path[] and mark it as unvisited
    path.pop()
    visited_courses[start.c['course_id']] = False
    visited_classes[start.c['unique']] = False


def generate_schedules(selected_courses):
    """Generate possible schedules from selected courses."""
    schedules = []

    if len(selected_courses) <= 0:
        return schedules

    possible_classes = {}
    for course_id in selected_courses:
        if course_id not in possible_classes:
            possible_classes[course_id] = []
        for row in get_sql("SELECT * FROM `classes` WHERE `course_id` = " + str(course_id)):
            possible_classes[course_id].append(UTClass(row))

    course_classes = possible_classes[selected_courses[0]]
    for ut_class in course_classes:
        for schedule in helper(ut_class, {}, {}, [], possible_classes):
            schedules.append(schedule)

    logging.info("Generated schedules:", schedules)
    return schedules


class SchedulesResource(object):
    """ Retrieve a list of possible schedules given a list of desired courses. """

    def on_post(self, req, resp):
        ensure_mysql_connection()

        # Read in the raw json payload
        try:
            raw_json = req.stream.read()
            if isinstance(raw_json, bytes):
                raw_json = raw_json.decode('utf-8')
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

        # Parse the json payload
        try:
            # resp.body = raw_json
            course_ids = json.loads(raw_json, encoding='utf-8')
            resp.body = json.dumps(generate_schedules(course_ids), default=json_serial)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', 'Could not decode the request body. The JSON was incorrect.')


class LoadCoursesResource(object):
    """ Retrieve a list of courses given a field of study. """

    def on_get(self, req, resp, field):
        ensure_mysql_connection()

        resp_body = {}
        courses = get_sql("SELECT * FROM `courses` WHERE `field` = '" + field + "'")
        for course in courses:
            resp_body[course['id']] = course
        resp.body = json.dumps(resp_body, default=json_serial)

if allowed_origins:
    cors = CORS(allow_origins_list=['http://localhost:63343'])
else:
    cors = CORS(allow_all_origins=True, allow_all_headers=True)
app = application = falcon.API(middleware=[cors.middleware])

app.add_route('/schedules', SchedulesResource())
app.add_route('/{field}/courses', LoadCoursesResource())
