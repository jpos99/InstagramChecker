from os.path import exists


class RecordCsv:
    def __init__(self, path_to_filename):
        self.csv_file_name = path_to_filename

    def record_csv(self, log):
        report = RecordCsv.open_csv(self)
        report.write(log)
        report.close()

    def open_csv(self):
        if not exists(self.csv_file_name):
            arquivo_csv_to_record = open(self.csv_file_name, 'w')
            return arquivo_csv_to_record
        arquivo_csv_to_record = open(self.csv_file_name, 'a')
        return arquivo_csv_to_record
