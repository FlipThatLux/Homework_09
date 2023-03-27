from pathlib import Path
import re
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to the script directory
os.chdir(script_dir)
# Now the current working directory is the same as the script directory

def greeting(user_input):
    return "How can I help you?"

def help(user_input):
    commands = [{"command": "hello", "description": "show greeting"},
                {"command": "help", "description": "show all available commands"},
                {"command": "add, name, phone_number", "description": "add a new contact"},
                {"command": "change, name, new_phone_number", "description": "change the phone number of an existing contact"},
                {"command": "phone, name", "description": "show the phone number of a contact"},
                {"command": "show all", "description": "show all contacts in console"},
                {"command": "goodbye", "description": "exit Phonebook manager"},
                {"command": "close", "description": "exit Phonebook manager"},
                {"command": "exit", "description": "exit Phonebook manager"}]
    result = ""
    for item in commands:
        result += f'{item["command"]}: {item["description"]}\n'
    return result

def check_file():
    result = "-"   #contacts.txt not found, try adding a contact first"
    try:
        with open("contacts.txt", "r") as file:
            content = file.readline()
            if content:
                result = "+"
    finally: return result

def valid_number(phone_number):
    phone_number = phone_number.strip('"')
    phone_number = phone_number.strip("'")
    if len(phone_number) > 15:
        return False
    for ch in phone_number:
        if ord(ch) not in range(48, 57 + 1) and ch not in (' ', '(', '+', ')'):
            return False
    if len(phone_number) <= 15:
        edited_phone_number = " " * (15 - len(phone_number)) + phone_number
    return edited_phone_number

def parcer(user_input): # Можливо, тут краще робити перевірку команд, імен чи номерів за допомогою re, але якщо користувач пише все як слід, то й цього вистачить
    disected_input = user_input.lower().split(",")
    command =  disected_input[0].strip(' ') if len(disected_input) > 1 else user_input.lower().strip(' ')
    name = disected_input[1].strip(' ') if len(disected_input) > 1 else None
    phone_number = disected_input[2].strip(' ') if len(disected_input) > 2 else None
    edited_phone_number = None
    if phone_number:
        edited_phone_number = valid_number(phone_number)
    input_data = {"command": command, "name": name, "phone_number": edited_phone_number}
    return input_data

def add(user_input):
    name = user_input["name"]
    phone_number = user_input["phone_number"]
    result = None
    if not name:
        return "Name invalid"
    if not phone_number:
        return "Phone number invalid"
    with open("contacts.txt", "a") as file:
        new_contact = {name:phone_number}
        file.write(str(new_contact) + "\n")
        file.close()
        file = open("contacts.txt", "r") # Цей рядок, як і два наступні, можна буде прибрати потім
        while True:
            line = file.readline()
            if not line or line == '\n':
                break
            result = line
    return f"Contact added: {result}"

def change(user_input):
    name = user_input["name"]
    phone_number = user_input["phone_number"]
    if not name:
        return "Name invalid"
    if not phone_number:
        return "Phone number invalid"
    result = 'Contact not found'
    with open("contacts.txt", "r+") as file:
        match_found = False
        while True:
            this_line_start = file.tell()
            line = file.readline()
            if not line or line == '\n':
                break
            name_from_line = re.search('[a-z]+', line)
            phone_number_start = name_from_line.span()[1] + this_line_start + 4
            name_from_line = name_from_line.group().strip('"')            
            #print(name_from_line, ref_name)
            if name_from_line == name:
                match_found = True
                #print('match found')
                phone_number_from_line = re.search('[0-9+()]+', line)            
                phone_number_end = phone_number_from_line.span()[1] + this_line_start - 1
                phone_number_from_line = phone_number_from_line.group().strip('"')
                #print(f"Name: {name_from_line}, phone number: {phone_number_from_line}")
                #print(phone_number_start, phone_number_end)
                phone_number = phone_number.strip('"')
                phone_number = phone_number.strip("'")
                #phone_number_len = len(phone_number)
                file.seek(phone_number_start)
                file.write(phone_number)
                file.seek(phone_number_end + 4)
                result = f'Match found = {match_found}\n{name_from_line} : {phone_number}'
                break
    return result

def show_contact(user_input):
    ref_name = user_input["name"]
    result = 'Contact not found'
    if not ref_name:
        result = "Name invalid"
        return result
    with open("contacts.txt", "r") as file:
        while True:
            line = file.readline()
            if not line or line == '\n':
                break
            name_from_line = re.search('[a-z]+', line)
            phone_number_from_line = re.search('[0-9+()]+', line)
            #print(phone_number_from_line, line)
            name_from_line = name_from_line.group().strip('"')
            phone_number_from_line = phone_number_from_line.group().strip('"')
            #print(name_from_line, ref_name)
            if name_from_line == ref_name:
                #print(f"Name: {name_from_line.capitalize()}, phone number: {phone_number_from_line}")
                result = f"Name: {name_from_line.capitalize()}, phone number: {phone_number_from_line}"
                break   
    return result

def show_all(user_input):
    with open("contacts.txt", "r") as file:
        result = ""
        while True:
            line = file.readline()
            #print(f"Problematic line: '{line}'")
            if not line or line == "\n":
                break
            name = re.search('[a-z]+', line)
            phone_number = re.search('[0-9+()]+', line)
            if name and phone_number:
                #result = f"name: {name.group().capitalize()}, phone number: {phone_number.group()}"
                result += f"name: {name.group().capitalize()}, phone number: {phone_number.group()}\n"
    return result

def handler(user_input):
    command = user_input["command"]
    result = None
    functions = {
                "hello": greeting,
                "help": help,
                "add": add,
                "change": change,
                "phone": show_contact,
                "show all": show_all
            }
    if command in ("goodbye", "close", "exit"):
        result = "Goodbye!"
    elif check_file() == "-":
        return "contacts.txt not found, try adding a contact first"
    elif command in functions.keys():
            # try:
            #     functions[command](user_input)
            # except: print("an error occured")
            result = functions[command](user_input)
    else:
        result = 'Unknown command, type "help" to see the list of commands'  
    return result

def main():

    print("Greetings, user! Phonebook manager online")
    
    functions = {
                 "hello": greeting,
                 "help": help,
                 "add": add,
                 "change": change,
                 "phone": show_contact,
                 "show all": show_all
                }
    
    while True:
        user_input = parcer(input('Enter a command: '))
        result = handler(user_input) 
        print(result)  
        if result == "Goodbye!":
            break
        elif result == 'Unknown command, type "help" to see the list of commands':
            continue

    # if edited_phone_number == False:
    #     print("The phone number seems to not suit the +**(***)******* format. Please try again")

main()