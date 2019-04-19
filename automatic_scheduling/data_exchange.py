## -*- coding: utf-8 -*-

import csv
import json
from schedule.config import config, ExchangeFormat


class Exchanger:

    @staticmethod
    def import_data(exchange_format: ExchangeFormat) -> dict:
        """ Import data from CSV/MongoDB/JSON """
        # ToDO import from MongoDB
        data = {'lessons': [], 'days': [], 'time_slots': [], 'auditoriums': [], 'student_groups': []}

        if exchange_format is ExchangeFormat.CSV:
            for filename in ['lessons', 'days', 'time_slots', 'auditoriums', 'student_groups']:
                csv_path = f"{config['import_csv_path']}{filename}.csv"
                with open(csv_path, "r", encoding="utf-8") as input_file:
                    reader = csv.reader(input_file)
                    for row in reader:
                        data[filename].append(row)

        if exchange_format is ExchangeFormat.DB:
            pass

        if exchange_format is ExchangeFormat.JSON:
            with open(config['import_json_path'], "r", encoding="utf-8") as input_file:
                data = json.load(input_file)

        return data

    @staticmethod
    def export_data(data: list, exchange_format: ExchangeFormat) -> None:
        """ Export data to CSV/MongoDB/JSON """
        # ToDO export to MongoDB
        if exchange_format is ExchangeFormat.CSV:
            with open(config['export_csv_path'], "w", encoding="utf-8") as output_file:
                writer = csv.writer(output_file)
                for row in data:
                     writer.writerow(row.values())

        if exchange_format is ExchangeFormat.DB:
            pass

        if exchange_format is ExchangeFormat.JSON:
            with open(config['export_json_path'], "w", encoding="utf-8") as output_file:
                json.dump(data, output_file, ensure_ascii=False)

    @staticmethod
    def csv_to_json():
        """ Transform input CSV to JSON """
        data = {'lessons': [], 'days': [], 'time_slots': [], 'auditoriums': [], 'student_groups': []}

        for filename in ['lessons', 'days', 'time_slots', 'auditoriums', 'student_groups']:
            csv_path = f"{config['import_csv_path']}{filename}.csv"
            json_path = config['import_json_path']
            with open(csv_path, "r", encoding="utf-8") as input_file:
                reader = csv.reader(input_file)
                for row in reader:
                    data[filename].append(row)
            with open(json_path, "w", encoding="utf-8") as output_file:
                json.dump(data, output_file, ensure_ascii=False)
