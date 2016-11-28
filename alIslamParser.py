import parseAlIslam

url = "https://www.al-islam.org/black-thursday-muhammad-al-tijani-al-samawi"
if "articles" not in url:
    book = parseAlIslam.get_book_metadata(url)
    if book:
        print book.description
else:
    print "this book is an article: %s" % (url)
