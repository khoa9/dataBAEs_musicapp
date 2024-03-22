import os
from sqlalchemy import *


'''
#parameters for arctic databases
db_username = 'svc-rspm'
db_password = 'ADENOID-tray-sailfish'
#db_host = 'recommendation-3.c8scn1wkslmg.us-east-2.rds.amazonaws.com'
#db_host = 'localhost'
db_host = 'arcresdb.rs.gsu.edu'
db_port = '3306'
#db_name = 'rspm'
#db_name = 'rspmdev'
db_name = 'RSPM_book_stage'
'''



#parameters for local database BOOK
db_username = 'root'
db_password = 'Admin123'
#db_host = 'recommendation-3.c8scn1wkslmg.us-east-2.rds.amazonaws.com'
db_host = 'localhost'
#db_host = 'arcresdb.rs.gsu.edu'
db_port = '3306'
#db_name = 'rspm'
#db_name = 'rspmdev'
db_name = 'rspm_book_prod_new'


# Create the database URL in the format required by SQLAlchemy
DB_URI = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"


#DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://nabeeltariq2:nabeeltariq2@nabeeltariq2.cpliemudyxqt.us-east-1.rds.amazonaws.com/nabeeltariq6?charset=utf8')






# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:sesame@localhost/movietweet?charset=utf8')



# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:sesame@localhost/movietweet_ratings?charset=utf8')



# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:sesame@localhost/movielensupgrade?charset=utf8')





# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://nabeeltariq3:nabeeltariq3@nabeeltariq3.cpliemudyxqt.us-east-1.rds.amazonaws.com/nabeeltariq3?charset=utf8')




# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://nabeeltariq2:nabeeltariq2@nabeeltariq2.cpliemudyxqt.us-east-1.rds.amazonaws.com/nabeeltariq2?charset=utf8')










# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://nabeeltariq2:nabeeltariq2@aa1taiyw3rzbwis.cpliemudyxqt.us-east-1.rds.amazonaws.com/aa1taiyw3rzbwis?charset=utf8')



# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://flask:nabeeltariq2@flasktest.cpliemudyxqt.us-east-1.rds.amazonaws.com/flaskdb?charset=utf8')


# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:sesame@localhost/movielens_meta?charset=utf8')

# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:sesame@localhost/amazonmusicalins2?charset=utf8')




# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://flask:nabeeltariq2@aa1bus1tdvnpq5m.cpliemudyxqt.us-east-1.rds.amazonaws.com/ebdb?charset=utf8')

#new database
# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://nabeeltariq2:nabeeltariq2@aa14nod91ksnt0i.cpliemudyxqt.us-east-1.rds.amazonaws.com/ebdb?charset=utf8')
