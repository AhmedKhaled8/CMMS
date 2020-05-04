
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

def reflect_table(table_name,meta_object, engine_object):
    try:
        table = Table(table_name, meta_object, autoload = True, autoload_with = engine_object)
        return table
    except SQLAlchemyError as err:
        if type(err) == sqlalchemy.exc.NoSuchTableError:
            print("ERROR: table does not exists")
            return None
        elif err.orig.args[0] == 1103:
            print("ERROR: Invalid table name")
        else:
            print("Unknown error occured")
            return None

"""Please remember to take the Date import"""
import datetime


def addDeviceEssential(code, serial, deviceType, day, month, year):
    dictionary = {
        'code': code,
        'serial': serial,
        'type': deviceType,
        'maint_date': datetime.datetime(year, month, day)
    }
    return dictionary


# connect engine to database
engine = create_engine("mysql+pymysql://root:123456@localhost/CMMS",echo = None)
# make a metadata object for DB handling
meta = MetaData()
# make a DB_cursor object for commiting
db = engine.connect()


# Load tables into variables
device_essentials = reflect_table("device_essentials", meta, engine)
device_description = reflect_table("device_description", meta, engine)
device_extras = reflect_table("device_extras", meta, engine)


""""ADD YOUR DATA FOR device_essentials TABLE HERE USING addDeviceEssential""""
essentialData = [
    addDeviceEssential(1, 1234567890, "XRAY", 30, 11, 2010)
]

""" THE FOLLOWING 2 LINES ARE COMMENTED TO PREVENET ANOTHER INSERTION"""
""" UNCOMMENT THEM TO INSERT THE DATA """

# insertEssential = device_essentials.insert().values(essentialData)
# db.execute(insertEssential)

def addDescription(code, description):
    dictionary = {
        'd_code': code,
        'description': description
    }
    return dictionary


""""ADD YOUR DATA FOR device_description TABLE HERE USING addDescription""""
descriptionsData = [
    addDescription(1, "A DEVICE DISCRIPTION")
]


""" THE FOLLOWING 2 LINES ARE COMMENTED TO PREVENET ANOTHER INSERTION"""
""" UNCOMMENT THEM TO INSERT THE DATA """
# insertDescription = device_description.insert().values(descriptionsData)
# db.execute(insertDescription)

def addExtra(d_code, name, model, manufacturer, country, recieve_day, recieve_month, recieve_year, cost, remove_day, remove_month, remove_year, status):
    dictionary = {
        'd_code': d_code,
        'name': name,
        'model': model,
        'manufacturer': manufacturer,
        'country': country,
        'receive_date': datetime.datetime(recieve_year, recieve_month, recieve_day),
        'cost': cost,
        'remove_date': datetime.datetime(remove_year, recieve_month, recieve_day),
        'status': status
    }    
    return dictionary

""""ADD YOUR DATA FOR device_extras TABLE HERE USING addExtra""""
extraData = [
    addExtra(1, 'XRAY-SIEMENS', 'SIEMENS-WOW', 'SIEMENES', 'EGY', 3, 11, 1998, 1111111, 20, 10, 2000, 'operational')
]


""" THE FOLLOWING 2 LINES ARE COMMENTED TO PREVENET ANOTHER INSERTION"""
""" UNCOMMENT THEM TO INSERT THE DATA """
# insertExtra = device_extras.insert().values(extraData)
# db.execute(insertExtra)