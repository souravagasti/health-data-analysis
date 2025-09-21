def parse_xml(file_path: str):
    """Parse export.xml and return ElementTree root."""
    import xml.etree.ElementTree as ET
    tree = ET.parse(file_path)
    return tree.getroot()
