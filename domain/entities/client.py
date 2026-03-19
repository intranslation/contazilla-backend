class Client:
    def __init__(self, id, name, cpf, email, phone, user_id, address=None, is_premium=False):
        self.id = id
        self.name = name
        self.cpf = cpf
        self.email = email
        self.phone = phone
        self.user_id = user_id
        self.address = address
        self.is_premium = is_premium
