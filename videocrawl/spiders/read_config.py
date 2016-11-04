import ConfigParser
import string, os, sys
cf = ConfigParser.ConfigParser()
cf.read("db.conf")
def get_dbhost():
    return cf.get("db", "db_host")
def get_dbport():
    return cf.getint("db", "db_port")


