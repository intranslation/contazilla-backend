class User:
    def __init__(self, email, name, phone, password):
        if "@" not in email:
            raise ValueError("E-mail is missing @")

        self.email = email
        self.name = name
        self.phone = phone
        self.password = password
