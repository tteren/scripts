import xml.etree.ElementTree as ET
import glob
import os

def load_xml(file_path):
    tree = ET.parse(file_path)
    return tree, tree.getroot()

def save_xml(tree, file_path):
    ET.indent(tree, space="  ", level=0)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

def add_tag(root, parent_tag, new_tag, attributes):
    parent = root.find(parent_tag)
    if parent is not None:
        new_element = ET.Element(new_tag, attributes)
        parent.append(new_element)
        print(f"Added tag <{new_tag}> under <{parent_tag}>")
    else:
        print(f"Parent tag <{parent_tag}> not found")

def remove_tag(root, tag_path, attribute_name=None, attribute_value=None):
    parent_path, tag_to_remove = tag_path.rsplit('/', 1)
    parent = root.find(parent_path)
    if parent is not None:
        for element in parent.findall(tag_to_remove):
            if attribute_name and attribute_value:
                if element.get(attribute_name) == attribute_value:
                    parent.remove(element)
                    print(f"Removed tag <{tag_to_remove}> with {attribute_name}='{attribute_value}' from <{parent_path}>")
            else:
                parent.remove(element)
                print(f"Removed tag <{tag_to_remove}> from <{parent_path}>")
    else:
        print(f"Tag path <{tag_path}> not found")

def add_attribute(root, tag_path, attribute_name, attribute_value):
    element = root.find(tag_path)
    if element is not None:
        element.set(attribute_name, attribute_value)
        print(f"Added attribute {attribute_name}='{attribute_value}' to <{tag_path}>")
    else:
        print(f"Tag <{tag_path}> not found")

def update_attribute(root, tag_path, attribute_name, attribute_value):
    element = root.find(tag_path)
    if element is not None:
        if attribute_name in element.attrib:
            element.set(attribute_name, attribute_value)
            print(f"Updated attribute {attribute_name}='{attribute_value}' in <{tag_path}>")
        else:
            print(f"Attribute {attribute_name} not found in <{tag_path}>")
    else:
        print(f"Tag <{tag_path}> not found")

def remove_attribute(root, tag_path, attribute_name):
    element = root.find(tag_path)
    if element is not None:
        if attribute_name in element.attrib:
            del element.attrib[attribute_name]
            print(f"Removed attribute {attribute_name} from <{tag_path}>")
        else:
            print(f"Attribute {attribute_name} not found in <{tag_path}>")
    else:
        print(f"Tag <{tag_path}> not found")

def process_xml_files(file_paths):
    for file_path in file_paths:
        print(f"Processing file: {file_path}")
        tree, root = load_xml(file_path)

        # Example operations
        add_tag(root, './/Service/Engine/Host', 'Context', {'path': '/myapp', 'docBase': 'myapp'})
        # remove_tag(root, './/Service/Engine/Host/Valve', 'className', 'org.apache.catalina.valves.AccessLogValve')
        # add_attribute(root, './/Service', 'newAttribute', 'newValue')
        # update_attribute(root, './/Service', 'surname', 'updatedSurname')
        # remove_attribute(root, './/Service', 'newAttribute')

        save_xml(tree, file_path)

if __name__ == "__main__":
    base_path = 'C:/ApacheTomcat/servers'
    pattern = '**/conf/server.xml'
    xml_file_paths = glob.glob(os.path.join(base_path, pattern), recursive=True)

    process_xml_files(xml_file_paths)