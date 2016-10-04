import csv
import random
## NEEDED COMMENTS HERE PER TOOL
needed = 500
#prefix = 'random_'
prefix = 'debug_'
tools_comment_count = {}
data = {}

with open('all_merged.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        tool_name = row[1]
        comment = row[0]
        if tool_name not in tools_comment_count:
            tools_comment_count[tool_name] = 0
            data[tool_name] = []
        if tools_comment_count[tool_name] < needed:
            data[tool_name].append(comment)
            tools_comment_count[tool_name] += 1
        else:
            # 50% probability that I will replace existing data
            if random.random() > 0.5:
                random_index = random.randrange(0, needed)
                # Already required count is there, randomly get index.
                data[tool_name][random_index] = comment

output_data = []
for tool_name in data:
    for comment in data[tool_name]:
        output_data.append([comment, tool_name])

with open(prefix + str(needed*len(data)) + '.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(output_data)