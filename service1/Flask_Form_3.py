from __future__ import print_function
from flask import Flask,render_template,request

import logging

import grpc

import HW2_pb2
import HW2_pb2_grpc

app = Flask(__name__)

@app.route('/Create_Seller_Account/')
def create_seller_form():
    return render_template('create_seller_account_form.html')

@app.route('/Seller_Account_Data/', methods = ['POST', 'GET'])
def create_seller_data():

    if request.method == 'GET':
        return f"This URL cannot be accessed directly"
    if request.method == 'POST':
        form_data = request.form
        user_name = form_data.get("User_Name")
        password = form_data.get("Password")
        print("user_name: ",user_name, "password: ",password)
        response =  stub.SellerCreate(HW2_pb2.CreateRequest(name=user_name,password=password))
        print("Response received: " + response.message)
        print("Seller_ID received: " + response.seller_id)
        return_form_data = {}
        return_form_data.update({"User_Name: ":user_name,"Password: ":password,"Seller_ID":response.seller_id})
        print("Response received message: ",response.message)
        return render_template('create_seller_account_data.html',form_data = return_form_data)

@app.route('/Login_Seller_Account/')
def login_seller_form():
    return render_template('login_seller_account_form.html')

@app.route('/Login_Seller_Data/', methods = ['POST', 'GET'])
def login_seller_data():

    if request.method == 'GET':
        return f"This URL cannot be accessed directly"
    if request.method == 'POST':
        form_data = request.form
        seller_id = form_data.get("Seller_ID")
        password = form_data.get("Password")
        print("seller_id ",seller_id, "password: ",password)
        response =  stub.SellerLogin(HW2_pb2.LoginRequest(seller_id=seller_id,password=password))
        print("Response received: " + response.message)

        return render_template('login_seller_account_data.html',form_data = form_data, message=response.message )

@app.route('/Logout_Seller_Account/')
def logout_seller_form():
    return render_template('logout_seller_account_form.html')

@app.route('/Logout_Seller_Data/', methods = ['POST', 'GET'])
def logout_seller_data():
    if request.method == 'GET':
        return f"This URL cannot be accessed directly"
    if request.method == 'POST':
        form_data = request.form
        seller_id = form_data.get("Seller_ID")

        response =  stub.SellerLogout(HW2_pb2.LogoutRequest(seller_id=seller_id))
        print("Response received: " + response.message)
        return render_template('logout_seller_account_data.html',form_data = form_data,message=response.message)


channel = grpc.insecure_channel('localhost:50051')
stub = HW2_pb2_grpc.Homework2Stub(channel)
app.run(host='localhost', port=8080)
