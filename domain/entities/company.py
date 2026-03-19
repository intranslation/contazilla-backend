class Company:
    def __init__(self, id, name, cnpj, client_id, user_id, address=None):
        if not cnpj:
            raise ValueError("CNPJ is required")
        if not name:
            raise ValueError("Name is required")

        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.client_id = client_id
        self.user_id = user_id
        self.address = address
