import bcrypt
import sys

def find_int(findInt):

    string_id = ""
    int_id = -1

    for string in findInt:
        for eachChar in string:
            if eachChar.isdigit():
                string_id += eachChar

    if string_id == "":
        pass
    else:
        int_id = int_id + int(string_id) + 1
    return int_id

def get_message(data):
    split_data = data.split(b'\r\n')
    message = split_data[0]
    return message.decode("utf-8")

def get_content_length(data):
    for element in range(len(data)):
        if data[element].__contains__("Cache-Control"):
            get_length = data[element].split("\\r\\n")[0]
            return int(get_length)
    return 0

def find_username_email(data):
    getData = str(data).replace('"', "").split()
    email = ""
    username = ""

    i = 0
    while i < len(getData):

        if getData[i] == "email:":
            # this is email information
            email += getData[i + 1].replace(",", "")

        elif getData[i] == "username:":
            # this is username information
            username += getData[i + 1]

        i += 1

    return [email, username]

def return_bool(check):
    if check.__contains__("------WebKitFormBoundary"):
        return True
    return False

def get_comment_message(data):

    comment = ""

    i = 0
    print("length of data: ",len(data))
    while i < len(data):

        if data[i].__contains__("name"):
            add_message = i + 1
            while return_bool(data[add_message]) == False:
                comment += data[add_message]
                comment += " "
                add_message += 1
            print(comment)
            return comment
        else:
            i += 1

    return comment

def render_template(html_filename, data):
    # with open(html_filename) as html_file:
    #     template = html_file.read()
    #     template = replace_placeholders(template, data)
    #     template = render_loop(template, data)
    #     html_file.close()

    template = html_filename
    template = replace_placeholders(template, data)
    template = render_loop(template, data)
    return template

def replace_placeholders(template, data):
    replaced_template = template
    print("------------------list of key")
    print(data.keys())
    for placeholder in data.keys():
        if isinstance(data[placeholder], str):
            replaced_template = replaced_template.replace("{{"+placeholder+"}}", data[placeholder])
            print("PLACEHOLDER: ", placeholder)
            print("DATA: ", data)
    print("REPLACED_TEMPLATE: ", replaced_template)
    return replaced_template

def render_loop(template, data):
    if "loop_data" in data:
        loop_start_tag = "{{loop}}"
        loop_end_tag = "{{end_loop}}"

        start_index = template.find(loop_start_tag)
        end_index = template.find(loop_end_tag)

        loop_template = template[start_index + len(loop_start_tag): end_index]
        loop_data = data["loop_data"]

        loop_content = ""
        for single_piece_of_content in loop_data:
            loop_content += replace_placeholders(loop_template, single_piece_of_content)

        final_content = template[:start_index] + loop_content + template[end_index+len(loop_end_tag):]
        print("-----------------------------------------")
        print("TEMPLATE FINAL CONTENT: ", final_content)
        print("-----------------------------------------")
        return final_content

def frameLength(bits):
    payload = bits[11:18]
    print("bitsssssss: ", payload)
    int_payload = int(str(payload), 2)
    if int_payload == 126:
        return bits[18:34]
    elif int_payload == 127:
        return bits[18:82]
    else:
        return payload

def salt_hash_token(token):
    hashed_salted_token = bcrypt.hashpw(token.encode(), bcrypt.gensalt())
    return hashed_salted_token

# def hash_xsrf(token):
#     token = token.encode()
#     return token

def create(username: str, password: str, user) -> bool:
    b_pass = password.encode()
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(b_pass,salt)

    try:
        if username.__contains__("<") or username.__contains__(">") or username.__contains__("/"):
            return False
        find = user.find({}, {"_id": 0})
        username_exists = False
        for users in find:
            if username == users["username"]:
                print("username already exists")
                sys.stdout.flush()
                sys.stderr.flush()
                username_exists = True
                break
        if not username_exists:
            user.insert_one({"username": username, "password":hashed_pass, "authentication token": "-"})
            print("username and hashed password inserted to database successfully")
            sys.stdout.flush()
            sys.stderr.flush()
            return True
        else:
            return False
    except:
        print("username and hashed password could not be inserted to database")
        sys.stdout.flush()
        sys.stderr.flush()

def verify_token(hashed_salted_token, user):
    try:
        print("hash_salt_token: ",hashed_salted_token)
        sys.stdout.flush()
        sys.stderr.flush()
        find = user.find({}, {"_id": 0})
        for users in find:
            print("users: ", users)
            sys.stdout.flush()
            sys.stderr.flush()
            print("users token vs actual token: ", str(users["authentication token"]), str(hashed_salted_token).replace(";", ""))
            sys.stdout.flush()
            sys.stderr.flush()
            # b'$2b$12$RbUwqbmbkkH9lgdQTxmptuwfNAnIkNqp9W7QlXvU4XhyNntxUEA6a'
            # b'$2b$12$RbUwqbmbkkH9lgdQTxmptuwfNAnIkNqp9W7QlXvU4XhyNntxUEA6a'
            if str(users["authentication token"]) == str(hashed_salted_token):
                print("found!!!!: ", users["username"])
                sys.stdout.flush()
                sys.stderr.flush()
                return str(users["username"])
        sys.stdout.flush()
        sys.stderr.flush()
        print("could not verify token")
        return ""
    except:
        print("username could not be found based on token")
        sys.stdout.flush()
        sys.stderr.flush()
        return ""
def verify(username: str, password: str, user):
    try:
        b_pass = password.encode()
        db_return = user.find_one({"username": username})
        print("db_return: ", db_return)
        sys.stdout.flush()
        sys.stderr.flush()
        if db_return:
            db_hashed_pass = db_return["password"]
            print("checked")
            sys.stdout.flush()
            sys.stderr.flush()
            return bcrypt.checkpw(b_pass, db_hashed_pass)
        print("could not find the username in database")
        sys.stdout.flush()
        sys.stderr.flush()
    except:
        print("unexpected error occurred.")
        sys.stdout.flush()
        sys.stderr.flush()
        return False
def findFireFox(receiveData):
    checkFireFox = 0
    for i in receiveData:
        if i.__contains__("Firefox"):
            checkFireFox += 1
            return checkFireFox
    return checkFireFox
def decide_no_yes_message(checkData):
    no_message = ""
    for i in checkData:
        if i.__contains__("/?msg"):
            return i.split("?")[1].split("\\r\\n")[0].split("=")[1]
    return no_message


def message_encode(checkData):
    print("message in helper: ", checkData)
    sys.stdout.flush()
    sys.stderr.flush()
    message = checkData.replace("%24", "$")
    message = message.replace("%26", "&")
    message = message.replace("%2B", "+")
    message = message.replace("%2C", ",")
    message = message.replace("%2F", "/")
    message = message.replace("%3A", ":")
    message = message.replace("%3B", ";")
    message = message.replace("%3D", "=")
    message = message.replace("%3F", "?")
    message = message.replace("%40", "@")
    message = message.replace("%22", '"')
    message = message.replace("%3C", "<")
    message = message.replace("%3E", ">")
    message = message.replace("%23", "#")
    message = message.replace("%25", "%")
    message = message.replace("%7B", "{")
    message = message.replace("%7D", "}")
    # <b>+hello+</b>
    return message
