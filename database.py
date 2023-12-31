from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

host= os.getenv("DB_HOST")
user=os.getenv("DB_USERNAME")
passwd= os.getenv("DB_PASSWORD")
db= os.getenv("DB_NAME")

connection_string = "mysql+pymysql://" + user + ":" + passwd + "@" + host + ":3306/" + db
engine = create_engine(connection_string, 
                       echo=False,
                       connect_args={
                        "ssl": {
                        "ssl_ca":"/etc/ssl/cert.pem"
                        }
                    }
                )

