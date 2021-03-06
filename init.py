from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError

tables = {}

country_block = ("country ENUM('AFG','ALA','ALB','DZA','ASM','AND','AGO',"
"'AIA','ATA','ATG','ARG','ARM','ABW','AUS','AUT','AZE','BHS','BHR','BGD',"
"'BRB','BLR','BEL','BLZ','BEN','BMU','BTN','BOL','BES','BIH','BWA','BVT',"
"'BRA','IOT','BRN','BGR','BFA','BDI','KHM','CMR','CAN','CPV','CYM','CAF',"
"'TCD','CHL','CHN','CXR','CCK','COL','COM','COG','COD','COK','CRI','CIV',"
"'HRV','CUB','CUW','CYP','CZE','DNK','DJI','DMA','DOM','ECU','EGY','SLV',"
"'GNQ','ERI','EST','ETH','FLK','FRO','FJI','FIN','FRA','GUF','PYF','ATF',"
"'GAB','GMB','GEO','DEU','GHA','GIB','GRC','GRL','GRD','GLP','GUM','GTM',"
"'GGY','GIN','GNB','GUY','HTI','HMD','VAT','HND','HKG','HUN','ISL','IND',"
"'IDN','IRN','IRQ','IRL','IMN','ISR','ITA','JAM','JPN','JEY','JOR','KAZ',"
"'KEN','KIR','PRK','KOR','KWT','KGZ','LAO','LVA','LBN','LSO','LBR','LBY',"
"'LIE','LTU','LUX','MAC','MKD','MDG','MWI','MYS','MDV','MLI','MLT','MHL',"
"'MTQ','MRT','MUS','MYT','MEX','FSM','MDA','MCO','MNG','MNE','MSR','MAR',"
"'MOZ','MMR','NAM','NRU','NPL','NLD','NCL','NZL','NIC','NER','NGA','NIU',"
"'NFK','MNP','NOR','OMN','PAK','PLW','PSE','PAN','PNG','PRY','PER','PHL',"
"'PCN','POL','PRT','PRI','QAT','REU','ROU','RUS','RWA','BLM','SHN','KNA',"
"'LCA','MAF','SPM','VCT','WSM','SMR','STP','SAU','SEN','SRB','SYC','SLE',"
"'SGP','SXM','SVK','SVN','SLB','SOM','ZAF','SGS','SSD','ESP','LKA','SDN',"
"'SUR','SJM','SWZ','SWE','CHE','SYR','TWN','TJK','TZA','THA','TLS','TGO',"
"'TKL','TON','TTO','TUN','TUR','TKM','TCA','TUV','UGA','UKR','ARE','GBR',"
"'USA','UMI','URY','UZB','VUT','VEN','VNM','VGB','VIR','WLF','ESH','YEM','ZMB','ZWE')")

province_block = ("province ENUM('ALX','ASN','AST','BA','BH','BNS','C','DK',"
"'DT','FYM','GH','GZ','IS','JS','KB','KFS','KN','MN','MNF',"
"'MT','PTS','SHG','SHR','SIN','SUZ','WAD')")

status_block = ("status ENUM ('hired','fired','resigned') NOT NULL DEFAULT 'hired'")

sex_block = "sex ENUM('male', 'female') NOT NULL DEFAULT 'male'"

department_block = " ENUM('Admissions', 'Open Cardiology', 'Radiology')"

found_block = " ENUM('found','none') NOT NULL DEFAULT 'none'"

available_block = " ENUM('available','not found') NOT NULL DEFAULT 'not found'"

tables['manager_essentials'] = ("CREATE TABLE manager_essentials ("
    " code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " name char(80) NOT NULL,"
    " department " + department_block + ","
    "" + status_block + ","
    " insurance bigint UNSIGNED NOT NULL DEFAULT 0 );")

