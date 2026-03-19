from datetime import datetime


class Asset:
    def __init__(
        self,
        id,
        filename,
        client_id,
        user_id,
        size=None,
        was_viewed=False,
        was_downloaded=False,
        created_at=None,
        updated_at=None,
    ):
        self.id = id
        self.filename = filename
        self.client_id = client_id
        self.user_id = user_id
        self.size = size
        self.was_viewed = was_viewed
        self.was_downloaded = was_downloaded
        self.created_at: None | datetime = created_at
        self.updated_at: None | datetime = updated_at
