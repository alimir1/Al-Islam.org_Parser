from bs4 import BeautifulSoup
import urllib

class Book(object):
    def __init__(self, title, authors, publishers, translators, description, tags, categories, featured_categories, related_books, miscellaneous_information):
        self.title = title
        self.authors = authors
        self.publishers = publishers
        self.translators = translators
        self.description = description
        self.tags = tags
        self.categories = categories
        self.related_books = related_books
        self.miscellaneous_information = miscellaneous_information
        self.featured_categories = featured_categories

def make_soup(url):
    html = urllib.urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def is_a_book(soup):
    print_content_region = soup.find("span", "print-content-region")
    if print_content_region:
        return True
    else:
        return False

def get_book_title(soup):
    title = soup.find("h1", "page-header")
    if title:
        return title.string
    else:
        return ""

def get_related_books(soup):
    section = soup.find("div", "region region-sidebar-second")
    if section:
        related_section = section.find("section", "block block-views clearfix")
        if related_section:
            related_sources = section.find("div", "view-content")
            if related_sources:
                related_books = [a.string for a in related_sources.findAll("span", "field-content")]
                if related_books:
                    return related_books
    else:
        return [""]

def get_parsed_items(soup, section_class_name):
    section = soup.find("div", section_class_name)
    if section:
        items = section.find("div", "field-items")
        if items:
            listOfItems = [a.string for a in items.findAll("div")]
            if listOfItems:
                return listOfItems
    else:
        return [""]

def get_description(soup):
    description_section = soup.find("div", "field field-name-body field-type-text-with-summary field-label-hidden")
    if description_section:
        description = description_section.find("p")
        if description:
            return description.string
    else:
        return ""

def get_miscellaneous_information(soup):
    miscellaneous_information_section = soup.find("div", "field field-name-field-misc-info field-type-text-long field-label-inline clearfix")
    if miscellaneous_information_section:
        miscellaneous_information = miscellaneous_information_section.find("div", "field-items")
        if miscellaneous_information:
            return miscellaneous_information.string
    else:
        return ""


def get_a_book_metadata(book_url):
    soup = make_soup(book_url)
    if is_a_book(soup):
        title = get_book_title(soup)
        featured_categories = get_parsed_items(soup, "field field-name-field-featured-category field-type-taxonomy-term-reference field-label-inline clearfix")
        authors = get_parsed_items(soup, "field field-name-field-author field-type-taxonomy-term-reference field-label-inline clearfix")
        publishers = get_parsed_items(soup, "field field-name-field-publisher field-type-taxonomy-term-reference field-label-inline clearfix")
        translators = get_parsed_items(soup, "field field-name-field-translator field-type-taxonomy-term-reference field-label-inline clearfix")
        categories = get_parsed_items(soup, "field field-name-field-category field-type-taxonomy-term-reference field-label-inline clearfix")
        tags = get_parsed_items(soup, "field field-name-field-tags field-type-taxonomy-term-reference field-label-inline clearfix")
        related_books = get_related_books(soup)
        description = get_description(soup)
        miscellaneous_information = get_miscellaneous_information(soup)

        return Book(title, authors, publishers, translators, description, tags, categories, featured_categories, related_books, miscellaneous_information)
    else:
        print "Not a book: %s" %(book_url)

def get_all_book_metaData():
    books = get_all_book_urls()
    ebook_metadatas = [get_a_book_metadata(book) for book in books]
    return ebook_metadatas

def download_all_ebooks():
    books = get_all_book_urls()
    all_books_urls = [download_ebook(book) for book in books]

def get_all_book_urls():
        soup = make_soup("https://www.al-islam.org/print/book/export/html")
        url_list = soup.find("div", "item-list")
        all_books_urls = [dd.a["href"] for dd in url_list.findAll("li")]
        return all_books_urls

def download_ebook(url):
    if "articles" not in url:
        soup = make_soup(url)
        if is_a_book(soup):
            ebook_url = soup.find("span", "print_epub").a["href"]
            ebook_title = get_book_title(soup)
            url_opener = urllib.URLopener()
            url_opener.retrieve(ebook_url, ebook_title + ".epub")