tables['manager_extras'] = ("CREATE TABLE manager_extras ("
    " r_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " SSN bigint UNSIGNED NOT NULL DEFAULT 0 ,"
    "" + sex_block + ","
    " phone BIGINT UNSIGNED NOT NULL,"
    " bdate date,"
    " street varchar(100) NOT NULL DEFAULT '0',"
    "" + province_block + ","
    " FOREIGN KEY (r_code) REFERENCES manager_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['users_man'] = ("CREATE TABLE users_man ("
	" code smallint UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " username varchar(51) UNIQUE NOT NULL,"
    " hash char(74) NOT NULL,"
    " token char(32) NOT NULL,"
    " email varchar(70) NOT NULL,"
    " r_code smallint UNSIGNED NOT NULL,"
    " FOREIGN KEY (r_code) REFERENCES manager_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")


tables['tech_essentials'] = ("CREATE TABLE tech_essentials ("
    " code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " name char(80) NOT NULL,"
    " department " + department_block + ","
    "" + status_block + ","
    " insurance bigint UNSIGNED NOT NULL DEFAULT 0 );")

tables['tech_extras'] = ("CREATE TABLE tech_extras ("
    " r_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " SSN bigint UNSIGNED NOT NULL DEFAULT 0 ,"
    "" + sex_block + ","
    " phone BIGINT UNSIGNED NOT NULL,"
    " bdate date,"
    " street varchar(100) NOT NULL DEFAULT '0',"
    "" + province_block + ","
    " FOREIGN KEY (r_code) REFERENCES tech_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['users_tech'] = ("CREATE TABLE users_tech ("
	" code smallint UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " username varchar(51) UNIQUE NOT NULL,"
    " hash char(74) NOT NULL,"
    " token char(32) NOT NULL,"
    " email varchar(70) NOT NULL,"
    " r_code smallint UNSIGNED NOT NULL,"
    " FOREIGN KEY (r_code) REFERENCES tech_essentials(code)"
	" ON UPDATE CASCADE ON DELETE CASCADE);")

tables['device_essentials'] = ("CREATE TABLE device_essentials ("
    " code SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,"
    " serial BIGINT UNSIGNED NOT NULL DEFAULT 0,"
    " type varchar(50) NOT NULL DEFAULT '0',"
    " status ENUM('operational', 'obselete') DEFAULT 'operational',"
    " maint_date date);")

tables['device_extras'] = ("CREATE TABLE device_extras ("
    " d_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " name varchar(50) NOT NULL DEFAULT '0',"
    " model varchar(30) NOT NULL DEFAULT '0',"
    " manufacturer varchar(50) NOT NULL,"
    "" + country_block +","
    " receive_date date NOT NULL,"
    " cost int UNSIGNED,"
    " department " + department_block + ","
    " remove_date date,"
    " FOREIGN KEY (d_code) REFERENCES device_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['device_description'] = ("CREATE TABLE device_description ("
    " d_code smallint UNSIGNED PRIMARY KEY NOT NULL,"
    " description varchar(255) NOT NULL DEFAULT '0',"
    " FOREIGN KEY (d_code) REFERENCES device_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['report_install'] = ("CREATE TABLE report_install ("
    " code MEDIUMINT UNSIGNED PRIMARY KEY,"
    " receive_date DATE,"
    " device_name varchar(50) NOT NULL DEFAULT '0',"
    " device_type varchar(50) NOT NULL DEFAULT '0',"
    " device_serial BIGINT UNSIGNED NOT NULL DEFAULT 0,"
    " device_manufacturer varchar(50) NOT NULL,"
    " cost int UNSIGNED NOT NULL DEFAULT 0,"
    " department " + department_block + ");")

tables['report_move'] = ("CREATE TABLE report_move ("
    " code MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,"
    " to_dep " + department_block + ","
    " from_dep " + department_block + ","
    " move_date DATE,"
    " device_code MEDIUMINT UNSIGNED NOT NULL,"
    " device_name varchar(50) NOT NULL DEFAULT '0',"
    " device_type varchar(50) NOT NULL DEFAULT '0',"
    " device_serial BIGINT UNSIGNED NOT NULL DEFAULT 0,"
    " device_manufacturer varchar(50) NOT NULL"
    ");")

tables['report_scrap'] = ("CREATE TABLE report_scrap ("
    " code MEDIUMINT UNSIGNED PRIMARY KEY,"
    " date DATE NOT NULL,"
    " device_name varchar(50) NOT NULL DEFAULT '0',"
    " device_type varchar(50) NOT NULL DEFAULT '0',"
    " device_serial BIGINT UNSIGNED NOT NULL DEFAULT 0,"
    " device_manufacturer varchar(50) NOT NULL,"
    " cause ENUM('upgrading', 'non-functional') NOT NULL DEFAULT 'non-functional'"
    ");")

tables['maintain_dates'] = ("CREATE TABLE maintain_dates ("
    " id MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,"
    " device_code MEDIUMINT UNSIGNED NOT NULL,"
    " maint_date DATE"
    ");")
    
tables['order_essentials'] = ("CREATE TABLE order_essentials("
    " code MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,"
    " serial BIGINT UNSIGNED NOT NULL DEFAULT 0,"
    " place VARCHAR(80) NOT NULL,"
    " type VARCHAR(80) NOT NULL,"
    " department " + department_block + ","
    " tech_code SMALLINT UNSIGNED,"
    " date_issued DATE NOT NULL,"
    " date_responded DATE,"
    " UNIQUE KEY (serial, date_issued));")

tables['order_extras_defib'] = ("CREATE TABLE order_extras_defib ("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " foreign_substance " + found_block + ","
    " cracks " + found_block + ","
    " broken_battery " + found_block + ","
    " leaky_battery " + found_block + ","
    " drained_battery " + found_block + ","
    " damaged_cable " + found_block + ","
    " expired_electrode " + found_block + ","
    " damaged_elecrode_package " + found_block + ","
    
    " service_indicator " + available_block + ","
    " illumination_self_test " + available_block + ","
    " LEDs_on " + available_block + ","
    " speaker_beep " + available_block + ","
    " spare_batteries_avaiable " + available_block + ","
    " spare_electrodes_avaiable " + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")


tables['order_extras_ECG'] = ("CREATE TABLE order_extras_ECG("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " foreign_substance " + found_block + ","
    " cracks " + found_block + ","
    " broken_battery " + found_block + ","
    " leaky_battery " + found_block + ","
    " drained_battery " + found_block + ","
    " damaged_cable " + found_block + ","
    " expired_electrode " + found_block + ","
    " damaged_elec_package " + found_block + ","
    " Incorrect_paper_loading " + found_block + ","
    " Printing_head_problem " + found_block + ","
    
    " service_indicator " + available_block + ","
    " spare_batteries_avaiable " + available_block + ","
    " spare_electrodes_avaiable " + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")


tables['order_extras_monitor'] = ("CREATE TABLE order_extras_monitor("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " cracks_in_strain_reliefs " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " damaged_cable " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_probes" + found_block + ","
    " malfunctional_Switches " + found_block + ","
    " broken_battery " + found_block + ","
    " leaky_battery " + found_block + ","
    " drained_battery " + found_block + ","
    " malfunctional_charger" + found_block + ","
    
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms" + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling" + available_block + ","
    " spare_batteries_avaiable " + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['order_extras_syringe_pump'] = ("CREATE TABLE order_extras_syringe_pump("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " cracks_in_strain_reliefs " + found_block + ","
    " Casters_or_brakes_not_mounted " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " damaged_detectors " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms " + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling" + available_block + ","
    " Operational_Flow_and_Stop_Mechanisms" + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['order_extras_infusion_pump'] = ("CREATE TABLE order_extras_infusion_pump("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " cracks_in_strain_reliefs " + found_block + ","
    " Casters_or_brakes_not_mounted " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " damaged_detectors " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms" + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling" + available_block + ","
    " Operational_Flow_and_Stop_Mechanisms" + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['order_extras_ventilator'] = ("CREATE TABLE order_extras_ventilator("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    
    " All_modes_working " + available_block + ","
    " Change_air_filter " + available_block + ","
    " Change_bacteria_filter " + available_block + ","
    " Change_fan_filter " + available_block + ","
    " Change_oxygen_sensor " + available_block + ","
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms " + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling " + available_block + ","
    " Spare_air_filters " + available_block + ","
    " Spare_bacteria_filters " + available_block + ","
    " Spare_oxygen_sensors " + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['order_extras_mob_ventilator'] = ("CREATE TABLE order_extras_mob_ventilator("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    " broken_battery " + found_block + ","
    " leaky_battery " + found_block + ","
    " drained_battery " + found_block + ","
    " malfunctional_charger" + found_block + ","

    
    " All_modes_working " + available_block + ","
    " Change_air_filter " + available_block + ","
    " Change_bacteria_filter " + available_block + ","
    " Change_fan_filter " + available_block + ","
    " Change_oxygen_sensor " + available_block + ","
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms " + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling " + available_block + ","
    " Spare_air_filters " + available_block + ","
    " Spare_bacteria_filters " + available_block + ","
    " Spare_oxygen_sensors " + available_block + ","
    " spare_batteries_avaiable " + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")


tables['order_extras_blood_gas'] = ("CREATE TABLE order_extras_blood_gas("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " malfunctional_bulbs " + found_block + ","
    " malfunctional_heaters " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms" + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling" + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['order_extras_Ultrasonic'] = ("CREATE TABLE order_extras_Ultrasonic("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    " malfunctional_transducer" + found_block + ","
    " Compromised_image_quality " + found_block + ","
    
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms" + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling" + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")


tables['order_extras_X_Ray'] = ("CREATE TABLE order_extras_X_Ray("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    " Above_limit_radiation " + found_block + ","
    " Compromised_image_quality " + found_block + ","
    
    " Lubricate_bearings " + available_block + ","
    " Lubricate_gears " + available_block + ","
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms" + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling" + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['order_extras_MRI'] = ("CREATE TABLE order_extras_MRI("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    " Above_limit_magnetization " + found_block + ","
    " Compromised_image_quality " + found_block + ","
    
    " Lubricate_bearings " + available_block + ","
    " Lubricate_gears " + available_block + ","
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms" + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling" + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['order_extras_CT'] = ("CREATE TABLE order_extras_CT("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    " Above_limit_radiation " + found_block + ","
    " Compromised_image_quality " + found_block + ","
    
    " Lubricate_bearings " + available_block + ","
    " Lubricate_gears " + available_block + ","
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms" + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling" + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")

tables['order_extras_Gamma_Camera'] = ("CREATE TABLE order_extras_Gamma_Camera("
    " r_code MEDIUMINT UNSIGNED NOT NULL,"
    " cracks_in_chassis " + found_block + ","
    " damaged_AC_plug " + found_block + ","
    " damaged_line_cord " + found_block + ","
    " tripped_Breaker " + found_block + ","
    " unconnected_cable_connectors " + found_block + ","
    " malfunctional_Switches " + found_block + ","
    " Above_limit_radiation " + found_block + ","
    " Compromised_image_quality " + found_block + ","
    
    " Lubricate_bearings " + available_block + ","
    " Lubricate_gears " + available_block + ","
    " Indicators_or_displays " + available_block + ","
    " Operational_alarms" + available_block + ","
    " Audible_signals " + available_block + ","
    " Operational_labeling" + available_block + ","
    " notes VARCHAR(255) NOT NULL DEFAULT 0,"
    " FOREIGN KEY (r_code) REFERENCES order_essentials(code)"
    " ON UPDATE CASCADE ON DELETE CASCADE);")



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
        
        

