# Logo and Contact Extractor

A command-line application that, given a list of website URLs as input, visits them
and finds, extracts and outputs the websites’ logo image URLs and all phone numbers (e.g.
mobile phones, land lines, fax numbers) present on the websites.

## Basic Usage

Given a file `websites.txt` that contains a list of websites to visit, run:

```bash
cat websites.txt | python -m extractor
```
