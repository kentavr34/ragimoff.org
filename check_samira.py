import re
t = open('samira.html', encoding='utf-8').read()
head = t[:t.find('</head>')] if '</head>' in t else t[:4000]
print('Has refresh:', bool(re.search(r'http-equiv=["\']refresh["\']', head, re.I)))
print('Has noindex:', bool(re.search(r'<meta[^>]+noindex', head, re.I)))
print('Head length:', len(head))