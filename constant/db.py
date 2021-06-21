from sqlalchemy import create_engine
from envr.envr import DB

#####################################

def my_create_engine(conn_str, pool_recycle=3600, pool_size=4):
    # MySQL connections become stale, so recyle them
    # every 'pool_recycle' seconds
    return create_engine(conn_str, pool_recycle=pool_recycle, pool_size=pool_size)

########## DB Engines ############
MYSQL_RW_CONN_STR    = DB['RW_CONN_STR']
AUTH_ENGINE   = my_create_engine(MYSQL_RW_CONN_STR)
