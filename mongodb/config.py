
def MongodbConfig(connexion):
    if connexion == "atlas":
        DB_ADMIN = ''
        DB_PASS = ''
        DB_CLUSTER = ''
        # If you work on mongo atlas
        URI = 'mongodb+srv://{}:{}@{}/test?retryWrites=true&w=majority'.format(DB_ADMIN, DB_PASS, DB_CLUSTER)
    else: 
        DB_HOST = ''
        DB_PORT = 0
        DB_NAME = ''
        DB_USER = ''
        DB_PASS = ''

        # If you work on local mongo compass
        URI = 'mongodb://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
    return URI

def FlaskConfig():
    pass