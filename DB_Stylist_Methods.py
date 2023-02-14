import sqlite3

def connect_to_db():
    conn = sqlite3.connect('FanAsa.db')
    return conn

def insert_stylist(stylist):
    print("insert_stylist\t",stylist)
    inserted_stylist = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Stylists (StylistID, Name, IPAddr, QPerson, QWating, CardUID, Status) VALUES (?, ?, ?, ?, ?, ?)", 
                    (stylist['StylistID'],stylist['Name'], stylist['IPAddr'],
                    stylist['QPerson'],stylist['QWating'],stylist['CardUID'],stylist['Status']) )
        conn.commit()
        inserted_stylist = get_stylist_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_stylist

def get_stylists():
    stylists = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Stylists")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            stylist = {}
            stylist["StylistID"] = i["StylistID"]
            stylist["Name"] = i["Name"]
            stylist["IPAddr"] = i["IPAddr"]
            stylist["QPerson"] = i["QPerson"]
            stylist["QWating"] = i["QWating"]
            stylist["CardUID"] = i["CardUID"]
            stylist["Status"] = i["Status"]
            stylists.append(stylist)

    except:
       stylists = []
    print("Stylist: **********>",stylists)
    return stylists

def get_stylist_by_carduid(carduid):
    stylist = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Stylists WHERE CardUID = ?", 
                       (carduid,))
        row = cur.fetchone()

        # convert row object to dictionary
        stylist["StylistID"] = row["StylistID"]
        stylist["Name"] = row["Name"]
        stylist["IPAddr"] = row["IPAddr"]
        stylist["QPerson"] = row["QPerson"]
        stylist["QWating"] = row["QWating"]
        stylist["CardUID"] = row["CardUID"]
        stylist["Status"] = row["Status"]
       
    except:
        stylist = {}
    return stylist

def get_stylist_by_id(stylist_id):
    stylist = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Stylists WHERE StylistID = ?", 
                       (stylist_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        stylist["StylistID"] = row["StylistID"]
        stylist["Name"] = row["Name"]
        stylist["IPAddr"] = row["IPAddr"]
        stylist["QPerson"] = row["QPerson"]
        stylist["QWating"] = row["QWating"]
        stylist["CardUID"] = row["CardUID"]
        stylist["Status"] = row["Status"]
       
    except:
        stylist = {}
    return stylist

def get_stylist_by_name(name):
    stylist = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Stylists WHERE Name = ?", 
                       (name,))
        row = cur.fetchone()
        # convert row object to dictionary
        stylist["StylistID"] = row["StylistID"]
        stylist["Name"] = row["Name"]
        stylist["IPAddr"] = row["IPAddr"]
        stylist["QPerson"] = row["QPerson"]
        stylist["QWating"] = row["QWating"]
        stylist["CardUID"] = row["CardUID"]
        stylist["Status"] = row["Status"]
       
    except:
        stylist = {}
    return stylist

def update_stylist(stylist):
    updated_stylist = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Stylists SET Name = ?, IPAddr = ?, QPerson = ?, QWating = ?, CardUID = ?, Status = ? WHERE StylistID =?",  
                     (stylist['Name'], stylist['IPAddr'],stylist['QPerson'],
                     stylist['QWating'],stylist['CardUID'],stylist['Status'],
                     stylist['StylistID'],))
        conn.commit()
        updated_stylist = get_stylist_by_id(stylist["StylistID"])

    except:
        conn.rollback()
        updated_stylist = {}
    finally:
        conn.close()
    return updated_stylist

def delete_stylist(stylist_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Stylists WHERE StylistID = ?",     
                      (stylist_id,))
        conn.commit()
        message["status"] = "Stylist deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete stylist"
    finally:
        conn.close()
    return message
