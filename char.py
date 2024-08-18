
import xml.etree.ElementTree as ET

tree = ET.parse("char_11001.plist")

root = tree.getroot()
for child in root.iter():
	print(child.tag,child.text)

print("555")
for elem in root.findall("char_11001_1_1_00.png"):
	print(elem.attrib)

print(666)
