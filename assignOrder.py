
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
from sqlalchemy import and_

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
report_install = reflect_table("report_install", meta, engine)
tech_essentials = reflect_table("tech_essentials", meta, engine)
tech_extras = reflect_table("tech_extras", meta, engine)


def getTech(department):
    selectStatment = tech_essentials.select().where(and_(tech_essentials.c.department == department, tech_essentials.c.status=="hired"))
    selectedData = db.execute(selectStatment)
    techCodes = []
    for tech in selectedData:
        code = tech[0]
        techCodes.append(code)
    getDetails = tech_extras.select().where(tech_extras.c.r_code.in_(techCodes))
    selectedDetails = db.execute(getDetails)
    for detail in selectedDetails:
        print(detail)

getTech("Radiology")



from sqlalchemy.sql import select
def getDevice(serial, department):
    selectDevice = select([device_essentials, device_extras]).where(and_(device_essentials.c.serial==serial, device_extras.c.department==department))
    devicesSelected = db.execute(selectDevice)
    # There is a problem in the loop: 
    # count = 0
    # for device in devicesSelected:
    #     count += 1
    #     if count > 1:
    #         print("More than one device have the same serial")
    #         break
    firstDevice = devicesSelected.fetchone()
    print("Device: ", firstDevice)

getDevice(123, "Radiology")