import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError

tables = {}

country_block = "country ENUM('AFG','ALA','ALB','DZA','ASM','AND','AGO','AIA','ATA','ATG','ARG','ARM','ABW','AUS','AUT','AZE','BHS','BHR','BGD','BRB','BLR','BEL','BLZ','BEN','BMU','BTN','BOL','BES','BIH','BWA','BVT','BRA','IOT','BRN','BGR','BFA','BDI','KHM','CMR','CAN','CPV','CYM','CAF','TCD','CHL','CHN','CXR','CCK','COL','COM','COG','COD','COK','CRI','CIV','HRV','CUB','CUW','CYP','CZE','DNK','DJI','DMA','DOM','ECU','EGY','SLV','GNQ','ERI','EST','ETH','FLK','FRO','FJI','FIN','FRA','GUF','PYF','ATF','GAB','GMB','GEO','DEU','GHA','GIB','GRC','GRL','GRD','GLP','GUM','GTM','GGY','GIN','GNB','GUY','HTI','HMD','VAT','HND','HKG','HUN','ISL','IND','IDN','IRN','IRQ','IRL','IMN','ISR','ITA','JAM','JPN','JEY','JOR','KAZ','KEN','KIR','PRK','KOR','KWT','KGZ','LAO','LVA','LBN','LSO','LBR','LBY','LIE','LTU','LUX','MAC','MKD','MDG','MWI','MYS','MDV','MLI','MLT','MHL','MTQ','MRT','MUS','MYT','MEX','FSM','MDA','MCO','MNG','MNE','MSR','MAR','MOZ','MMR','NAM','NRU','NPL','NLD','NCL','NZL','NIC','NER','NGA','NIU','NFK','MNP','NOR','OMN','PAK','PLW','PSE','PAN','PNG','PRY','PER','PHL','PCN','POL','PRT','PRI','QAT','REU','ROU','RUS','RWA','BLM','SHN','KNA','LCA','MAF','SPM','VCT','WSM','SMR','STP','SAU','SEN','SRB','SYC','SLE','SGP','SXM','SVK','SVN','SLB','SOM','ZAF','SGS','SSD','ESP','LKA','SDN','SUR','SJM','SWZ','SWE','CHE','SYR','TWN','TJK','TZA','THA','TLS','TGO','TKL','TON','TTO','TUN','TUR','TKM','TCA','TUV','UGA','UKR','ARE','GBR','USA','UMI','URY','UZB','VUT','VEN','VNM','VGB','VIR','WLF','ESH','YEM','ZMB','ZWE')"

province_block = "province ENUM('ALX','ASN','AST','BA','BH','BNS','C','DK','DT','FYM','GH','GZ','IS','JS','KB','KFS','KN','MN','MNF','MT','PTS','SHG','SHR','SIN','SUZ','WAD')"

sex_block = "sex ENUM('male', 'female') NOT NULL DEFAULT 'male'"

found_block = "ENUM('found','none') NOT NULL DEFAULT 'none'"

available_block = "ENUM('available','not found') NOT NULL DEFAULT 'not found'"

tables['manager_essentials'] = ("CREATE TABLE manager_essentials ("
    " code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " name char(80) NOT NULL,"
    " insurance bigint UNSIGNED NOT NULL DEFAULT 0 );")

tables['manager_extras'] = ("CREATE TABLE manager_extras ("
    " m_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " SSN bigint UNSIGNED NOT NULL DEFAULT 0 ,"
    "" + sex_block + ","
    " phone BIGINT UNSIGNED NOT NULL,"
    " bdate date,"
    " street varchar(100) NOT NULL DEFAULT '0',"
    "" + province_block + ","
    " FOREIGN KEY (m_code) REFERENCES manager_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['users_man'] = ("CREATE TABLE users_man ("
	" code smallint UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " username varchar(51) UNIQUE NOT NULL,"
    " hash char(74) NOT NULL,"
    " token char(32) NOT NULL,"
    " email varchar(70) NOT NULL,"
    " m_code smallint UNSIGNED NOT NULL,"
    " FOREIGN KEY (m_code) REFERENCES manager_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")


tables['tech_essentials'] = ("CREATE TABLE tech_essentials ("
    " code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " name char(80) NOT NULL,"
    " insurance bigint UNSIGNED NOT NULL DEFAULT 0 );")

tables['tech_extras'] = ("CREATE TABLE tech_extras ("
    " t_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " SSN bigint UNSIGNED NOT NULL DEFAULT 0 ,"
    "" + sex_block + ","
    " phone BIGINT UNSIGNED NOT NULL,"
    " bdate date,"
    " street varchar(100) NOT NULL DEFAULT '0',"
    "" + province_block + ","
    " FOREIGN KEY (t_code) REFERENCES tech_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['users_tech'] = ("CREATE TABLE users_tech ("
	" code smallint UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " username varchar(51) UNIQUE NOT NULL,"
    " hash char(74) NOT NULL,"
    " token char(32) NOT NULL,"
    " email varchar(70) NOT NULL,"
    " t_code smallint UNSIGNED NOT NULL,"
    " FOREIGN KEY (t_code) REFERENCES tech_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

tables['device_essentials'] = ("CREATE TABLE device_essentials ("
    " code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " serial INT UNSIGNED NOT NULL DEFAULT 0,"
    " type varchar(50) NOT NULL DEFAULT '0',"
    " maint_date date);")

tables['device_extras'] = ("CREATE TABLE device_extras ("
    " d_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " name varchar(50) NOT NULL DEFAULT '0',"
    " model varchar(30) NOT NULL DEFAULT '0',"
    " manufacturer varchar(50) NOT NULL,"
    "" + country_block +","
    " receive_date date,"
    " cost int UNSIGNED,"
    " remove_date date,"
    " status ENUM('operational', 'obselete'),"
    " FOREIGN KEY (d_code) REFERENCES device_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['device_description'] = ("CREATE TABLE device_description ("
    " d_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " description varchar(255) NOT NULL DEFAULT '0',"
    " FOREIGN KEY (d_code) REFERENCES device_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['order_essentials'] = ("CREATE TABLE order_essentials("
    " code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,"
    " serial INT UNSIGNED NOT NULL DEFAULT 0,"
    " place VARCHAR(80) NOT NULL,"
    " tech_code SMALLINT UNSIGNED,"
    " date_issued DATETIME NOT NULL);")

tables['order_extras'] = ("CREATE TABLE order_extras ("
    " date_responded DATETIME,"
    " foreign_sub " + found_block + ","
    " cracks " + found_block + ","
    " broken_battery " + found_block + ","
    " leaky_battery " + found_block + ","
    " drained_battery " + found_block + ","
    " damaged_cable " + found_block + ","
    " expired_electrode " + found_block + ","
    " damaged_elec_package " + found_block + ","
    " service_indicator " + found_block + ","
    " illumination_self_test " + available_block + ","
    " LEDs_on " + available_block + ","
    " speaker_beep " + available_block + ","
    " spare_batteries_avaiable " + available_block + ","
    " spare_electrodes_avaiable " + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0);")

engine = create_engine("mysql+pymysql://root:sqldata@localhost/CMMS",echo = None)
if not database_exists(engine.url):
    try:
        create_database(engine.url, "UTF8MB4")
    except SQLAlchemyError as err:
        print("Failed creating database: {}".format(err))
        exit(1)

for table_name in tables:
    table_description = tables[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='\n')
        engine.execute(table_description)
    except SQLAlchemyError as err:
        if err.orig.args[0] == 1050:
            print("table already exists")
        else:
            print("error occured {}".format(err))
    else:
        print("OK")
        
        

