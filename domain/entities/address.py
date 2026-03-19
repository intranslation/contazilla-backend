class Address:
    def __init__(self, id, street, zip_code, city, state, country, client_id=None, company_id=None):
        self.id = id
        self.street = street
        self.zip_code = zip_code
        self.city = city
        self.state = state
        self.country = country
        self.client_id = client_id
        self.company_id = company_id
