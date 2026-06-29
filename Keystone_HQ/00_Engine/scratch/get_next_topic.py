import json

d = json.load(open('c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/learning_queue.json'))
next_topic = None
category = None

for q in d['queue']:
    if q.get('status') != 'completed':
        for t in q.get('topics', []):
            if t not in q.get('completed', []):
                next_topic = t
                category = q['domain']
                break
    if next_topic:
        break

print(f'CATEGORY: {category}')
print(f'TOPIC: {next_topic}')
