# SEIR-Course
## ASSIGNMENT 01
### Web Page Analysis & Simhash

#### Problem Statement

1. Write a Python program that takes a URL from the command line and outputs:
   * Page Title (without HTML tags)
   * Page Body (plain text)
   * All URLs the page links to
     
2. Extend the program to:
   * Count word frequency in the page body (case-insensitive, alphanumeric words)
   * Implement a 64-bit polynomial rolling hash for words (`p = 53`, `m = 2⁶⁴`)
   * Compute Simhash for a document
   * Take two URLs as input and print how many bits are common in their simhashes

---

## How I Solved It

* Fetched webpages using HTTP requests with a User-Agent.
* Parsed HTML using BeautifulSoup and removed script/style tags.
* Extracted page title, body text, and all links.
* Counted word frequencies from the body text.
* Implemented polynomial rolling hash using ASCII values of characters.
* Computed 64-bit Simhash using weighted bit vectors.
* Compared simhashes of two URLs using XOR to find common bits.

---
