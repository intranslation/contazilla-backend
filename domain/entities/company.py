class Company:
    def __init__(self, id, name, address, cnpj, client_id, user_id):
        if not cnpj:
            raise ValueError("CNPJ is required")
        if not name:
            raise ValueError("Name is required")
        if not address:
            raise ValueError("Address is required")

        self.id = id
        self.name = name
        self.address = address
        self.cnpj = cnpj
        self.client_id = client_id
        self.user_id = user_id
