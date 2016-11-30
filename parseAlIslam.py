from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen, urlretrieve

featured_categories_class_name = "field field-name-field-featured-category field-type-taxonomy-term-reference field-label-inline clearfix"
authors_class_name = "field field-name-field-author field-type-taxonomy-term-reference field-label-inline clearfix"
publishers_class_name = "field field-name-field-publisher field-type-taxonomy-term-reference field-label-inline clearfix"
translators_class_name = "field field-name-field-translator field-type-taxonomy-term-reference field-label-inline clearfix"
categories_class_name = "field field-name-field-category field-type-taxonomy-term-reference field-label-inline clearfix"
tags_class_name = "field field-name-field-tags field-type-taxonomy-term-reference field-label-inline clearfix"
description_section_class_name = "field field-name-body field-type-text-with-summary field-label-hidden"
miscellaneous_information_section_class_name = "field field-name-field-misc-info field-type-text-long field-label-inline clearfix"

class Book(object):
    def __init__(self, title, authors, publishers, translators, description, tags, categories, featured_categories, related_books, miscellaneous_information, unique_book_title_string):
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
        self.unique_book_title_string = unique_book_title_string

def make_soup(url):
    html = urlopen(url).read()
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
        newTitle = cleanString(' '.join(title.string.split()))
        return newTitle

def get_related_books(soup):
    section = soup.find("div", "region region-sidebar-second")
    if section:
        related_section = section.find("section", "block block-views clearfix")
        if related_section:
            related_sources = section.find("div", "view-content")
            if related_sources:
                related_books = [cleanString(' '.join(a.string.split())) for a in related_sources.findAll("span", "field-content")]
                if related_books:
                    return related_books

def get_parsed_items(soup, section_class_name):
    section = soup.find("div", section_class_name)
    if section:
        items = section.find("div", "field-items")
        if items:
            listOfItems = [cleanString(' '.join(a.string.split())) for a in items.findAll("div")]
            if listOfItems:
                return listOfItems

def get_description(soup):
    description_section = soup.find("div", description_section_class_name)
    if description_section:
        description = description_section.find("p")
        if description:
            return description.string
    else:
        return ""

def get_miscellaneous_information(soup):
    miscellaneous_information_section = soup.find("div", miscellaneous_information_section_class_name)
    if miscellaneous_information_section:
        miscellaneous_information = miscellaneous_information_section.find("div", "field-items")
        if miscellaneous_information:
            return miscellaneous_information.string
    else:
        return ""

def get_a_book_metadata(book_url, need_to_download_ebook):
    if "articles" not in book_url:
        soup = make_soup(book_url)
        if is_a_book(soup):
            title = get_book_title(soup)
            featured_categories = get_parsed_items(soup, featured_categories_class_name)
            authors = get_parsed_items(soup, authors_class_name)
            publishers = get_parsed_items(soup, publishers_class_name)
            translators = get_parsed_items(soup, translators_class_name)
            categories = get_parsed_items(soup, categories_class_name)
            tags = get_parsed_items(soup, tags_class_name)
            related_books = get_related_books(soup)
            description = get_description(soup)
            miscellaneous_information = get_miscellaneous_information(soup)
            unique_book_title_string = create_unique_title(title, authors, publishers, translators)
            if need_to_download_ebook:
                download_ebook(soup, unique_book_title_string)
            return Book(title, authors, publishers, translators, description, tags, categories, featured_categories, related_books, miscellaneous_information, unique_book_title_string)

def get_all_book_metaData():
    books = get_all_book_urls()
    ebook_metadatas = [get_a_book_metadata(book) for book in books]
    return ebook_metadatas

def download_ebook(soup, unique_book_string):
    ebook_title = unique_book_string
    ebook_url = soup.find("span", "print_epub").a["href"]
    urlretrieve(ebook_url, ebook_title + ".epub")

# Unique string for saving epub or other al-Islam files
def create_unique_title(title, authors, publishers, translators):
    title = title
    if authors:
        return refineStringFileNaming(title + authors[0]).replace("?", "")
    elif publishers:
        return refineStringFileNaming(title + publishers[0]).replace("?", "")
    elif translators:
        return refineStringFileNaming(title + translators[0]).replace("?", "")
    else:
        return title.replace("?", "")

def get_all_book_urls():
        soup = make_soup("https://www.al-islam.org/print/book/export/html")
        url_list = soup.find("div", "item-list")
        all_books_urls = [dd.a["href"] for dd in url_list.findAll("li")]
        return all_books_urls

# Removes special characters (for FIREBASE)
# https://www.firebase.com/docs/web/guide/understanding-data.html#section-creating-references
#A child node's key cannot be longer than 768 bytes,
#nor deeper than 32 levels. It can include any unicode characters except for
#. $ # [ ] / and ASCII control characters 0-31 and 127.
def cleanString(string):
    newString = string
    newString = newString.replace(".", "")
    newString = newString.replace("[", "")
    newString = newString.replace("]", "")
    newString = newString.replace("#", "")
    newString = newString.replace("$", "")
    newString = newString.replace("/", "")
    return newString

# To name file of the ebook.
# Cannot use / > < | : &
# Reference: https://www.cyberciti.biz/faq/linuxunix-rules-for-naming-file-and-directory-names/
def refineStringFileNaming(unique_string):
    newString = unique_string
    newString = newString.replace("/", "")
    newString = newString.replace(">", "")
    newString = newString.replace("<", "")
    newString = newString.replace("|", "")
    newString = newString.replace(":", "")
    newString = newString.replace("&", "")
    newString = newString.replace(" ", "") # removes all spaces
    return newString
