import csv
from Util import util

# Return rows of a CSV. Will convert numerical strings to floats
def get_csv(fp, skipHeaders=0, get_range=None):
    with open(fp) as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')

        # Skip n rows without logic
        for i in range(skipHeaders):
            next(reader, None)  # skip the headers

        if skipHeaders: # Perform an additional check to ensure all headers skipped
            data = []
            for row in reader:
                row = util.array_safe_str_to_float(row) # Convert row to floats

                if "#" in row[0]: # Skip comment rows
                    continue
                if not get_range:
                    data.append(row)
                else:
                    data.append(row[get_range[0]:get_range[1]])
            return data
        else:
            return [util.array_safe_str_to_float(row) for row in reader]

def write_csv(fp, data, headers=None):
    with open(fp, "wt", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        if headers:
            writer.writerow(headers)
        writer.writerows(data)