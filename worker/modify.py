import pymysql.cursors
import atexit
import re

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

def get_sql(sql):
    """Wrapper for getting SQL query information."""
    with cnx.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        if cursor.rowcount is not 0:
            return result
        return None


courses = get_sql("SELECT * FROM `courses`")
print(courses[:5])
with cnx.cursor() as cursor:
    count = 0
    for course in courses:
        course['field'] = re.search(r"^([a-zA-Z ]{1,3})", course['name']).group(1)
        course['hours'] = course['name'][len(course['field'])]

        sql = "REPLACE INTO `courses` (`id`, `name`, `field`, `description`, `hours`, `online`) " + \
              "VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (course['id'], course['name'], course['field'],
                             course['description'], course['hours'], course['online']))
        count += 1
        if count % 10 is 0:
            print("%", 100*count/len(courses))
            cnx.commit()

classes = get_sql("SELECT * FROM `classes`")
print(classes[:5])