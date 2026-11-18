import csv
import json
import glob

all_rows = []
csv_files = glob.glob("*.csv")

if not csv_files:
    raise FileNotFoundError("No such file found")

for csv_name in csv_files:
    with open(csv_name, "r", encoding = "utf-8", newline = "") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["source_file"] = csv_name
            all_rows.append(row)

print(f"Read {len(all_rows)} rows from {len(csv_files)} CSV files.")
valid_records = []
invalid_records = []
high_consumption_rates = []
duplicates = []
region_East_high_voltage_meters = 0
is_east = 0
is_east_total = 0
region_North_high_voltage_meters = 0
is_north = 0
is_north_total = 0
region_South_high_voltage_meters = 0
is_south_total = 0
is_south = 0
region_West_high_voltage_meters = 0
is_west = 0
is_west_total = 0
uniq_ids = []
get_sammary = []

for row in all_rows:
    time_stamp = row['timestamp']
    meter_id = str(row['meter_id'])

    if meter_id == None or meter_id == "":
        invalid_records.append(f"Meter id : {meter_id} has an invalid name")
        continue

    region = str(row['region'])

    if region == None or region == "":
            invalid_records.append(f"Meter id : {meter_id} has an invalid region")
            continue

    try:
        consumption = float(row['consumption_kwh'])

    except ValueError:
        invalid_records.append(f"Meter id : {meter_id} has an invalid consumption")
        continue

    if consumption < 0 :
        invalid_records.append(f"Meter id : {meter_id} has an invalid region")
        continue

    if consumption >= 250 :
        high_consumption_rates.append(meter_id)

        if region == "east":
            region_East_high_voltage_meters += 1

        elif region == "west":
            region_West_high_voltage_meters += 1

        elif region == "south":
            region_South_high_voltage_meters += 1

        else:
            region_North_high_voltage_meters += 1
            
        continue

    source = str(row['source_file'])

    uniq_id = time_stamp + meter_id 

    if uniq_id in uniq_ids:
            duplicates.append(f"Meter id : {meter_id} has a duplicate")
            continue
    
    uniq_ids.append(uniq_id)

    valid_records.append(row)

    if region == "east":
        is_east += 1
        is_east_total += consumption

    if region == "south":
        is_south += 1
        is_south_total += consumption
        

    if region == "north":
        is_north += 1
        is_north_total += consumption
        

    if region == "west":
        is_west += 1
        is_west_total += consumption

    
print({"Region" : 'East',
       "Number of valid meters" : f"{is_east}",
        "Average" : f'{is_east_total / is_east}KWH',
        "Total High Voltage readings" : f'{region_East_high_voltage_meters}'} )
print({"Region" : 'West',
       "Number of valid meters" : f"{is_west}",
        "Average" : f'{is_west_total/is_west}KWH',
        "Total High Voltage readings" : f'{region_West_high_voltage_meters}'} )
print({"Region" : 'North',
        "Number of valid meters" : f"{is_north}",
        "Average" : f'{is_north_total/is_north}KWH',
        "Total High Voltage readings" : f'{region_North_high_voltage_meters}'} )
print({"Region" : 'South',
        "Number of valid meters" : f"{is_south}",
        "Average" : f'{is_south_total/is_south}KWH',
        "Total High Voltage readings" : f'{region_South_high_voltage_meters}'} )
                


reports ={
"Number of files" : len(csv_files),
"Region summary" : {
 "East Region" : {
    "Records" : is_east,
    "Avg_KWH" : is_east_total / is_east,
    "High Usage" : region_East_high_voltage_meters},
"West Region" : {
    "Records" : is_west,
    "Avg_KWH" : is_west_total / is_west,
    "High Usage" : region_West_high_voltage_meters},
"North Region" : {
    "Records" : is_north,
    "Avg_KWH" : is_north_total / is_north,
    "High Usage" : region_North_high_voltage_meters},
"South Region" : {
    "Records" : is_south,
    "Avg_KWH" : is_south_total / is_south,
    "High Usage" : region_South_high_voltage_meters},
},
"Duplicates Found" : len(duplicates),
"Invalid Rows" : len(invalid_records),
"High Voltages" : high_consumption_rates
        }   

with open("data_reports.json", "w", encoding='utf-8') as file:
    json.dump(reports,file,indent=4)

print(reports)