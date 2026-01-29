import json

string_with_json = '{"name": "Александр", "age": 30, "is_student": false}'
parsed_json_data = json.loads(string_with_json)

print(parsed_json_data, type(parsed_json_data))

json_dict = {
    'name': 'Алексей',
    "age": 12,
    "is_student": True,
    "test_null": None
}
json_string = json.dumps(json_dict, indent=2, ensure_ascii=False)
print(json_string, type(json_string))

with open("json_example.json", "r", encoding="utf-8") as f:
    data_of_file = json.load(f)
    print(data_of_file, type(data_of_file))

with open("test_write_in_file.json", "w", encoding="utf-8") as f:
    json.dump(json_dict, f, indent=2, ensure_ascii=False)
