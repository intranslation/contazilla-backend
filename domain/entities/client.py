class Client:
    def __init__(self, id, name, cpf, phone, user_id):
        if not cpf:
            raise ValueError("CPF is required")

        self.id = id
        self.name = name
        self.cpf = cpf
        self.phone = phone
        self.user_id = user_id
