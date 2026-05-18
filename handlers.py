from main import AddressBook, Record


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Value error: {str(e)}"
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid number of arguments."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return inner


@input_error
def add_contact(args, book: AddressBook):
    """
    Додати новий контакт або оновити існуючий
    Формат: add [ім'я] [телефон]
    """
    if len(args) < 2:
        raise ValueError("Please provide name and phone number")
    
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    
    if phone:
        record.add_phone(phone)
    
    return message


@input_error
def change_contact(args, book: AddressBook):
    """
    Змінити телефонний номер контакту
    Формат: change [ім'я] [старий телефон] [новий телефон]
    """
    if len(args) < 3:
        raise ValueError("Please provide name, old phone, and new phone")
    
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    """
    Показати телефонні номери контакту
    Формат: phone [ім'я]
    """
    if len(args) < 1:
        raise ValueError("Please provide contact name")
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    if not record.phones:
        return f"Contact '{name}' has no phone numbers"
    
    phones = "; ".join(phone.value for phone in record.phones)
    return f"{name}: {phones}"


@input_error
def show_all(book: AddressBook):
    """
    Показати всі контакти в адресній книзі
    """
    if not book.data:
        return "Address book is empty"
    
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    """
    Додати день народження контакту
    Формат: add-birthday [ім'я] [дата народження DD.MM.YYYY]
    """
    if len(args) < 2:
        raise ValueError("Please provide name and birthday in DD.MM.YYYY format")
    
    name, birthday, *_ = args
    record = book.find(name)
    
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    record.add_birthday(birthday)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book: AddressBook):
    """
    Показати день народження контакту
    Формат: show-birthday [ім'я]
    """
    if len(args) < 1:
        raise ValueError("Please provide contact name")
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    if record.birthday is None:
        return f"Contact '{name}' has no birthday"
    
    return f"{name}'s birthday: {record.birthday}"


@input_error
def show_birthdays(book: AddressBook):
    """
    Показати дні народження на наступному тижні
    """
    upcoming = book.get_upcoming_birthdays()
    
    if not upcoming:
        return "No birthdays in the next week"
    
    result = "Upcoming birthdays:\n"
    for person in upcoming:
        result += f"{person['name']}: {person['birthday']} (congratulate on {person['congratulation_date']})\n"
    
    return result.strip()