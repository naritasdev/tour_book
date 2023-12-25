from sqlalchemy import create_engine

connection_string = "mysql+pymysql://xqfwvqq5cu6lbnn58sau:pscale_pw_V2GUBhUORuf1JtIJEE6fHg2UrdsAWP8yVDgVO6bc7kp@aws.connect.psdb.cloud:3306/tours"
engine = create_engine(connection_string, 
                       echo=False,
                       connect_args={
                        "ssl": {
                        "ssl_ca":"/etc/ssl/cert.pem"
                        }
                    }
                )

