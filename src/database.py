import psycopg2

CONNECT_STRING = "dbname=rent"

class Database:
  @staticmethod
  def get_connection():
    return psycopg2.connect(CONNECT_STRING)
