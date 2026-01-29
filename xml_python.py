import xml.etree.ElementTree as ET

xml_data = """
<user>
    <first_name>John</first_name>
    <last_name>Jones</last_name>
    <email>john.jones@example.com</email>
</user>
"""

root = ET.fromstring(xml_data)

print(root.find('first_name').text)

print("User lastname is", root.find('last_name').text)
