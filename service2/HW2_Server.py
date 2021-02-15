# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from concurrent import futures
import logging
import grpc
import HW2_pb2
import HW2_pb2_grpc


class Homework2Servicer(HW2_pb2_grpc.Homework2Servicer):

    def SellerCreate(self, request, context):
        global Unique_Seller_ID
        Unique_Seller_ID += 1
        Seller_Database_Entry = {} #keys are user_name, password, seller_rating
        Seller_Database_Entry["user_name"] = request.name
        Seller_Database_Entry["password"]= request.password
        Seller_Database_Entry["seller_rating"] = 0

        print("Seller_Database_Entry ", Seller_Database_Entry)
        print("Unique_Seller_ID: ", Unique_Seller_ID)
        Seller_Database.update({Unique_Seller_ID:Seller_Database_Entry})
        print("Seller_Database ", Seller_Database)

        return_string = request.name + " " + request.password + " Account Created Successfully"
        return HW2_pb2.CreateReply(message=return_string,seller_id = str(Unique_Seller_ID))

    def SellerLogin(self, request, context):

        seller_id = int(request.seller_id)
        if seller_id in Seller_Database:
            print("seller_id in Seller_Database", Seller_Database[seller_id])

            if request.password == Seller_Database[seller_id]["password"]:
                print("passwords match")
                return_string = "Login Successful"
            else:
                print("passwords DO NOT match")
                return_string = "Login Unsuccessful, Passwords do not match"
        else:
            print("seller_id NOT in Seller_Database")
            return_string = "Login Unsuccessful, Seller_ID not found"

        return HW2_pb2.LoginReply(message=return_string)

    def SellerLogout(self, request, context):
        seller_id = int(request.seller_id)

        if seller_id in Seller_Database:
            print("seller_id in Seller_Database", Seller_Database[seller_id])
            return_string = "Logout Successful"
        else:
            print("seller_id NOT in Seller_Database")
            return_string = "Logout Unsuccessful, Seller_ID not found"

        return HW2_pb2.LogoutReply(message=return_string)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    HW2_pb2_grpc.add_Homework2Servicer_to_server(Homework2Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

# Seller_Database:
#   user_name: assigned by user at login, may not be unique
#   seller_ID: unique identifier assigned by system
#   seller_rating:
# ?? do I add a list of what this seller currently has for sale?  Or just search?

global Unique_Seller_ID
Unique_Seller_ID = 1111
Seller_Database = {}  #key is seller ID
Buyer_Database = {}

if __name__ == '__main__':

    logging.basicConfig()
    serve()
