from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
browser = webdriver.Chrome(options=options)
browser.get("http://danielas3rtn54uwmofdo3x2bsdifr47huasnmbgqzfrec5ubupvtpid.onion")
input()