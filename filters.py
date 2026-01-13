class IgnoreSpam:
    def filter(self, record):
        msg = record.getMessage();
        if "wodomierz/" in msg:
            return False
        elif("plan/" in msg):
            return False;
        return True;

