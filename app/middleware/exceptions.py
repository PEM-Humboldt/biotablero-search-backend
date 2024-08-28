class CollectionNotFoundError(Exception):
    def __init__(self, collection_url: str):
        self.collection_url = collection_url


class ItemsNotFoundError(Exception):
    def __init__(self, items_url: str):
        self.items_url = items_url


class NoFeaturesError(Exception):
    def __init__(self, items_url: str):
        self.items_url = items_url


class HTTPRequestError(Exception):
    def __init__(self, url: str):
        self.url = url


class BBoxValidationError(Exception):
    def __init__(self, bbox: list, message: str = "Invalid bbox"):
        self.bbox = bbox
        self.message = message
        super().__init__(self.message)


class CustomValidationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
