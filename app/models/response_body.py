class ResponseBody:
    def __init__(self, status, message, body):
        self.status = status
        self.message = str(message)
        self.body = body

    def serialize(self):
        return {
            "status": self.status,
            "message": self.message,
            "body": self.body
        }
