import time
import numpy as np
import csv
import json


class Bench:
    def __init__(self):
        self.data_file = "log.csv"
        self.headers_file = "headers.csv"

    def init_files(self):
        headers_file = open(self.headers_file, 'w+')
        headers_file.close()
        data_file = open(self.data_file, 'w+')
        data_file.close()

    def write_array(self, data):

        # Store records for later use
        records = []

        # Keep track of headers in a set
        headers = set([])

        for line in data:
            # line = line.strip()

            # Parse each line as JSON
            # parsed_json = json.loads(line)
            parsed_json = line

            records.append(parsed_json)

            # Make sure all found headers are kept in the headers set
            for header in parsed_json.keys():
                headers.add(header)

        # You only know what headers were there once you have read all the JSON once.

        # Now we have all the information we need, like what all possible headers are.

        headers_file = open(self.headers_file, 'w+')
        # write headers to the file in order
        headers_file.write(",".join(sorted(headers)) + '\n')
        headers_file.close()

        out_file = open(self.data_file, 'a+')
        for record in records:
            # write each record based on available fields
            cur_line = []
            for header in sorted(headers):
                if header in record:
                    cur_line.append(record[header])
                else:
                    cur_line.append('')
            out_file.write(",".join(str(e) for e in cur_line) + '\n')
        out_file.close()

    # def write_multi(self, data):
    #     for d in data:
    #         self.write(d)


if __name__ == '__main__':
    bench = Bench()

    data = [{
        "calibratedHeading": 0,
        "gyroHeading": 0.00543
    }, {
        "calibratedHeading": 0.5,
        "gyroHeading": 0.0054355
    }]

    bench.write_array(data)




