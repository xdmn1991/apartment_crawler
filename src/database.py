import psycopg2

CONNECT_STRING = "dbname=rent_detail user=yi"

class Database:
  @staticmethod
  def get_connection():
    return psycopg2.connect(CONNECT_STRING)