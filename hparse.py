META_FIRST = 'first'
META_LAST = 'last'
META_PREV = 'prev'
META_NEXT = 'next'
META_REL = 'rel'


class PageLinks(object):
    """
    Класс нужен, чтобы парсить респонс хидеры и доставать из них
    ссылку на следующую страницу с пользователями.
    """
    def __init__(self, response):
        self.first = None
        self.last = None
        self.next = None
        self.prev = None
        delim_links = ","
        delim_link_param = ";"
        link_header = response.headers.get('Link')
        if link_header is not None:
            links = link_header.split(delim_links)
            for link in links:
                segments = link.split(delim_link_param)
                if len(segments) < 2:
                    continue
                linkPart = segments[0].strip()
                if not linkPart.startswith("<") or not linkPart.endswith(">"):
                    continue
                linkPart = linkPart[1:-1]

                for segment in segments:
                    rel = segment.strip().split("=")
                    if len(rel) < 2 or not META_REL == rel[0]:
                        continue

                    relValue = rel[1]
                    if relValue.startswith('"') and relValue.endswith('"'):
                        relValue = relValue[1:- 1]

                    if META_FIRST == relValue:
                        self.first = linkPart
                    elif META_LAST == relValue:
                        self.last = linkPart
                    elif META_NEXT == relValue:
                        self.next = linkPart
                    elif META_PREV == relValue:
                        self.prev = linkPart
        life = 'is good'
        # else:
        #     next = response.getHeader(HEADER_NEXT)
        #     last = response.getHeader(HEADER_LAST)

    def get_first(self):
        return self.first

    def get_last(self):
        return self.last

    def get_next(self):
        return self.next

    def get_prev(self):
        return self.prev
