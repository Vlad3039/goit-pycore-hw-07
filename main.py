from collections import UserDict
from datetime import datetime, timedelta
import re


class Field:
    """Базовий клас для всіх полів контакту"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту"""
    pass


class Phone(Field):
    """Клас для зберігання телефонного номера з валідацією"""
    def __init__(self, value):
        # Перевіряємо, що телефон складається з 10 цифр
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)


class Birthday(Field):
    """Клас для зберігання дня народження з валідацією формату DD.MM.YYYY"""
    def __init__(self, value):
        try:
            # Перетворюємо рядок на об'єкт datetime у форматі DD.MM.YYYY
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Клас для зберігання інформації про контакт"""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        """Додати телефонний номер до контакту"""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """Видалити телефонний номер з контакту"""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str):
        """Змінити існуючий телефонний номер"""
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone: str):
        """Знайти телефонний номер у контакті"""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str):
        """Додати день народження до контакту"""
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, Phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    """Клас для управління колекцією контактів"""
    
    def add_record(self, record: Record):
        """Додати запис (контакт) до адресної книги"""
        self.data[record.name.value] = record

    def find(self, name: str):
        """Знайти контакт за іменем"""
        return self.data.get(name)

    def delete(self, name: str):
        """Видалити контакт за іменем"""
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        """
        Повертає список контактів, які мають дні народження 
        протягом наступних 7 днів
        """
        upcoming_birthdays = []
        today = datetime.today().date()
        
        for record in self.data.values():
            if record.birthday:
                # Отримуємо дату народження цього року
                # record.birthday.value - це об'єкт datetime.date
                birthday_value = record.birthday.value
                birthday_this_year = birthday_value.replace(year=today.year)
                
                # Якщо день народження вже минув цього року, беремо наступний рік
                if birthday_this_year < today:
                    birthday_this_year = birthday_value.replace(year=today.year + 1)
                
                # Перевіряємо, чи день народження на наступному тижні
                days_until_birthday = (birthday_this_year - today).days
                
                if 0 <= days_until_birthday <= 7:
                    # Якщо день народження на вихідні, привітаємо в понеділок
                    congratulation_date = birthday_this_year
                    if congratulation_date.weekday() == 5:  # Субота
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:  # Неділя
                        congratulation_date += timedelta(days=1)
                    
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime("%d.%m.%Y"),
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        
        return upcoming_birthdays

    def __str__(self):
        if not self.data:
            return "Address book is empty"
        return "\n".join(str(record) for record in self.data.values())