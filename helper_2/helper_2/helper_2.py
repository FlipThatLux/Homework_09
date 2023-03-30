phonebook = {}

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

def parcer(user_input):
    disected_input = user_input.lower().split(",")
    command =  disected_input[0].strip(' ') if len(disected_input) > 1 else user_input.lower().strip(' ')
    name = disected_input[1].strip(' ') if len(disected_input) > 1 else None
    phone_number = disected_input[2].strip(' ') if len(disected_input) > 2 else None
    return {"command": command, "name": name, "phone_number": phone_number}

def command_error(func):
    def inner(user_input):
        try:
            return func(user_input)
        except KeyError:
            return 'Unknown command, type "help" to see the list of commands'
    return inner

def add(user_input):
    name = user_input["name"]
    phone_number = user_input["phone_number"]
    if not name:
        return "Name invalid"
    if not phone_number:
        return "Phone number invalid"
    if name in phonebook.keys():
        return "A contact with this name already exists"
    phonebook[name] = phone_number
    return f"Contact added: {name.capitalize()}: {phone_number}"

def change(user_input):
    name = user_input["name"]
    phone_number = user_input["phone_number"]
    if not name:
        return "Name invalid"
    if not phone_number:
        return "Phone number invalid"
    result = 'Contact not found'
    if name in phonebook.keys():
        phonebook[name] = phone_number
        result = f"Contact changed to {name.capitalize()}: {phone_number}"
    return result

def show_contact(user_input):
    ref_name = user_input["name"]
    result = 'Contact not found'
    if not ref_name:
        result = "Name invalid"
        return result
    if ref_name in phonebook.keys():
        result = f"{ref_name.capitalize()}: {phonebook[ref_name]}"  
    return result

def show_all(user_input):
    result = ""
    for name, phone_number in phonebook.items():
        result += f"{name.capitalize()}: {phone_number}\n"
    if result == "":
        result = "Seems like your list of contacts is empty. Try adding some"      
    return result

# def handler(user_input):
#     command = user_input["command"]
#     functions = {
#                 "hello": greeting,
#                 "help": help,
#                 "add": add,
#                 "change": change,
#                 "phone": show_contact,
#                 "show all": show_all
#             }
#     if command in ("goodbye", "close", "exit"):
#         result = "Goodbye!"
#     elif command in functions.keys():
#             result = functions[command](user_input)
#     else:
#         result = 'Unknown command, type "help" to see the list of commands'  
#     return result

@command_error
def handler(user_input):
    command = user_input["command"]
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
    else: result = functions[command](user_input) 
    return result
    


def main():
    print("Greetings, user! Phonebook manager online")
    while True:
        user_input = parcer(input('Enter a command: \n>>> '))
        result = handler(user_input) 
        print(result)  
        if result == "Goodbye!":
            break
        elif result == 'Unknown command, type "help" to see the list of commands':
            continue

main()