from bs4 import BeautifulSoup
import requests, re

# main function
def main():
    crawler = TorCrawler()
    crawler.crawl()

class TorCrawler:
    def __init__(self):
        # http://lockbitapt2d73krlbewgv27tquljgxr33xbwwsp6rkyieto7u4ncead.onion/
        # http://danschat356lctri3zavzh6fbxg2a7lo6z3etgkctzzpspewu7zdsaqd.onion/
        self._root_url = "http://danielas3rtn54uwmofdo3x2bsdifr47huasnmbgqzfrec5ubupvtpid.onion"
        # socks5h
        self._proxies = {
            "http":"socks5h://127.0.0.1:9150",
            "https":"socks5h://127.0.0.1:9150"
        }
        
        self._crawling_url = ""
        self._hrefs = []
        self._not_allowed_ext = ["mp4", "avi", "mov", "mkv", "wav", "flac", "raw", "iso", "exe", "dmg", "gz", "tar", "zip", "mp3", "xlsx", "pptx", "blend", "ai", "apk"]
        
    # return url
    def get_root_url(self):
        return self._root_url

    # return proxies
    def get_proxies(self):
        return self._proxies

    # print my ip information
    def get_my_ip(self):
        response = requests.get("http://ip-api.com/line", proxies=self.get_proxies())
        print(response.text)
    
    # get base urls from navigation bar
    def get_base_urls(self):
        response = requests.get(self.get_root_url(), proxies=self.get_proxies())
        soup = BeautifulSoup(response.text, "html.parser")
        a_tags = soup.find_all("a")
        hrefs = []
        title = []
        for a_tag in a_tags:
            try:
                hrefs.append(a_tag["href"])
                title.append(a_tag.text)
                # print(a_tag["href"], a_tag.text)
                if a_tag.text == "Onion link list":
                    self.crawl_list_page(a_tag["href"])
            except:
                pass
                
    def get_crawling_url(self):
        return self._crawling_url
    
    def set_crawling_url(self, url):
        self._crawling_url = url
        
    def add_href(self, url):
        self._hrefs.append(url)
        
    def clear_href(self):
        self._hrefs = []
    
    def check_href(self, url):
        return url in self._hrefs
    
    def get_not_allowed_ext(self):
        return self._not_allowed_ext
            
    # def crawl_each_page(self):
    
    # crawl "Onion link list" page
    def crawl_list_page(self, url):
        response = requests.get(url, proxies=self.get_proxies())
        soup = BeautifulSoup(response.text, "html.parser")
        ul_tags = soup.find_all("ul", class_="list")
    
        
        # get category list
        for ul_tag in ul_tags:
            li_tags = ul_tag.find_all("li")
            category_kind = li_tags[0].text
            if "Categories" in category_kind:
                category_kind = category_kind.replace(":", "")
                # send category kind, name, and url
                for li_tag in li_tags:
                    href = ""
                    try:
                        a_tag = li_tag.find("a")
                        href = url + a_tag["href"]
                    except:
                        href = ""
                    
                    if category_kind == "Special categories:":
                        continue
                    if li_tag.text == "Special categories:" or li_tag.text == "Categories:":
                        continue
                    data = {
                        "num": 1,
                        "category_kind": category_kind,
                        "category_name": li_tag.text,
                        "url": href
                    }
                    print(li_tag.text, "choose 1 to crawl, choose 2 to pass: ")
                    option = int(input())
                    if option == 1:
                        pass
                    elif option == 2:
                        continue
                    
                    response = requests.post("http://127.0.0.1:1023/kisia", json=data)
                    
                    if href != "" and "Categories" in category_kind:
                        self.crawl_each_list(li_tag.text, href)

                        
    def crawl_each_list(self, category, url):
        depth = 1
        response = requests.get(url + "&page=0", proxies=self.get_proxies())
        soup = BeautifulSoup(response.text, "html.parser")
    
        table = soup.find("div", id="maintable")
        # print(table)
        # Onion link    Description     Last seen       Added at        Actions
        rows = table.find_all(attrs={'class':'row up'})
        # print(rows)
        
        for row in rows:
            
            cols = row.find_all(attrs={'class':'col'})
            href = cols[0].find("a")["href"]
            data = {
                "num": 2,
                "category": category,
                "Onion link": href,
                "Description": cols[1].text,
                "Last seen": cols[2].text,
                "Added at": cols[3].text,
                "Actions": cols[4].text
            }
            response = requests.post("http://127.0.0.1:1023/kisia", json=data)
            self.set_crawling_url(href)
            self.clear_href()
            self.crawl_dark_web(href, depth+1, category, cols[1].text)

    def crawl_dark_web(self, url, depth, category, description):
        if depth == 5:
            return

        response = requests.get(url, proxies=self.get_proxies())
        if "HTTP Error" in response.text:
            return
        if response.status_code != 200:
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        a_tags = soup.find_all("a")
        # print(a_tags)
        for a_tag in a_tags:
            try:
                referer = url
                new_url = url
                if a_tag["href"] in new_url:
                    continue
                if a_tag["href"].startswith('/'):
                    new_url = self.get_crawling_url() + a_tag["href"]
                elif a_tag["href"].startswith('?'):
                    new_url = new_url + a_tag["href"]
                elif a_tag["href"].startswith('#'):
                    new_url = new_url + a_tag["href"]
                else:
                    new_url = a_tag["href"]
                
                if self.check_href(new_url):
                    continue
                else:
                    self.add_href(new_url)
                    
                url_type = "url"
                if new_url.split('.')[-1] in self.get_not_allowed_ext():
                    url_type = new_url.lstrip('.')
                if "github.com" in new_url:
                    continue
                
                bitcoin = ""
                try:    
                    bitcoin = ", ".join(re.findall(r'^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$', response.text))
                except:
                    bitcoin = ""
                print(category, a_tag.text, new_url, bitcoin)
                
                data = {
                    "num": 3,
                    "category": category,
                    "description": description,
                    "type": url_type,
                    "text": a_tag.text.replace("\n", ""),
                    "url": new_url,
                    "referer": referer,
                    "bitcoin": bitcoin
                }
                response = requests.post("http://127.0.0.1:1023/kisia", json=data)
                
                if url_type == "url": 
                    self.crawl_dark_web(new_url, depth+1, category, description)
            except:
                pass
        
    # finally crawl
    def crawl(self):
        self.get_my_ip()
        self.get_base_urls()

if __name__ == "__main__":
    main()
