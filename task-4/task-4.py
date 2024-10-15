class OldLogger:
    def log(self, message):
        print(f"OldLogger: {message}")

class NewLogger:
    def write_log(self, message):
        print(f"NewLogger: {message}")

class LoggerAdapter:
    def __init__(self, new_logger):
        self._new_logger = new_logger
    
    def log(self, message):
        self._new_logger.write_log(message)

if __name__ == "__main__":
    old_logger = OldLogger()
    old_logger.log("Повідомлення через OldLogger")

    new_logger = NewLogger()
    adapter = LoggerAdapter(new_logger)
    adapter.log("Повідомлення через NewLogger")