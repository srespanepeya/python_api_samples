from flask import Flask
from flask import request, jsonify
from flask_mail import Mail
from flask_mail import Message
from peyalookerapi import PeyaLookerApi
from peyaredshift import PeyaRedshift
from flask_api import status
import yaml
import json


f = open('config.yml')
params = yaml.load(f,Loader=yaml.BaseLoader)
f.close()

phrase = params['auth']['secret-phrase']
mail_server = params['smtp']['mail_server']
mail_port = params['smtp']['mail_port']
mail_username = params['smtp']['mail_username']
mail_password = params['smtp']['mail_password']
recipients = params['recipients']

app = Flask(__name__)

app.config.update(dict(
    DEBUG = False,
    MAIL_SERVER = mail_server,
    MAIL_PORT = mail_port,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = mail_username,
    MAIL_PASSWORD = mail_password,
))

mail = Mail(app)

@app.route("/api/v1/ping", methods=['GET'])
def ping():
    return "pong",status.HTTP_200_OK

@app.route("/api/v1/user/disable", methods=['GET'])
def disable_user():
    pPhrase = request.headers.get('secret-phrase')
    if phrase == pPhrase:
        if 'email' in request.args:
            email = request.args['email']
            looker = PeyaLookerApi()
            user =looker.get_user_by_email(email)
            if user: 
                print('----->User found with id {0} and is disabled {1}'.format(user.id, user.is_disabled))
                if user.is_disabled:
                    return jsonify({'acknowledged':True,'message':'User already disabled'}), status.HTTP_200_OK
                else:
                    id = user.id
                    body = {'is_disabled':True}
                    response = looker.update_user(id,body)
                    if response.is_disabled:
                        message = """
                            Hello Looker Admin,
                            this is an auto generated email sent just to let you know that user {0} with email {1} was disabled due to Bamboo deletion.
                            Kind regards,
                            PeYa BI Team

                            **Please do not reply this email
                        """.format(user.id,email)
                        msg = Message(body=message,subject="Test - User disabled in Looker",sender="santiago.respane@pedidosya.com",recipients=recipients)
                        print('--->{0}'.format(msg))
                        mail.send(msg)
                        return jsonify({'acknowledged':True,'message':'User found with id {0} and now is disabled'.format(user.id)}),status.HTTP_200_OK
            else:
                # Go and looker for the user in the gspreadsheet
                return jsonify({'acknowledged':False,'message':'User not found'}), status.HTTP_404_NOT_FOUND
        else:
            return jsonify({'acknowledged':False,'message':'Email parameter not provided'}), status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({'acknowledged':False,'message':'Unauthorized'}), status.HTTP_401_UNAUTHORIZED

@app.route("/api/v1/audit/get",methods=['POST'])
def getAuditState():
    pPhrase = request.headers.get('secret-phrase')
    if phrase == pPhrase:
        body = request.json
        # if validRequest(body):
        pDate = body['date']
        pJob_name = body['job_name']
        query = """select state,date_id,job_name from talend_status where job_name ='{job_name}' and date_id={date_id}""".format(job_name=pJob_name,date_id=pDate)
        print('--->{0}'.format(query))
        rds = PeyaRedshift()
        result = rds.runQuery(query)
        return jsonify(result[0]['state']=='SUCCESSFUL'),status.HTTP_200_OK 
    else:
        return "", status.HTTP_401_UNAUTHORIZED        

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

@app.route("/api/v1/users/list",methods=['GET'])
def getAllUsers():
    pPhrase = request.headers.get('secret-phrase')
    if phrase == pPhrase:
        looker = PeyaLookerApi()
        print('--->looker api initialized')
        users =looker.get_all_users()
        res = {"data":[]}

        for u in users:
            if not u.verified_looker_employee:
                # print ("#--->{0} - {1} - {2}".format(u.id,u.email,u.is_disabled))
                res["data"].append(
                    {
                        "id": u.id,
                        "display_name": u.display_name,
                        "email": u.email,
                        "is_disabled": u.is_disabled
                    }
                )

        print(len(res["data"]))

        print('--->looker users obtained')
        print('--->{0}'.format(type(res)))
        return jsonify(res),status.HTTP_200_OK 
        #return jsonify(user_list),status.HTTP_200_OK 
        #return app.response_class(res, content_type='application/json'),status.HTTP_200_OK 
    else:
        return "", status.HTTP_401_UNAUTHORIZED    

@app.route("/api/v1/schedule/plan/get",methods=['GET'])
def getSchedulePlan():
    pPhrase = request.headers.get('secret-phrase')
    if phrase == pPhrase:
        if 'id' in request.args:
            scheduled_plan_id = int(request.args['id'])
            looker = PeyaLookerApi()
            sp = looker.getSchedulePlan(scheduled_plan_id)

            res=jsonify({'user_id':sp.user_id,
                         'scheduled_plan_id':sp.id,
                         'destinations':[item.address for item in sp.scheduled_plan_destination]})

            print(res)
            #print(type(sp))

            return res,status.HTTP_200_OK  
        else: 
            return jsonify({'acknowledged':False,'message':'Id parameter not specified correctly'}), status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({'acknowledged':False,'message':'Unauthorized'}), status.HTTP_401_UNAUTHORIZED


@app.route("/api/v1/schedule/plan/delete",methods=['DELETE'])
def deleteSchedulePlan():
    pPhrase = request.headers.get('secret-phrase')
    if phrase == pPhrase:
        if 'id' in request.args:
            scheduled_plan_id = int(request.args['id'])
            looker = PeyaLookerApi()
            sp = looker.deleteSchedulePlan(scheduled_plan_id)
            print(sp)
            res=jsonify({'acknowledged':True,'response':sp})
            print(res)
            return res,status.HTTP_200_OK  
        else: 
            return jsonify({'acknowledged':False,'message':'Id parameter not specified correctly'}), status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({'acknowledged':False,'message':'Unauthorized'}), status.HTTP_401_UNAUTHORIZED




# if __name__ == '__main__':
app.run(host='0.0.0.0',port=5987)
app.run(debug=True)