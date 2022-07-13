import json
import socketserver
import sys
import uuid
from random import random
import hashlib
import base64
from pymongo import MongoClient

import helper

client = MongoClient("mongo")
db = client["database"]
user = db["user"]


class MyTCPHandler(socketserver.BaseRequestHandler):
    dict_message = {}
    dict_id = 0
    nextID = 0
    messages = []
    myWebSockets = []
    def handle(self):

        htmlFile = open("index.html", "r", encoding='utf-8').read().encode()
        js = open("functions.js", "r", encoding='utf-8').read().encode()
        css = open("style.css", "r", encoding='utf-8').read().encode()
        signedIn = open("signedPage.html", "r", encoding='utf-8').read().encode()
        signUp = open("signup.html", "r", encoding='utf-8').read().encode()



        received_data = self.request.recv(1024)

        print("received_data: ", received_data)
        sys.stdout.flush()
        sys.stderr.flush()

        decodeData = received_data
        checkData = str(decodeData).split()
        checkFireFox = 0
        for i in checkData:
            if i.__contains__("Firefox"):
                checkFireFox += 1
                break
        print("checkData: ", checkData)

        print("checkFireFox: ", checkFireFox)
        sys.stdout.flush()
        sys.stderr.flush()
        # checkData[1].split("=")[0] == "/?msg":

        # print("checkData[1].split[0] : ", checkData[1].split("?")[0])
        sys.stdout.flush()
        sys.stderr.flush()
        print("checkData[0]: ", checkData[0])
        sys.stdout.flush()
        sys.stderr.flush()
        print("checkData[1]: ", checkData[1])
        sys.stdout.flush()
        sys.stderr.flush()

        # this is for firefox
        if checkData[1] == "/" and checkFireFox != 0 and helper.decide_no_yes_message(checkData) == "":
            print("DID GO TO 0")
            sys.stdout.flush()
            sys.stderr.flush()



            visit_key = ""
            token_value = ""
            token_key = ""
            number = 0
            visit_value = ""
            authentication_value = ""
            checkVisit = ""
            for index in range(len(checkData)):
                if checkData[index].__contains__("Cookie"):
                    print("index: ", index)
                    split = checkData[index+1:]
                    # if i.__contains__("Upgrade-Insecure-Requests:"):
                    #     checkVisit = i.replace("\\r\\nUpgrade-Insecure-Requests:", "").split("=")[0]
                    #     value = i.replace("\\r\\nUpgrade-Insecure-Requests:", "").split("=")[1]
                    # else:
                    for i in split:
                        if i.__contains__("visit"):
                            print("i: ", i)
                            sys.stdout.flush()
                            sys.stderr.flush()
                            checkVisit = i.split("\\r\\n")[0]
                            visit_value = checkVisit.split("=")[1]
                            visit_key = checkVisit.split("=")[0]
                            print("checkVisit: ", checkVisit)
                            print("visit_key: ", visit_key)
                            print("visit_value: ", visit_value)
                            # break
                        # elif checkVisit == "Authentication":
                        elif i.__contains__("Authentication"):
                            print("iiiiiii: ", i)
                            sys.stdout.flush()
                            sys.stderr.flush()

                            print("checkvisitssss: ", checkVisit)
                            sys.stdout.flush()
                            sys.stderr.flush()
                            token_key += i.split("=")[0]
                            print("found TOKEN")
                            sys.stdout.flush()
                            sys.stderr.flush()
                            token_value = i.split("=")[1].split("\\r\\n")[0]
                            print("token_value1: ", token_value)
                            sys.stdout.flush()
                            sys.stderr.flush()
                            # token_value = token_value.replace(";", "")
                            # print("token_value2: ", token_value)
                            # sys.stdout.flush()
                            # sys.stderr.flush()
                            # token_value += str(token_value)
                            # print("token_value:" ,token_value)
                            # sys.stdout.flush()
                            # sys.stderr.flush()
                    # break
            if visit_key == "visits":
                    # visit_key += checkVisit
                    print("value.replace for firefox: ", visit_value.replace(";", ""))
                    sys.stdout.flush()
                    sys.stderr.flush()
                    number = int(visit_value.replace(";", "")) + 1
                    print("number for firefox: ", number)
                    sys.stdout.flush()
                    sys.stderr.flush()
                    with open("index.html", "r") as f:
                        template = f.read()
                    template = template.replace("number", str(number))

                    self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                         len(template)) + "\r\nSet-Cookie: visits=" + str(
                                         number) + "; Max-Age=3600\r\n" + "Location: \r\n\r\n" + str(
                                         template)).encode())
                    # break
            elif token_key == "Authentication":
                    token_key += checkVisit
                    print("found TOKEN")
                    sys.stdout.flush()
                    sys.stderr.flush()
                    token_value = token_value.replace("\\", "")
                    token_value = token_value.replace(";", "")
                    # token_key += str(token_value)
                    print("token_value: ", token_value)
                    sys.stdout.flush()
                    sys.stderr.flush()
                    # break
            # there were no visits
            elif visit_key == "" and visit_value == "":
                number += 1
                with open("index.html", "r") as f:
                    template = f.read()
                template = template.replace("number", str(number))

                self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                         len(template)) + "\r\nSet-Cookie: visits=" + str(
                                         number) + "; Max-Age=3600\r\n" + "Location: \r\n\r\n" + str(
                                         template)).encode())



            find_username = ""
            if token_value != "":
                print("authentication_value", token_value)
                sys.stdout.flush()
                sys.stderr.flush()
                print("checking verify_token")
                sys.stdout.flush()
                sys.stderr.flush()
                find_username += helper.verify_token(token_value, user)

            visits_value = 0
            print("find_username: ", find_username)
            sys.stdout.flush()
            sys.stderr.flush()

            print("VISIT_KEY: ", visit_key)
            sys.stdout.flush()
            sys.stderr.flush()

            print("VISIT VALUE: ", visits_value)
            sys.stdout.flush()
            sys.stderr.flush()

            print("TOKEN KEY: ", token_key)
            sys.stdout.flush()
            sys.stderr.flush()

            print("TOKEN VALUE: ", token_value)
            sys.stdout.flush()
            sys.stderr.flush()
            visited = 0
            if len(visit_key) == 0 or visit_key != "visits" or len(token_key) != 0 or token_key != "Authentication":

                # number += 1
                with open("index.html", "r") as f:
                    templateFirefox = f.read()


                print("AUTHENT. TOKEN: ", token_value)

                sys.stdout.flush()
                sys.stderr.flush()
                print("USER: ", find_username)
                sys.stdout.flush()
                sys.stderr.flush()
                if token_value != "" and find_username != "":
                    print("replacing user for firefox")
                    sys.stdout.flush()
                    sys.stderr.flush()
                    print("find_username: ", find_username)
                    sys.stdout.flush()
                    sys.stderr.flush()
                    templateFirefox = templateFirefox.replace("replace", find_username)
                    print("FIREFOX TEMPLATE: ", templateFirefox)
                    sys.stdout.flush()
                    sys.stderr.flush()
                    templateFirefox = templateFirefox.replace("number", str(number))

                    self.request.sendall((
                                                     "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                                 len(templateFirefox)) + "\r\nSet-Cookie: visits=" + str(
                                                 number) + "; Max-Age=3600\r\n" + "Location: \r\n\r\n" + str(
                                                 templateFirefox)).encode())
                else:
                    templateFirefox = templateFirefox.replace("number", str(number))

                    self.request.sendall(("HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                             len(templateFirefox)) + "\r\nSet-Cookie: visits=" + str(number) + "; Max-Age=3600\r\n" + "Location: \r\n\r\n" + str(
                                             templateFirefox)).encode())
                visited += 1
            elif visited == 0:
                number += 1
                print("exists")
                sys.stdout.flush()
                sys.stderr.flush()
                print("exists number: ", number)
                sys.stdout.flush()
                sys.stderr.flush()
                with open("index.html", "r") as f:
                    template = f.read()
                template = template.replace("number", str(number))
                # template = template.replace("user", str(find_username))


                # self.request.sendall((
                #                                  "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                #                              len(htmlFile)) + "\r\nSet-Cookie: visits=" + str(number) + "; Max-Age=3600\r\n" + "Location: \r\n\r\n" + str(
                #                              template)).encode())

            print("FINISH FIREFOX")
            sys.stdout.flush()
            sys.stderr.flush()
            # self.request.sendall((
            #                                  "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
            #                              len(htmlFile)) + "\r\nLocation: /welcome\r\n\r\n" + str(htmlFile.decode())).encode())




        elif checkData[1] == "/" and checkFireFox == 0:
            print("DID GO TO 1")
            sys.stdout.flush()
            sys.stderr.flush()
            key = ""
            token = ""
            token_key = ""
            number = 0
            authentication_value = ""

            for i in range(len(checkData)):
                if checkData[i].__contains__("Cookie:"):
                    split = checkData[i+1:]
                    print("split: ", split)
                    if len(split) > 1:
                        print("LEN(SPLIT) > 1")
                        sys.stdout.flush()
                        sys.stderr.flush()
                        if str(split[1].replace("\\r\\n\\r\\n'", "").split("=")[0]).replace("\\", "") == "Authentication":
                            authentication_value += str(split[1].replace("\\r\\n\\r\\n'", "").split("=")[1]).replace("\\", "")
                            authentication_value = authentication_value.replace(";", "")
                        else:
                            authentication_value += str(split[0].replace("\\r\\n\\r\\n'", "").split("=")[1]).replace("\\", "")
                            authentication_value = authentication_value.replace(";", "")

                        print("value: ", authentication_value)
                        sys.stdout.flush()
                        sys.stderr.flush()
                    for i in split:
                        print("i: ", i)
                        sys.stdout.flush()
                        sys.stderr.flush()
                        checkVisit = i.replace("\\r\\n\\r\\n'", "").split("=")[0]
                        value = i.replace("\\r\\n\\r\\n'", "").split("=")[1]
                        print("checkVisit: ", checkVisit)
                        if checkVisit == "visits":
                            key += checkVisit
                            print("value.replace: ", value.replace(";", ""))
                            sys.stdout.flush()
                            sys.stderr.flush()
                            number += int(value.replace(";", ""))
                            print("number: ", number)
                            sys.stdout.flush()
                            sys.stderr.flush()
                            break
                        elif checkVisit == "Authentication":
                            token_key += checkVisit
                            print("found TOKEN")
                            sys.stdout.flush()
                            sys.stderr.flush()
                            value = value.replace("\\", "")
                            value = value.replace(";", "")
                            token += str(value)
                            print(token)
                            sys.stdout.flush()
                            sys.stderr.flush()
                    break
            find_username = ""
            if authentication_value != "":
                print("authentication_value", authentication_value)
                sys.stdout.flush()
                sys.stderr.flush()
                print("checking verify_token")
                sys.stdout.flush()
                sys.stderr.flush()
                find_username += helper.verify_token(authentication_value,user)

            visits_value = 0
            print("find_username: ", find_username)
            sys.stdout.flush()
            sys.stderr.flush()

            print("KEY: ", key)
            sys.stdout.flush()
            sys.stderr.flush()

            print("VISIT VALUE: ", visits_value)
            sys.stdout.flush()
            sys.stderr.flush()

            if len(key) == 0 or key != "visits" or len(authentication_value) != 0 or authentication_value != "Authentication":

                number += 1
                # xsrf_token = ""
                # for users in user.find({}, {"_id": 0}):
                #     if users["authentication token"] == authentication_value:
                #         xsrf_token += str(users["XSRF"])
                with open("index.html", "r") as f:
                    template = f.read()
                # template = template.replace("{{xsrf}}", xsrf_token)
                print("AUTHENT. TOKEN2: ", authentication_value)
                sys.stdout.flush()
                sys.stderr.flush()
                print("USER2: ", find_username)
                sys.stdout.flush()
                sys.stderr.flush()
                if authentication_value != "" and find_username != "":
                    print("replacing user2")
                    sys.stdout.flush()
                    sys.stderr.flush()
                    template = template.replace("replace", find_username.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

                template = template.replace("number", str(number))

                self.request.sendall((
                                                 "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                             len(template)) + "\r\nSet-Cookie: visits=" + str(number) + "; Max-Age=3600\r\n" + "Location: \r\n\r\n" + str(
                                             template)).encode())
            else:

                number += 1
                print("exists")
                sys.stdout.flush()
                sys.stderr.flush()
                print("exists number: ", number)
                sys.stdout.flush()
                sys.stderr.flush()
                with open("index.html", "r") as f:
                    template = f.read()
                template = template.replace("number", str(number))


                self.request.sendall((
                                                 "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                             len(htmlFile)) + "\r\nSet-Cookie: visits=" + str(number) + "; Max-Age=3600\r\n" + "Location: \r\n\r\n" + str(
                                             template)).encode())

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                         len(htmlFile)) + "\r\nLocation:\r\n\r\n" + str(htmlFile.decode())).encode())
        # USER SIGN IN or SIGN UP FOR OTHERS
        elif len(checkData) != 0 and checkData[0] == "b'GET" and checkData[1].split("?")[0] == "/action_page.php" and checkFireFox == 0 and helper.findFireFox(checkData) == 0:
            print("DID GO TO 3")
            sys.stdout.flush()
            sys.stderr.flush()
        # elif len(checkData) != 0 and checkData[0] == "b'GET" and checkData[1] == "/signUp":
            print("GO TO SIGN UP")
            if checkFireFox == 0:
                # recData = received_data + self.request.recv(2048)
                recDataSplit = checkData
                getInfo = recDataSplit[1].split("?")
                print("getInfo: ", getInfo)
                sys.stdout.flush()
                sys.stderr.flush()
                get_username_and_password = recDataSplit[1].split("&")
                print("get_user_pass: ", get_username_and_password)
                sys.stdout.flush()
                sys.stderr.flush()
                username = get_username_and_password[0].split("=")[1].replace("+", " ").replace(">","&gt;").replace("<","&lt;").replace("&","&amp;")
                password = get_username_and_password[1].split("=")[1]
                print("username and password: ", username, password)
                sys.stdout.flush()
                sys.stderr.flush()

                #this is sign up
                if len(get_username_and_password) > 2:
                    sys.stdout.flush()
                    sys.stderr.flush()
                    created = helper.create(username,password, user)
                    if created:
                        self.request.sendall(("HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                                     len(htmlFile)) + "\r\nLocation: /\r\n\r\n" + str(
                                                     htmlFile.decode())).encode())
                    else:
                        print("stay signup for others after incorrect username")

                        with open("signup.html", "r") as f:
                            template = f.read()
                        template = template.replace("enter a unique username", "username already exists, or do not use speacial characters. please try a different username")
                        self.request.sendall((
                                                         "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                                     len(signUp)) + "\r\nLocation: \r\n\r\n" + str(
                                                     template)).encode())

                # this is sign in
                else:
                    verified = helper.verify(username,password,user)
                    print("checking verification")
                    sys.stdout.flush()
                    sys.stderr.flush()
                    if verified:
                        print("username and password verified in sign in!")
                        sys.stdout.flush()
                        sys.stderr.flush()
                        auth_token = helper.salt_hash_token(str(uuid.uuid4()))
                        xsrf_token = str(uuid.uuid4())
                        user.update_one({"username": username}, {"$set": {'authentication token': auth_token}})
                        user.update_one({"username": username}, {"$set": {'XSRF': xsrf_token}})

                        # with open("index.html", "r") as f:
                        #     template = f.read()
                        # template = template.replace("username", username.replace("+", " ").replace(">","&gt;").replace("<","&lt;").replace("&","&amp;"))
                        # template = template.replace("{{xsrf}}", xsrf_token)

                        # print("TEMPLATE XSRF: ", template)
                        sys.stdout.flush()
                        sys.stderr.flush()
                        self.request.sendall((
                                                         "HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8" + "\r\nSet-Cookie: Authentication=" + str(
                                                     auth_token) + "; Max-Age=3600\r\n" + "Location: /\r\n\r\n").encode())
                        # self.request.sendall(("HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                        #                          len(template)) + "\r\nSet-Cookie: Authentication=" + str(auth_token) + "; Max-Age=3600\r\n" + "Location: /\r\n\r\n" + str(
                        #                          template)).encode())
                    else:
                        print("incorrect username or pass")
                        sys.stdout.flush()
                        sys.stderr.flush()
                        with open("index.html", "r") as f:
                            template = f.read()
                        template = template.replace("&#128273;", "incorrect username or password!")
                        self.request.sendall(("HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                                     len(htmlFile)) + "\r\nLocation: /\r\n\r\n" + str(template)).encode())
                    find = user.find({}, {"_id": 0})
                    for users in find:
                        print("user that logged in: ", users)
                        sys.stdout.flush()
                        sys.stderr.flush()
                        # dict = {"$set": {"id": int_id, "email": str(getData[0]), "username": str(getData[1])}}


        # USER SIGN IN or SIGN UP FOR FIREFOX

        elif len(checkData) != 0 and checkData[0] == "b'GET" and checkData[1].split("?")[0] == "/action_page.php" and checkFireFox != 0 and helper.findFireFox(checkData) == 1:
        # elif len(checkData) != 0 and checkData[0] == "b'GET" and checkData[1].split("?")[0] == "/signUp" and checkFireFox != 0:
            print("DID GO TO 4")
            sys.stdout.flush()
            sys.stderr.flush()
            if checkFireFox != 0:
                # recData = received_data + self.request.recv(2048)
                recDataSplit = checkData
                getInfo = recDataSplit[1].split("?")
                print("getInfo2: ", getInfo)
                sys.stdout.flush()
                sys.stderr.flush()
                get_username_and_password = recDataSplit[1].split("&")
                username = get_username_and_password[0].split("=")[1]
                password = get_username_and_password[1].split("=")[1]
                print("get_username_and_password: ", get_username_and_password)
                sys.stdout.flush()
                sys.stderr.flush()
                print("username and password2: ", username, password)
                sys.stdout.flush()
                sys.stderr.flush()

                #this is sign up for firefox
                if len(get_username_and_password) > 2:
                    print("this is signup firefox: ")
                    sys.stdout.flush()
                    sys.stderr.flush()
                    created = helper.create(username,password, user)
                    if created:
                        self.request.sendall(("HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                                     len(htmlFile)) + "\r\nLocation: /\r\n\r\n" + str(
                                                     htmlFile.decode())).encode())
                    else:

                        with open("signup.html", "r") as f:
                            template = f.read()
                        template = template.replace("enter a unique username", "username already exists, or do not use speacial characters. please try a different username")
                        self.request.sendall((
                                                         "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                                     len(signUp)) + "\r\nLocation: \r\n\r\n" + str(
                                                     template)).encode())

                # this is sign in for firefox
                else:
                    verified = helper.verify(username,password,user)
                    print("checking verification2")
                    sys.stdout.flush()
                    sys.stderr.flush()
                    if verified:
                        print("username and password verified in sign in!2")
                        sys.stdout.flush()
                        sys.stderr.flush()
                        auth_token = helper.salt_hash_token(str(uuid.uuid4()))
                        user.update_one({"username": username}, {"$set": {'authentication token': auth_token}})
                        with open("index.html", "r") as f:
                            template = f.read()
                        template = template.replace("replace", username.replace("+", " ").replace(">","&gt;").replace("<","&lt;").replace("&","&amp;"))
                        self.request.sendall((
                                                     "HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                                 len(template)) + "\r\nSet-Cookie: Authentication=" + str(
                                                 auth_token) + "; Max-Age=3600\r\n" + "Location: /\r\n\r\n" + str(
                                                 template)).encode())
                        # self.request.sendall((
                        #                                  "HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                        #                              len(template.encode())) + "\r\nSet-Cookie: Authentication=" + str(
                        #                           auth_token) + "\r\nLocation: /\r\n\r\n" +
                        #                              template).encode())
                    else:
                        print("incorrect username or pass2")
                        sys.stdout.flush()
                        sys.stderr.flush()
                        with open("index.html", "r") as f:
                            template = f.read()
                        template = template.replace("&#128273;", "incorrect username or password!")
                        self.request.sendall(("HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                                     len(htmlFile)) + "\r\nLocation: /\r\n\r\n" + str(template)).encode())
                    find = user.find({}, {"_id": 0})
                    for users in find:
                        print("user that logged in: ", users)
                        sys.stdout.flush()
                        sys.stderr.flush()
                        # dict = {"$set": {"id": int_id, "email": str(getData[0]), "username": str(getData[1])}}

        # this is message
        # elif len(checkData) != 0 and checkData[0].__contains__("GET") and str(checkData[1].split("=")[0]) == "/?msg":
        elif len(checkData) != 0 and checkData[0].__contains__("GET") and checkData[1].__contains__("msg"):
                xsrf = checkData[1].split("=")[1].split("&")[0]
                print("DID GO TO 2")
                sys.stdout.flush()
                sys.stderr.flush()
                print("MESSAGE: ", checkData[1].split("=")[1])
                sys.stdout.flush()
                sys.stderr.flush()
            # if checkFireFox == 0:
                authentication_value = ""
                message = helper.message_encode(checkData[1].split("=")[1].replace("+", " "))
                message = message.replace(">","&gt;").replace("<","&lt;").replace("&","&amp;")
                # message = message.replace(">",">").replace("<","<").replace("&","&")

                print("message: ", message)
                sys.stdout.flush()
                sys.stderr.flush()
                visits_value = 0
                for i in range(len(checkData)):
                    if checkData[i].__contains__("Cookie:"):
                        split = checkData[i+1:]
                        print("split: ", split)
                        if len(split) > 1:
                            print("LEN(SPLIT) > 1")
                            sys.stdout.flush()
                            sys.stderr.flush()
                            for i in range(len(split)):
                                # OTHERS
                                if checkFireFox == 0:
                                    if str(split[i].replace("\\r\\n\\r\\n'", "").split("=")[0]).replace("\\","") == "Authentication":
                                        authentication_value += str(split[i].replace("\\r\\n\\r\\n'", "").split("=")[1]).replace(
                                            "\\", "")
                                        authentication_value = authentication_value.replace(";", "")

                                    elif str(split[i].replace("\\r\\n\\r\\n'", "").split("=")[0]).replace("\\","") == "visits":
                                        visits_value += int(split[i].replace("\\r\\n\\r\\n'", "").split("=")[1].replace(
                                            "\\", "").replace(";", ""))
                                    else:
                                        pass
                                # FIREFOX
                                else:
                                    if str(split[i].replace("\\r\\n\\r\\n'", "").split("=")[0]).replace("\\", "") == "Authentication":
                                        authentication_value += str(split[i].split("\\r\\n")[0].split("=")[1]).replace("\\", "")
                                        authentication_value = authentication_value.replace(";", "")

                                    elif str(split[i].replace("\\r\\n\\r\\n'", "").split("=")[0]).replace("\\","") == "visits":
                                        # visits_value += int(split[i].replace("\\r\\n\\r\\n'", "").split("=")[1].replace("\\", "").replace(";", ""))
                                        visits_value += int(split[i].split("\\r\\n")[0].split("=")[1].replace(";", ""))
                                    else:
                                        pass

                            print("authent value: ", authentication_value)
                            sys.stdout.flush()
                            sys.stderr.flush()
                            print("visit value: ", visits_value)
                            sys.stdout.flush()
                            sys.stderr.flush()
                if authentication_value != "":
                    username = helper.verify_token(authentication_value, user)
                    if username != "":
                        print("verified token and username!")
                        sys.stdout.flush()
                        sys.stderr.flush()
                        with open("index.html", "r") as f:
                            template = f.read()
                        # template = template.replace("{{name}}", username)
                        # template = template.replace("{{message}}", str(message))
                        template = template.replace("replace", username)
                        template = template.replace("number", str(visits_value + 1))

                        add_data = {"name": username, "message": message,}

                        alreadySend = 0
                        # len_mess = len(MyTCPHandler.messages)
                        print("messages: ", MyTCPHandler.messages)
                        sys.stdout.flush()
                        sys.stderr.flush()
                        for previousMessages in MyTCPHandler.messages:
                            if previousMessages["name"] == username and previousMessages["message"] == message:
                        # if len_mess > 0 and MyTCPHandler.messages[len_mess -1]["name"] == username and MyTCPHandler.messages[len_mess-1]["message"] == message:
                                alreadySend += 1
                        if alreadySend == 0:
                            MyTCPHandler.messages.append(add_data)
                            print("messages: ", MyTCPHandler.messages)
                            sys.stdout.flush()
                            sys.stderr.flush()

                        content = helper.render_template(template, {"loop_data": MyTCPHandler.messages})

                        with open("copy.html", "w") as file:
                            file.write(content)
                            file.close()
                        print("TEMPLATE: ", content)

                        find = user.find({}, {"_id": 0})
                        find_xsrf = xsrf
                        # for users in find:
                        #     if users["username"] == username and users["XSRF"] != find_xsrf:
                        #         print("no XSRF!!")
                        #         sys.stdout.flush()
                        #         sys.stderr.flush()
                        #         error = "\r\n you have no permission to this page"
                        #         self.request.sendall(("HTTP/1.1 403 Forbidden Error\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                        #                                      len(error)) + error).encode())
                        #         break

                        self.request.sendall(("HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(len(content)) + "\r\nSet-Cookie: visits=" + str(visits_value + 1) + "; Max-Age=3600" + "\r\nLocation: /" + "\r\n\r\n" + str(content)).encode())

                        # self.request.sendall(("HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(len(content)) + "\r\nLocation: /\r\n\r\n" + str(content)).encode())
                    else:
                        print("found token but no username")
                        sys.stdout.flush()
                        sys.stderr.flush()
                        self.request.sendall(("HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(len(htmlFile)) + "\r\nLocation: /\r\n\r\n" + str(htmlFile)).encode())

                else:
                    print("message should not appear")
                    sys.stdout.flush()
                    sys.stderr.flush()
                    # self.request.sendall(("HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                    #                              len(htmlFile)) + "\r\nSet-Cookie: visits=" + str(visits_value) + "; Max-Age=3600\r\n" + "\r\nLocation: /\r\n\r\n" + str(
                    #                              htmlFile)).encode())
                    self.request.sendall((
                                                     "HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                                 len(htmlFile)) + "\r\nLocation: /\r\n\r\n" + str(htmlFile)).encode())



        elif len(checkData) != 0 and checkData[1] == "/signUp":
            print("---------------------------------------------signup-------------------------------------------")
            sys.stdout.flush()
            sys.stderr.flush()
            self.request.sendall(("HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                         len(signUp)) + "\r\nLocation:\r\n\r\n" + str(signUp.decode())).encode())

        elif len(checkData) != 0 and checkData[1] == "/functions.js":
            print("---------------------------------function----------------------------------")
            sys.stdout.flush()
            sys.stderr.flush()
            self.request.sendall(("HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/javascript; charset=utf-8\r\nContent-Length: " + str(
                                         len(js)) + "\r\nLocation:\r\n\r\n" + str(js.decode())).encode())

        elif len(checkData) != 0 and checkData[1] == "/style.css":
            print("---------------------------------------------style----------------------------------")
            sys.stdout.flush()
            sys.stderr.flush()
            self.request.sendall(("HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/css; charset=utf-8\r\nContent-Length: " + str(
                                         len(css)) + "\r\n\r\n" + str(css.decode())).encode())

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000

    print("server is not running")
    sys.stdout.flush()
    sys.stderr.flush()
    # port = 3779


    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()
