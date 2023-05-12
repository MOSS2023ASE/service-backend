from service_backend.settings import ENV
if ENV['USE_MYSQL']:
    import pymysql
    pymysql.install_as_MySQLdb()
