import os
import logging
import datetime
import time
import zipfile

class LoggingError(Exception):
    """Власний клас для обробки помилок у логуванні"""
    pass

class Logger:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        self.current_log_file = None
        self.logger = logging.getLogger('custom_logger')
        self.logger.setLevel(logging.DEBUG)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self._set_log_file()

    def _set_log_file(self):
        try:
            today = datetime.date.today().strftime('%Y-%m-%d')
            self.current_log_file = os.path.join(self.log_dir, f'{today}.log')

            file_handler = logging.FileHandler(self.current_log_file, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            if self.logger.hasHandlers():
                self.logger.handlers.clear()

            self.logger.addHandler(file_handler)
        except Exception as e:
            raise LoggingError(f'Помилка під час створення лог-файлу: {e}')

    def _check_log_file(self):
        """Метод для перевірки та зміни лог-файлу при зміні дати"""
        today = datetime.date.today().strftime('%Y-%m-%d')
        log_file_name = f'{today}.log'
        if not self.current_log_file.endswith(log_file_name):
            self._set_log_file()

    def info(self, message):
        self._check_log_file()
        try:
            self.logger.info(message)
        except Exception as e:
            raise LoggingError(f'Помилка під час запису логу: {e}')

    def warning(self, message):
        self._check_log_file()
        try:
            self.logger.warning(message)
        except Exception as e:
            raise LoggingError(f'Помилка під час запису логу: {e}')

    def error(self, message):
        self._check_log_file()
        try:
            self.logger.error(message)
        except Exception as e:
            raise LoggingError(f'Помилка під час запису логу: {e}')

    def critical(self, message):
        self._check_log_file()
        try:
            self.logger.critical(message)
        except Exception as e:
            raise LoggingError(f'Помилка під час запису логу: {e}')

    def archive_logs(self, archive_name='logs_archive.zip'):
        """Метод для архівації старих лог-файлів"""
        try:
            archive_path = os.path.join(self.log_dir, archive_name)

            with zipfile.ZipFile(archive_path, 'w') as archive:
                for file_name in os.listdir(self.log_dir):
                    file_path = os.path.join(self.log_dir, file_name)
                    if file_name.endswith('.log') and file_name != os.path.basename(self.current_log_file):
                        archive.write(file_path, arcname=file_name)
                        os.remove(file_path)
            print(f'Логи успішно архівовані у файл {archive_name}')
        except Exception as e:
            raise LoggingError(f'Помилка під час архівації лог-файлів: {e}')

    def run(self):
        """Основний цикл для постійного логування з відслідковуванням часу та різних рівнів"""
        try:
            counter = 0
            while True:
                # Інформаційне повідомлення кожні 10 секунд
                self.info("Це інформаційне повідомлення.")
                
                # Попередження кожні 30 секунд
                if counter % 3 == 0:
                    self.warning("Це попередження.")
                
                # Помилка кожні 60 секунд
                if counter % 6 == 0:
                    self.error("Це повідомлення про помилку.")
                
                # Критична помилка кожні 120 секунд
                if counter % 12 == 0:
                    self.critical("Це критична помилка.")

                counter += 1
                time.sleep(10)  # Пауза на 10 секунд
        except KeyboardInterrupt:
            print("Логування зупинено користувачем.")


# Приклад використання
logger = Logger()

# Запуск циклу логування
logger.run()
