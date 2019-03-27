import pandas as pd

filename = "PopulateData.sql"

with open(filename, "w") as fp:
    # Creating Tables
    fp.write(
        'CREATE TABLE NeighbourhoodLocation ( \n'
        '   n_name VARCHAR(100), \n'
        '   lat REAL, \n'
        '   lon REAL, \n'
        '   PRIMARY KEY (n_name)); \n\n'

        'CREATE TABLE Demographic(\n'
        '   DID INT,\n'
        '   primary_language VARCHAR(50),\n'
        '   secondary_language VARCHAR(50),\n'
        '   third_language VARCHAR(50),\n'
        '   population INT,\n'
        '   num_old INT,\n'
        '   num_young INT,\n'
        '   PRIMARY KEY (DID));\n\n'

        'CREATE TABLE Neighbourhood(\n'
        '   NID INT,\n'
        '   n_name VARCHAR(100) NOT NULL,\n'
        '   DID INT NOT NULL,\n'
        '   PRIMARY KEY (NID),\n'
        '   FOREIGN KEY (n_name) REFERENCES NeighbourhoodLocation(n_name),\n'
        '   FOREIGN KEY (DID) REFERENCES Demographic(DID));\n\n'

        'CREATE TABLE Crime(\n'
        '   Crime_ID INT,\n'
        '   description VARCHAR(100),\n'
        '   c_datetime DATETIME,\n'
        '   NID INT NOT NULL,\n'
        '   PRIMARY KEY	(Crime_ID),\n'
        '   FOREIGN KEY (NID) REFERENCES Neighbourhood(NID));\n\n'

        'CREATE TABLE VehicleCollision(\n'
        '   Crime_ID INT,\n'
        '   license_plate VARCHAR(10),\n'
        '   PRIMARY KEY (Crime_ID),\n'
        '   FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID));\n\n'

        'CREATE TABLE Theft(\n'
        '   Crime_ID INT,\n'
        '   theft_type VARCHAR(20),\n'
        '   PRIMARY KEY (Crime_ID),\n'
        '   FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID));\n\n'

        'CREATE TABLE Item(\n'
        '   i_name VARCHAR(50),\n'
        '   i_value REAL,\n'
        '   PRIMARY KEY (i_name));\n\n'

        'CREATE TABLE StolenItem(\n'
        '   Crime_ID INT,\n'
        '   i_name VARCHAR(50),\n'
        '   description VARCHAR(100),\n'
        '   PRIMARY KEY (Crime_ID, i_name),\n'
        '   FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID),\n'
        '   FOREIGN KEY (i_name) REFERENCES Item(i_name));\n\n'

        'CREATE TABLE Criminal(\n'
        '   Criminal_ID INT,\n'
        '   age INT,\n'
        '   height_cm INT,\n'
        '   hair_color VARCHAR(10),\n'
        '   lives_in INT,\n'
        '   PRIMARY KEY (Criminal_ID),\n'
        '   FOREIGN KEY (lives_in) REFERENCES Neighbourhood(NID));\n\n'

        'CREATE TABLE CommittedBy(\n'
        '   Crime_ID INT,\n'
        '   Criminal_ID INT,\n'
        '   PRIMARY KEY (Crime_ID, Criminal_ID),\n'
        '   FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID),\n'
        '   FOREIGN KEY (Criminal_ID) REFERENCES Criminal(Criminal_ID)\n'
        '   ON DELETE CASCADE);\n\n'

        '## Insert tuples into NeighbourhoodLocation ##\n'
    )

    df = pd.read_csv("../data/Neighbourhood_Location.csv")
    sql_format = "INSERT INTO NeighbourhoodLocation VALUES ('{}', {}, {});\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["n_name"].strip(), row["lat"], row["lon"]))

    fp.write("\n## Insert tuples into Demographic ##\n")
    df = pd.read_csv("../data/Demographic.csv")
    sql_format = "INSERT INTO Demographic VALUES ({}, '{}', '{}', '{}', {}, {}, {});\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["Demographic_ID"], row["Pri_Lang"].strip(), row["Sec_Lang"].strip(),
            row["Thir_Lang"].strip(), row["Population"], row["Num_Old"], row["Num_Young"],
            row["Neighbourhood_ID"]))

    fp.write("\n## Insert tuples into Neighbourhood ##\n")
    df = pd.read_csv("../data/Neighbourhood.csv")
    sql_format = "INSERT INTO Neighbourhood VALUES ({}, '{}', {});\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["Neighbourhood_ID"], row["Name"].strip(), row["Demographic_ID"]))

    fp.write("\n## Insert tuples into Crime ##\n")
    df = pd.read_csv("../data/Crime.csv")
    sql_format = "INSERT INTO Crime VALUES ({}, '{}', '{}', {});\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["Crime_ID"], row["Description"].strip(), row["DateTime"],
            row["NID"]))

    fp.write("\n## Insert tuples into VehicleCollision ##\n")
    df = pd.read_csv("../data/Vehicle_Collision.csv")
    sql_format = "INSERT INTO VehicleCollision VALUES ({}, '{}');\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["Crime_ID"], row["License_Plate"]))

    fp.write("\n## Insert tuples into Theft ##\n")
    df = pd.read_csv("../data/Theft.csv")
    sql_format = "INSERT INTO Theft VALUES ({}, '{}');\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["Crime_ID"], row["Theft_Type"].strip()))

    fp.write("\n## Insert tuples into Item ##\n")
    df = pd.read_csv("../data/Items.csv")
    sql_format = "INSERT INTO Item VALUES ('{}', {});\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["Name"], row["Value"]))

    fp.write("\n## Insert tuples into StolenItem ##\n")
    df = pd.read_csv("../data/Stolen_Item.csv")
    sql_format = "INSERT INTO StolenItem VALUES ({}, '{}', '{}');\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["Crime_ID"], row["Name"], row["Description"]))

    fp.write("\n## Insert tuples into Criminal ##\n")
    df = pd.read_csv("../data/Criminal.csv")
    sql_format = "INSERT INTO Criminal VALUES ({}, {}, {}, '{}', {});\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["Criminal_ID"], row["Age"], row["Height"],
            row["Hair_Color"], row["NID"]))

    fp.write("\n## Insert tuples into CommittedBy ##\n")
    df = pd.read_csv("../data/Committed_By.csv")
    sql_format = "INSERT INTO CommittedBy VALUES ({}, {});\n"
    for i, row in df.iterrows():
        fp.write(sql_format.format(
            row["Crime_ID"], row["Criminal_ID"]))

