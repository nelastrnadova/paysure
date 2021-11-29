import re


class XML:
    def __init__(self, xml: str):
        self.xml = xml

    def get_from_xml(self, element: str) -> str:  # TODO: doesnt always return str
        request_amount_match: float = re.match(rf".*<{element}>(.*)<\/{element}>", self.xml)
        if request_amount_match:
            request_amount_groups: tuple = request_amount_match.groups()
            if len(request_amount_groups):
                return request_amount_groups[0]
        return None
