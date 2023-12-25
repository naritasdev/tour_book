from sqlalchemy import create_engine

usr = 'duoz5ozsyzetvzlksz2c'
pwd = 'pscale_pw_x5FU5Jifh4r6FuCAMwGCYaFdC43NNaz0iTQ9s97xPIm'
host = 'us-east.connect.psdb.cloud'
db = 'tours'

connection_string = "mysql+pymysql://" + usr + ":" + pwd + "@" + host + ":3306/" + db
engine = create_engine(connection_string, 
                       echo=False,
                       connect_args={
                        "ssl": {
                        "ssl_ca":"/etc/ssl/cert.pem"
                        }
                    }
                )

