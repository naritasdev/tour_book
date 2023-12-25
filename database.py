from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

<<<<<<< HEAD
usr = 'duoz5ozsyzetvzlksz2c'
pwd = 'pscale_pw_x5FU5Jifh4r6FuCAMwGCYaFdC43NNaz0iTQ9s97xPIm'
host = 'us-east.connect.psdb.cloud'
db = 'tours'
=======
host= os.getenv("DB_HOST")
user=os.getenv("DB_USERNAME")
passwd= os.getenv("DB_PASSWORD")
db= os.getenv("DB_NAME")
>>>>>>> 40ff45a (add secure credentiasl to db)

connection_string = "mysql+pymysql://" + user + ":" + passwd + "@" + host + ":3306/" + db
engine = create_engine(connection_string, 
                       echo=False,
                       connect_args={
                        "ssl": {
                        "ssl_ca":"/etc/ssl/cert.pem"
                        }
                    }
                )

