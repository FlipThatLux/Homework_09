phonebook = {}

def command_error(func):
    def inner(args):
        try:
            return func(args)
        except KeyError:
            return 'Unknown command, type "help" to see the list of commands'
        except IndexError:
            return 'Not enough arguments'
    return inner

def greeting(args):
    return "How can I help you?"

def help(args):
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
    user_input += ","
    disected_input = user_input.lower().split(",")
    disected_input.remove('')
    results = list()
    for i in disected_input:
        results.append(i.lower().strip(' '))
    return results

def add(args):
    if args[1] in phonebook.keys():
        return "A contact with this name already exists"
    phonebook[args[1]] = args[2]
    return f"Contact added: {args[1].capitalize()}: {args[2]}"

def change(args):
    if args[1] in phonebook.keys():
        phonebook[args[1]] = args[2]
        return f"Contact changed to {args[1].capitalize()}: {args[2]}"
    return 'Contact not found'

def show_contact(args):
    if args[1] in phonebook.keys():
        return f"{args[1].capitalize()}: {phonebook[args[1]]}"  
    return f"{args[1].capitalize()} not found"

def show_all(args):
    result = ""
    for name, phone_number in phonebook.items():
        result += f"{name.capitalize()}: {phone_number}\n"     
    return result

@command_error
def handler(args):
    functions = {
                "hello": greeting,
                "help": help,
                "add": add,
                "change": change,
                "phone": show_contact,
                "show all": show_all 
                }
    return functions[args[0]](args)

def main():
    print("Greetings, user! Phonebook manager online")
    while True:
        user_input = parcer(input('Enter a command: \n>>> '))
        #print(user_input)
        if user_input[0] in ("goodbye", "close", "exit"):
            print("Goodbye!")
            break
        result = handler(user_input)
        if result == "":
            result = "Seems like your list of contacts is empty. Try adding some" 
        print(result)

main()