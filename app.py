from DB_Stylist_Methods import *
from DB_Job_Methods import *
from flask import Flask, request, jsonify, make_response 
import json
from flask_sock import Sock

######################################
jsonFile = "Jobs.json"
stylistjson = "Stylist.json"

########## Read jobs from json file

with open(jsonFile) as job_file:
  file_contents = job_file.read()
print(file_contents)
job_file.close()

Jobs = json.loads(file_contents)
print(Jobs)

########## Read stylist from json file

with open(stylistjson) as st_file:
  file_contents = st_file.read()
print(file_contents)
st_file.close()

Stylists = json.loads(file_contents)
print(Stylists)

app = Flask(__name__)

sock = Sock(app)

@app.route("/")
def home():
    return "<h1>Home Page<h1>"    
 
@app.route("/about")
def about():
    return "<h1>About Page<h1>"  

@app.route('/jobs', methods=['GET'])
def api_get_jobs():
    return jsonify(get_jobs())

@app.route("/jobs/<name>", methods = ['GET'])
def api_get_job_by_stylist_name(name):
    stylist=[]
    DBJobs=get_jobs()
    for job in DBJobs:
        if job["Stylist"] == name:
            stylist.append(job)
    return jsonify(stylist)

@app.route("/jobs/<int:id>", methods= ['GET'])
def api_get_job_by_id(id):
   return jsonify(get_job_by_id(id))

@app.route('/stylists', methods=['GET'])
def api_get_stylists():
    return jsonify(get_stylists())

@app.route('/stylists/<stylist_id>', methods=['GET'])
def api_get_stylist_by_id(stylist_id):
    return jsonify(get_stylist_by_id(stylist_id))

@app.route('/stylists/<card_uid>', methods=['GET'])
def api_get_stylist_by_carduid(card_uid):
    print('card_uid=',card_uid)
    return jsonify(get_stylist_by_carduid(card_uid))

@app.route('/stylists/name/<name>', methods=['GET'])
def api_get_stylist_by_name(name):
    print('------------> name=',name)    
    return jsonify(get_stylist_by_name(name))

@app.route('/stylists/add',  methods = ['POST'])
def api_add_stylist():
    print(request)
    stylist = request.get_json()
    print(stylist)
    return jsonify(insert_stylist(stylist))

@app.route('/stylists/addall',  methods = ['GET'])
def api_addall_stylist():
    for st in Stylists:
        insert_stylist(st)
    return jsonify(Stylists)

@app.route('/stylists/update',  methods = ['PUT'])
def api_update_stylist():
    stylist = request.get_json()
    print("api_update_stylist=",stylist)
    return jsonify(update_stylist(stylist))

@app.route('/stylists/register/<int:stylist_id>',  methods = ['PUT'])
def api_register_stylist(stylist_id):
    stylist=get_stylist_by_id(stylist_id)
    cardUID = request.get_json()
    print("api_register_stylist=",stylist,"\t",cardUID)
    stylist["CardUID"]=cardUID
    print("api_register_stylist=",stylist,"\t",stylist["CardUID"])
    update_stylist(stylist)
    return jsonify(stylist)

@app.route('/stylists/delete/<stylist_id>',  methods = ['DELETE'])
def api_delete_stylist(stylist_id):
    return jsonify(delete_stylist(stylist_id))

@app.route("/stylists/jobs/<int:stylist_id>", methods = ['GET'])
def api_get_jobs_by_stylistID(stylist_id):
    stylist = get_stylist_by_id(stylist_id)
    name=stylist["Name"]
    DBJobs=get_jobs()    
    stylistjobs=[]
    for job in DBJobs:
        if job["Stylist"] == name:
            stylistjobs.append(job)
    return jsonify(stylistjobs)

@app.route("/login/<int:stylist_id>", methods= ['GET'])
def api_login(stylist_id):
    DBStylists=get_stylists()
    for st in DBStylists:
        if st["StylistID"] == stylist_id:  
            ipadd = request.environ['REMOTE_ADDR']
            st["IPAddr"]=ipadd
            st["Status"]="غیرآماده"
            update_stylist(st)
            return jsonify(st)
    stfail={"Name": "Unknown"}
    return jsonify(stfail)

@app.route("/login/<card_uid>", methods= ['GET'])
def api_login_card_uid(card_uid):
    print('card_uid=',card_uid)
    DBStylists=get_stylists()
    for st in DBStylists:
        if st["CardUID"] == card_uid:  
            ipadd = request.environ['REMOTE_ADDR']
            st["IPAddr"]=ipadd
            st["Status"]="غیرآماده"
            update_stylist(st)
            return jsonify(st)
    stfail={"Name": "Unknown"}
    return jsonify(stfail)

