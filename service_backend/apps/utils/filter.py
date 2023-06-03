class Filter:
    def __init__(self):
        self.keywords = []
        self.parse()

    def parse(self, path="keyword"):
        try:
            f = open(path, 'r', encoding='utf-8')
        except Exception as e:
            return
        for keyword in f:
            self.keywords.append(keyword.strip())

    def has_sensitive_word(self, message):
        for kw in self.keywords:
            if kw in message:
                return True
        return False

    # def filter(self, message, replace="*"):
    #     for kw in self.keywords:
    #         message = message.replace(kw, replace * len(kw))
    #     return message
