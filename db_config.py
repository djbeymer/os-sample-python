from application import application
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = 'root'
application.config['MYSQL_DATABASE_PASSWORD'] = 'Passw0rd'
application.config['MYSQL_DATABASE_DB'] = 'discover'
application.config['MYSQL_DATABASE_HOST'] = '172.30.247.183'
mysql.init_app(application)
