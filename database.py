from sqlalchemy import create_engine

usr = '37i3djj7iynnncqf0er1'
pwd = 'pscale_pw_MOZsp0q6pht1TB4uHJzNPnNUjh3u7D9PSrOC2l2rkm6'
host = 'aws.connect.psdb.cloud'
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