@app.route("/logoff/<name>", methods= ['GET'])
def api_logoff(name):
    DBStylists=get_stylists()
    for st in DBStylists:
        if st["Name"] == name:  
            st["Status"]="آفلاین"
            update_stylist(st)
            return jsonify(st)   

@app.route("/login/ready/<name>", methods= ['GET'])
def api_ready(name):
    DBStylists=get_stylists()
    for st in DBStylists:
        if st["Name"] == name:  
            st["Status"]="آماده"
            print(st)
            update_stylist(st)
            return jsonify(st)      

@app.route('/jobs/addall',  methods = ['GET'])
def api_addall_jobs():
    for job in Jobs:
        insert_job(job)
    return jsonify(Jobs)


@app.route('/jobs/assign/<int:id>', methods= ['GET'])
def api_assign_job(id):
    DBJobs=get_jobs()
    DBStylists=get_stylists()
    for job in DBJobs:
        if (job["ID"] == id): 
            print(job)
            name=job["Stylist"]
            for st in DBStylists:
                if (st["Name"]==name and job["Status"]=="انجام نشده"):
                    job["Status"] = "اختصاص داده"
                    job["QNumber"]= st["QPerson"]+1
                    st["QPerson"]= st["QPerson"]+1
                    st["QWating"]= st["QWating"]+job["Duration"]                   
                    job["QWating"]=st["QWating"]-job["Duration"] 
                    update_stylist(st)
                    update_job(job)        
            return jsonify(job)


@app.route("/jobs/accept/<int:id>", methods= ['GET'])
def api_accept(id):
    DBJobs=get_jobs()
    DBStylists=get_stylists()
    for job in DBJobs:        
        if (job["ID"] == id and job["Status"]=="اختصاص داده"): 
            name=job["Stylist"]
            for st in DBStylists:
                if (st["Name"]==name and st["Status"]=="آماده"):
                    jobac=job
                    job["Status"]= "در دست اقدام"
                    st["Status"]="مشغول"
                    job["QNumber"]=job["QNumber"]-1
                    st["QPerson"]=st["QPerson"]-1
                    job["QWating"]=0 
                    break
    name=jobac["Stylist"]
    print(name)
    for job in DBJobs: 
        if(job["ID"] != id and job["Status"]=="اختصاص داده" and job["Stylist"]==name):
            job["QNumber"]=job["QNumber"]-1
            print(job)
    for job in DBJobs:
        update_job(job)  
    for st in DBStylists:
        update_stylist(st)    
    return jsonify(jobac)


@app.route('/jobs/finish/<int:id>', methods= ['GET'])
def api_finish_job(id):
    DBJobs=get_jobs()
    DBStylists=get_stylists()
    for job in DBJobs:
        if (job["ID"] == id and job["Status"]=="در دست اقدام"): 
            name=job["Stylist"]
            for st in DBStylists:
                if (st["Name"]==name and st["Status"]=="مشغول"):
                    jobac=job
                    job["Status"]= "اتمام"
                    st["Status"]= "غیرآماده"
                    job["Finished"]=1
                    st["QWating"]= st["QWating"]-job["Duration"]
                    break
    name=jobac["Stylist"]
    for job in DBJobs: 
        if(job["ID"] != id and job["Status"]=="اختصاص داده" and job["Stylist"]==name):
            print("#######",jobac["Duration"])
            job["QWating"]=job["QWating"]-jobac["Duration"]
            print(job["QWating"]) 
    for job in DBJobs:
        update_job(job)  
    for st in DBStylists:
        update_stylist(st)    
    return jsonify(jobac)                


@sock.route('/echo')
def echo(sock):
    while True:
        data = sock.receive()
        print("*****> "+data)
        sock.send(data)       


@sock.route('/job')
def job(sock):
    while True:
        id=int(sock.receive())
        for job in Jobs:
            if job["ID"] == id:  
                print(job)
                sock.send(job)
                break  

                
@sock.route('/stylist')
def stylist(sock):
    while True:
        stylist=sock.receive()
        print(stylist)
        DBJobs=get_jobs()
        for job in DBJobs:
            if (job["Stylist"]==stylist and job["Status"]=="اختصاص داده"):
                print(job)
                sock.send(job)
                break

if __name__ == "__main__":  
    app.run() #run app