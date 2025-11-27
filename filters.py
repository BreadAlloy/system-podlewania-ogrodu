class IgnoreSpam:
    def filter(self, record):
        if "wodomierz/" in record.getMessage():
            return False
        else:
            return True

