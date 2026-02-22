import sys
import requests
from bs4 import BeautifulSoup

def main():
    p = 53
    mod = 2 ** 64

    def http_req(url):
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print("Page not accessible:", url)
            sys.exit(1)
        return res.text

    def bodyText_and_links(html):
        soup = BeautifulSoup(html, "html.parser")

        if soup.title:
            title = soup.title.get_text().strip()
        else:
            title = "No title"

        for t in soup.find_all("script"):
            t.decompose()
        for t in soup.find_all("style"):
            t.decompose()

        if soup.body:
            body = soup.body.get_text(" ", strip=True)
        else:
            body = ""

        links = []
        for a in soup.find_all("a"):
            h = a.get("href")
            if h:
                links.append(h)

        return title, body, links

    def wordFreq(text):
        text = text.lower()
        freq = {}
        word = ""

        for ch in text:
            if ch.isalnum():
                word += ch
            else:
                if word != "":
                    freq[word] = freq.get(word, 0) + 1
                    word = ""

        if word != "":
            freq[word] = freq.get(word, 0) + 1

        return freq

    # polynomial rolling hash function
    def wordhash(wd):     
        h = 0
        power = 1
        for c in wd:
            h = (h + ord(c) * power) % mod   #s[i] = ord(c)
            power = (power * p) % mod
        return h

    def simHash(freqMap):
        bitScore = [0] * 64

        for w in freqMap:
            h = wordhash(w)
            cnt = freqMap[w]

            for i in range(64):
                if (h >> i) & 1:
                    bitScore[i] += cnt
                else:
                    bitScore[i] -= cnt

        finalHash = 0
        for i in range(64):
            if bitScore[i] > 0:
                finalHash += (1 << i)

        return finalHash

    def commonBits(a, b):
        x = a ^ b
        diff = 0
        for i in range(64):
            if x & 1:
                diff += 1
            x >>= 1
        return 64 - diff

    if len(sys.argv) != 3:
        print("Provide arguments like : python fileName.py url1 url2")
        sys.exit(1)

    url1 = sys.argv[1]
    url2 = sys.argv[2]

    html1 = http_req(url1)
    html2 = http_req(url2)

    title1, text1, links1 = bodyText_and_links(html1)
    title2, text2, links2 = bodyText_and_links(html2)

    print("\n______URL 1_________")
    print("Page Title:\n", title1)
    print("\nPage Body:\n")
    print(text1)          #This will show whole text from body.
    # print(text1[:45])  use this when we want to see limited text.

    print("\nPage Links:")
    for l in links1:
        print(l)

    #If we want to see only limited links, use this.
    # link_limit = 25
    # count = 0
    # for l in links1:
    #     print(l)
    #     count += 1
    #     if count == link_limit:
    #         break

#------------------------------------------------

    print("\n______URL 2________")
    print("Page Title:","\n",title2)
    print("\nPage Body:\n")
    print(text2)
    print("\nPage Links:")
    for l in links2:
        print(l)

    freq1 = wordFreq(text1)
    freq2 = wordFreq(text2)

    hash1 = simHash(freq1)
    hash2 = simHash(freq2)

    print("\nSimhash of URL 1:", hash1)
    print("Simhash of URL 2:", hash2)
    print("Common bits in simhash:", commonBits(hash1, hash2))

if __name__ == "__main__":
    main()