import csv
from Util import util

# # Define data
# data = [
#     (1, "A towel,", 1.0),
#     (42, " it says, ", 2.0),
#     (1337, "is about the most ", -1),
#     (0, "massively useful thing ", 123),
#     (-2, "an interstellar hitchhiker can have.", 3),
# ]

# # Write CSV file
# with open("test.csv", "wt") as fp:
#     writer = csv.writer(fp, delimiter=",")
#     # writer.writerow(["your", "header", "foo"])  # write header
#     writer.writerows(data)

# # Read CSV file
# with open("test.csv") as fp:
#     reader = csv.reader(fp, delimiter=",", quotechar='"')
#     # next(reader, None)  # skip the headers
#     data_read = [row for row in reader]

# print(data_read)

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

                if "#" in row[0]:
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