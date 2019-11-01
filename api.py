from flask import Flask
from flask import request, jsonify
from flask_mail import Mail
from flask_mail import Message
from peyalookerapi import PeyaLookerApi
from flask_api import status
import yaml

host = 'peya-looker'
f = open('config.yml')
params = yaml.load(f,Loader=yaml.BaseLoader)
f.close()

phrase = params['hosts'][host]['secret-phrase']
mail_server = params['hosts'][host]['mail_server']
mail_port = params['hosts'][host]['mail_port']
mail_username = params['hosts'][host]['mail_username']
mail_password = params['hosts'][host]['mail_password']

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
                            this is an email just to let you know that user {0} with email {1} was disabled due to Bamboo deletion.
                        """.format(user.id,email)
                        msg = Message(body=message,subject="Test - User disabled in Looker",sender="santiago.respane@pedidosya.com",recipients=["santiago.respane@pedidosya.com","looker.admins@pedidosya.com"])
                        print('--->{0}'.format(msg))
                        mail.send(msg)
                        return jsonify({'acknowledged':True,'message':'User found with id {0} and now is disabled'.format(user.id)}),status.HTTP_200_OK
            else:
                # Go and looker for the user in the gspreadsheet

                return jsonify({'acknowledged':False,'message':'User not found'}), status.HTTP_404_NOT_FOUND
            return email
        else:
            return jsonify({'acknowledged':False,'message':'Email parameter not provided'}), status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({'acknowledged':False,'message':'Unauthorized'}), status.HTTP_401_UNAUTHORIZED

# if __name__ == '__main__':
app.run(host='0.0.0.0',port=5000)
# app.run(debug=True)