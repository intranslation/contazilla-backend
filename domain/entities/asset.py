class Asset:
    def __init__(self, id, filename, url, client_id, user_id):
        if not url:
            raise ValueError("URL is required")

        self.id = id
        self.filename = filename
        self.url = url
        self.client_id = client_id
        self.user_id = user_id
