class OldLogger:
    def log(self, message: str):
        print(f"OldLogger: {message}")

class NewLogger:
    def write_log(self, msg: str):
        print(f"NewLogger: {msg}")

class LoggerAdapter:
    def __init__(self, logger):
        self._logger = logger

    def log(self, message: str):

        if hasattr(self._logger, 'write_log'):
            self._logger.write_log(message)
        elif hasattr(self._logger, 'log'):
            self._logger.log(message)
        else:
            print("Логер не підтримує методів log або write_log.")

if __name__ == "__main__":
    new_logger = NewLogger()
    adapter = LoggerAdapter(new_logger)
    adapter.log("Повідомлення через адаптер (NewLogger)")

    old_logger = OldLogger()
    adapter = LoggerAdapter(old_logger)
    adapter.log("Повідомлення через адаптер (OldLogger)")
