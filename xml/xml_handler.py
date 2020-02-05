import xml.sax

class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data=""
        self.model=""
        self.speed=""

    def startElement(self, tag, attribut):
        self.current_data=tag
        if tag == "car":
            print('---car---')
            name=attribut["name"]
            print("name", name)

    def endElement(self, tag):
        if self.current_data=='model':
            print('model', self.model)
        elif self.current_data=='speed':
            print('speed :', self.speed)
        self.current_data=""

    def characters(self, content):
        if self.current_data=="model":
            self.model=content
        elif self.current_data=='speed':
            self.speed=content


if __name__ == '__main__':
    parser=xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    handler=XMLHandler()
    parser.setContentHandler(handler)
    parser.parse('example.xml')