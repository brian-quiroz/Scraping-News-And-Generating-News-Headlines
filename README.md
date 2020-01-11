# Scraping News and Generating News Headlines

Given a set of keywords, scrape search results from 6 of the largest media outlets in my country (Peru). These media outlets are owned by the same company and their websites are very similar, which simplifies the scraping process. Most, if not all, of the news will be in Spanish. I have created two programs to do two different tasks with the scraped news:

## Display the News on My Own Site
To use, run: `displayNews.py <keywords> <numPages>`, where `keywords` is the keyword or keywords to search for (in quotes) and `numPages` is the number of pages of search results in each news website to use. To view results, open the given server URL (e.g. `http://127.0.0.1:5000/`) and add `/test` (e.g. `http://127.0.0.1:5000/test`). The results will take a few seconds to display.
The program will:
1. Start a Flask server
2. Extract the news:
    * For each news website, send get request to keyword(s) search result page(s) on news website
    * For each news on the search page, scrape title (headlines) and link
    * Send get request to each linked page
    * Scrape description, date, publisher (name of news outlet), and article body
3. Sort the articles by date
4. Use render_template to display HTML and execute Javascript code from HTML template on the server
5. Send get request from JavaScript code to obtain JSON article data from Python
6. Fetch and unpack JSON data on Javascript side
7. Generate new HTML elements and display data on server

## Generate Fake News
To use, run: `generateFakeNews.py <keywords> <numPages> <numNews>`, where `keywords` is the keyword or keywords to search for (in quotes), `numPages` is the number of pages of search results in each news website to use, and `numNews` is the number of fake headlines to generate. The results will be displayed on the command line.
The program will:
1. Extract the news:
    * For each news website, send get request to keyword(s) search result page(s) on news website
    * For each news on the search page, scrape title (headlines) and link
2. Output headlines to file
3. Read file from Hidden Markov Model script
4. Train algorithm with the headlines from the file
5. Generate and display new "fake news" headlines on command line
Note: This process can also be done in two steps by running `scrapeNews.py <keywords> <numPages>` to generate the text file and then running `HMM.py <filename> <numNews>`.
