class User:
    def __init__(self, id, email, name, phone, password, role, is_archived=False):
        if "@" not in email:
            raise ValueError("E-mail is missing @")

        self.id = id
        self.email = email
        self.name = name
        self.phone = phone
        self.password = password
        self.role = role
        self.is_archived = is_archived
