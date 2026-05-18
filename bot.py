from main import AddressBook
from handlers import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    show_birthdays
)


def parse_input(user_input: str):
    """
    Розпарсити введені користувачем дані
    Повертає команду та список аргументів
    """
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return command, args


def main():
    """Основна функція бота"""
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Type 'hello' for help or 'close'/'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("Enter a command: ").strip()
            
            if not user_input:
                continue
            
            command, args = parse_input(user_input)
            
            # Команди для закриття програми
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            
            # Команда привітання
            elif command == "hello":
                print("How can I help you?")
                print("Available commands:")
                print("  add [name] [phone] - Add new contact or phone to existing")
                print("  change [name] [old_phone] [new_phone] - Change phone number")
                print("  phone [name] - Show phone numbers for contact")
                print("  all - Show all contacts")
                print("  add-birthday [name] [DD.MM.YYYY] - Add birthday")
                print("  show-birthday [name] - Show contact's birthday")
                print("  birthdays - Show upcoming birthdays (next 7 days)")
                print("  close/exit - Exit the bot\n")
            
            # Команда додавання контакту
            elif command == "add":
                print(add_contact(args, book))
            
            # Команда зміни телефону
            elif command == "change":
                print(change_contact(args, book))
            
            # Команда показу телефону
            elif command == "phone":
                print(show_phone(args, book))
            
            # Команда показу всіх контактів
            elif command == "all":
                print(show_all(book))
            
            # Команда додавання дня народження
            elif command == "add-birthday":
                print(add_birthday(args, book))
            
            # Команда показу дня народження
            elif command == "show-birthday":
                print(show_birthday(args, book))
            
            # Команда показу днів народження на наступному тижні
            elif command == "birthdays":
                print(show_birthdays(book))
            
            # Невідома команда
            else:
                print("Invalid command. Type 'hello' for help.")
        
        except KeyboardInterrupt:
            print("\nGood bye!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()