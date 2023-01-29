import sqlite3

def connect_to_db():
    conn = sqlite3.connect('FanAsa.db')
    return conn

def insert_job(job):
    print("insert_job\t",job)
    inserted_job = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Jobs (ID, Type, Stylist, Customer, Finished, Duration, QNumber, QWating, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (job['ID'],job['Type'], job['Stylist'],
                    job['Customer'],job['Finished'],job['Duration'],
                    job['QNumber'],job['QWating'],job['Status'] ))
        conn.commit()
        inserted_job = get_job_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_job

def get_jobs():
    jobs = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Jobs")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            job = {}
            job["ID"] = i["ID"]
            job["Type"] = i["Type"]
            job["Stylist"] = i["Stylist"]
            job["Customer"] = i["Customer"]
            job["Finished"] = i["Finished"]
            job["Duration"] = i["Duration"]
            job["QNumber"] = i["QNumber"]
            job["QWating"] = i["QWating"]
            job["Status"] = i["Status"]
            jobs.append(job)

    except:
       jobs = []
    return jobs


def get_job_by_id(job_id):
    job = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Jobs WHERE ID = ?", 
                       (job_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        job["ID"] = row["ID"]
        job["Type"] = row["Type"]
        job["Stylist"] = row["Stylist"]
        job["Customer"] = row["Customer"]
        job["Finished"] = row["Finished"]
        job["Duration"] = row["Duration"]
        job["QNumber"] = row["QNumber"]
        job["QWating"] = row["QWating"]
        job["Status"] = row["Status"]        
    except:
        job = {}
    return job

def update_job(job):
    updated_job = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Jobs SET Type = ?, Stylist = ?, Customer =?, Finished = ?, Duration = ?, QNumber = ?, QWating = ?, Status = ?  WHERE ID =?",  
                     (job['Type'], job['Stylist'],job['Customer'],
                      job['Finished'],job['Duration'],
                      job['QNumber'],job['QWating'],job['Status'],
                      job['ID'],))
        conn.commit()
        updated_job = get_job_by_id(job["ID"])
    except:
        conn.rollback()
        updated_job = {}
    finally:
        conn.close()
    return updated_job


def delete_job(job_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Jobs WHERE ID = ?",     
                      (job_id,))
        conn.commit()
        message["status"] = "job deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete job"
    finally:
        conn.close()
    return message
