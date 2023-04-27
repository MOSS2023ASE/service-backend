class Filter:
    def __init__(self):
        self.keywords = []
        self.parse()

    def parse(self, path="keyword"):
        try:
            f = open(path)
        except Exception as e:
            return
        for keyword in f:
            self.keywords.append(keyword.strip())

    def filter(self, message, replace="*"):
        for kw in self.keywords:
            message = message.replace(kw, replace * len(kw))
        return message
