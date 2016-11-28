# Al-Islam.org Parser
A python script to parse data from Al-Islam.org's books.

---
By: Ali Mir

Created: November 27, 2016

Pull requests are always appreciated :)

---

## Usage

### Get Book Metadata: get_a_book_metadata(url)
Returns a book object containing description, tags, categories, etc.

Example: 

```python
import parseAlIslam

tabatabai_book = get_a_book_metadata("https://www.al-islam.org/a-shiite-anthology-muhammad-husayn-tabatabai")
print tabatabai_book.title # A Shi'ite Anthology
```

### Get All Books Metadata: get_all_book_metaData()
Returns a list of book objects.

Link for entire books collection: http://al-islam.org/print/book/export/html/

### Download an Ebook: download_ebook(url)
Downloads ebook of the Al-Islam.org book url.

Ebook name: title of the book

Ebook format: epub

Example:

```python
import parseAlIslam

download_ebook("https://www.al-islam.org/ethical-discourses-vol2-makarim-shirazi")
# file downloaded as: Ethical Discourses: Volume 2.epub
```

### Download All Ebooks: download_all_ebooks()
Downloads entire ebook collection from Al-Islam.org!
