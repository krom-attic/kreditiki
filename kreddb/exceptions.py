class CsvUploadException(Exception):
    def __init__(self, field, *args, **kwargs):
        self.field = field
        super().__init__(*args, **kwargs)
