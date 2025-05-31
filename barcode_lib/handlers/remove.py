from barcode_lib.handlers.base import ModeBase

class RemoveMode(ModeBase):
    def __init__(self, reader):
        self.reader = reader

    def process_code(self, code: str):
        print(f"[RemoveMode] Processed code: {code}")
