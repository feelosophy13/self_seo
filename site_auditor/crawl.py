import sys
import re, html5lib
from bs4 import BeautifulSoup
from threading import Thread
from urllib2 import urlopen, build_opener, HTTPRedirectHandler, Request, URLError
from urlparse import urljoin
from requests import head
from site_auditor.models import Site, Page, H_Tag, Image_Link, CSS_Link, JS_Link, Page_Link, Email_Link, External_Link, Canonical_Link, Trivial_Link, Static_File_Link

unvisited_page_urls = []
visited_page_urls = []
threadlist = []
static_file_types = ['.png', '.jpg', 'jpeg', '.pdf', '.gif', '.svg', '.mp3', '.mp4']

# single-threaded crawl(); functional
def crawl(url):
    site = initialize_site(url)
    while len(unvisited_page_urls) > 0:
        print str(len(visited_page_urls)) + ' pages processed'
        print 'pages processed:'
        print visited_page_urls
        print '\n'
        print str(len(unvisited_page_urls)) + ' remaining pages to be processed in queue'
        print 'pages to be processed:' 
        print unvisited_page_urls 
        print '\n'
        process_page(unvisited_page_urls.pop(0), site)
    print 'crawl() okay'

# this function sets main site URL, 'page_archive' dictionary, and return HTML of main site URL 
def initialize_site(url):
    if is_valid_url(url):
    	canonical_site_set = canonical_site_is_set(url)
        if canonical_site_set:
        	url = get_redirected_url(url)
        site = Site(url=url, canonical_site_set=canonical_site_set)
        site.save()
        process_first_page(url, site)
        return site
        print 'initialize_site() okay'

def process_first_page(url, site):
    if url not in visited_page_urls:
        visited_page_urls.append(url)
    html = load_html(url)
    GA_installed = GA_is_installed(html)    
    page = Page(site=site, url=url, GA_installed=GA_installed)
    page.save()
    h_tag_levels = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']	
    for level in h_tag_levels:
        process_h_tags(url, html, site, page, level)        
    process_img_links(url, html, site, page)
    process_css_links(url, html, site, page)
    process_js_links(url, html, site, page)
    process_canonical_links(url, html, site, page)
    process_href_links(url, html, site, page)
    process_meta_title(url, html, site, page)
    process_meta_description(url, html, site, page)
    print 'process_first_page() okay'

def process_page(url, site):
    if url not in visited_page_urls:
        visited_page_urls.append(url)
    html = load_html(url)
    GA_installed = GA_is_installed(html)    
    page = Page.objects.get(site=site, url=url)
    h_tag_levels = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']	
    for level in h_tag_levels:
        process_h_tags(url, html, site, page, level)
    process_img_links(url, html, site, page)
    process_css_links(url, html, site, page)
    process_js_links(url, html, site, page)
    process_canonical_links(url, html, site, page)
    process_href_links(url, html, site, page)
    process_meta_title(url, html, site, page)
    process_meta_description(url, html, site, page)
    page.save()
    print 'process_page() okay'

def process_h_tags(url, html, site, page, level):
    h_tags = html.findAll(type)
    # process h tags; extract text only without the wrapping HTML codes
    for h in h_tags:
    	text = extract_text(h)
    	h_tag = H_Tag(text=text, site=site, page=page, level=level)
    	h_tag.save()    	
    print 'process_t_tags() okay'

""" MULTI-THREAD PROCESS_H_TAGS()
def process_h_tags(url, html, site, page, level):
    h_tags = html.findAll(type)
    # process h tags; extract text only without the wrapping HTML codes
    for h in h_tags:    	
    	thread = Thread(target=distributed_process_h_tag, args=(h, site, page, level))
        thread.daemon = True
        thread.start()
    print 'process_t_tags() okay'

def distributed_process_h_tag(h, site, page, level):
    text = extract_text(h)
    h_tag = H_Tag(text=text, site=site, page=page, level=level)
    h_tag.save()    	
"""

def process_img_links(url, html, site, page):
    img_list = html.findAll('img', src=True)
    # process image links
    for img in img_list:
        link = img['src'] = urljoin(site.url, img['src']) # making sure that URL is absolute
        try: 
            alt = img['alt']
        except KeyError:
            alt = ''
        found = head(link).status_code != 404  
        img_link = Image_Link(link=link, site=site, page=page, alt=alt, found=found)
        img_link.save()
    print 'img_links() okay'

""" MULTI-THREAD PROCESS_IMG_LINKS()
def process_img_links(url, html, site, page):
    img_list = html.findAll('img', src=True)
    # process image links
    for img in img_list:
        thread = Thread(target=distributed_process_img_link, args=(img, site, page))
        thread.daemon = True
        thread.start()
    print 'img_links() okay'

def distributed_process_img_link(img, site, page):
    link = img['src'] = urljoin(site.url, img['src']) # making sure that URL is absolute
    try: 
        alt = img['alt']
    except KeyError:
        alt = ''
    found = head(link).status_code != 404  
    img_link = Image_Link(link=link, site=site, page=page, alt=alt, found=found)
    img_link.save()
"""

def process_css_links(url, html, site, page):
    css_list = html.findAll('link', rel='stylesheet')
    # process css links
    for css in css_list:
        link = css['href'] = urljoin(site.url, css['href']) # making sure that URL is absolute
        found = head(link).status_code != 404
        css_link = CSS_Link(link=link, site=site, found=found)
        css_link.save()
        css_link.page.add(page)
    print 'css_links() okay'

""" MULTI-THREAD PROCESS_CSS_LINKS()
def process_css_links(url, html, site, page):
    css_list = html.findAll('link', rel='stylesheet')
    # process css links
    for css in css_list:
        thread = Thread(target=distributed_process_css_link, args=(css, site, page))
        thread.daemon = True
        thread.start()
    print 'css_links() okay'

def distributed_process_css_link(css, site, page):
    link = css['href'] = urljoin(site.url, css['href']) # making sure that URL is absolute
    found = head(link).status_code != 404
    css_link = CSS_Link(link=link, site=site, found=found)
    css_link.save()
    css_link.page.add(page)
"""

def process_js_links(url, html, site, page):
    js_list = html.findAll('script', src=True)
    # process js links
    for js in js_list:
        link = js['src'] = urljoin(site.url, js['src']) # making sure that URL is absolute
        found = head(link).status_code != 404
        js_link = JS_Link(link=link, site=site, found=found)
        js_link.save()
        js_link.page.add(page)
    print 'js_links() okay'

""" MULTI-THREAD PROCESS_JS_LINKS()
def process_js_links(url, html, site, page):
    js_list = html.findAll('script', src=True)
    # process js links
    for js in js_list:
        thread = Thread(target=distributed_process_js_link, args=(js, site, page))
        thread.daemon = True
        thread.start()
    print 'js_links() okay'

def distributed_process_js_link(js, site, page):
    link = js['src'] = urljoin(site.url, js['src']) # making sure that URL is absolute
    found = head(link).status_code != 404
    js_link = JS_Link(link=link, site=site, found=found)
    js_link.save()
    js_link.page.add(page)    
"""

def process_canonical_links(url, html, site, page):
    canonical_list = html.findAll('link', rel='canonical')
    # process canonicalization    
    for c in canonical_list:
        link = c['href'] = urljoin(site.url, c['href']) # making sure that URL is absolute
        found = head(link).status_code != 404
        c_link = Canonical_Link(link=link, site=site, page=page, found=found)
        c_link.save()
    print 'process_canonical_links() okay'


# BELOW IS THE LOGIC BEHIND PROCESSING (INTERNAL) PAGE LINKS AND CREATING CORRESPONDING PAGE() CLASS OBJECTS FOR THOSE LINKS
# 1. load HTML of a page
# 2. find all links, referred to as "page links", that point to other (internal) pages
# 3. for each page link, examine the following:
#    - if Page() class object hasn't been created under that page link's URL
#      > then it means the page has not been crawled and no information was extracted
#      > create a Page() class object, add 1 to its number of incoming links (n_incoming_links)
#      > append the page link to the list of unvisited page links to be indexed later
#    - if Page() class object has been created under that page link's URL
#      > then it means the page has already been crawled and information was extracted
#      > do NOT create a Page() class object; just call the already created Page() object via Page.objects.get() method and increment the Page() class object's incoming link count
#      > also do NOT append the page link to the list of unvisited page links because the page has already been visited and indexed
# 4. repeat step 1 through 3 while the list of unvisited page links is filled 
def process_href_links(url, html, site, page):
    a_list = html.findAll('a', href=True)
    # process page links 
    for a in a_list:
        a['href'] = a_href = urljoin(site.url, a['href']) # making sure that URL is absolute
        if 'mailto:' in a_href: # if email link 
            process_email_link(a_href, site, page) # store the email link
        else: # if not email link
            try: 
                found = head(a_href).status_code != 404 # check if link is good
            except:
                found = False
        if site.url in a_href: # if internal link
            if '#' not in a_href: # if not a trivial link
                if is_not_page_link(a_href): # if static file link (e.g. direct link to images or css file)
                    process_static_file_link(a_href, site, page, found)
                else: # if a page link
                        process_page_link(a_href, site, page, found) # add page
                        if (a_href not in visited_page_urls) and (a_href not in unvisited_page_urls) and found: 
                            unvisited_page_urls.append(a_href) # put into the list of page links to visit to crawl                            
                        page.n_outgoing_links += 1 # add 1 to the number of outgoing page link to the page
                        page.save()
                        try: # try finding target page (recipient) of page link and add 1 to its number of incoming page links
                            target_page = Page.objects.get(site=site, url=a_href) #
                            target_page.n_incoming_links += 1
                        except: # if target page doesn't exist, create one and add 1 to its number of incoming page links
                            target_page = Page(site=site, url=a_href, n_incoming_links=1)
                        target_page.save()
            else: # if a trivial link
                process_trivial_link(a_href, site, page, found)
        else: # if external link
            process_external_link(a_href, site, page, found)
    print 'process_href_links() okay'

def process_external_link(a_href, site, page, found):
    try: 
        external_link = External_Link.objects.get(link=a_href, site=site, page=page)
    except:
        external_link = External_Link(link=a_href, site=site, page=page, found=found)
        external_link.save()
    print 'process_external_link() okay'
 
# each page should have only one meta title 
# in case of multiple meta title, Google utilizes only the first 
# you can read more about it here: http://moz.com/ugc/google-serp-test-multiple-page-title-meta-description-tags
def process_meta_title(url, html, site, page):
    meta_title_list = html.findAll('meta', attrs={'property':'og:title'})    
    try:
        page.meta_title = meta_title_list[0]['content']

    except:
        page.meta_title = ''
    page.save()
    print 'process_meta_title() okay'

# each page should have only one meta description 
# in case of multiple meta description, Google utilizes only the first 
# you can read more about it here: http://moz.com/ugc/google-serp-test-multiple-page-title-meta-description-tags
def process_meta_description(url, html, site, page):
    meta_description_list = html.findAll('meta', attrs={'name':'description'})
    try:
        page.meta_description = meta_description_list[0]['content']
    except:
        page.meta_description = ''
    page.save()
    print 'process_meta_description() okay'
     
def process_email_link(a_href, site, page):
    try:
        email_link = Email_Link.objects.get(link=a_href, site=site, page=page)
    except:
        email_link = Email_Link(link=a_href, site=site)
        email_link.save()    
        email_link.page.add(page)
    print 'process_email_link() okay'
    
def process_static_file_link(a_href, site, page, found):
    try:
        static_file_link = Static_File_Link.objects.get(link=a_href, site=site, page=page)
    except:
        static_file_link = Static_File_Link(link=a_href, site=site, page=page, found=found)
        static_file_link.save()
    print 'process_static_file_link() okay'

def process_page_link(a_href, site, page, found):
    try:
        page_link = Page_Link.objects.get(link=a_href, site=site)
    except:
        page_link = Page_Link(link=a_href, site=site, found=found)
        page_link.save()
        page_link.page.add(page)
    print 'process_page_link() okay'
    
def process_trivial_link(a_href, site, page, found):
    try:
        trivial_link = Trivial_Link(link=a_href, site=site, page=page)
    except:
        trivial_link = Trivial_Link(link=a_href, site=site, page=page, found=found)
        trivial_link.save()
    print 'process_trivial_link() okay'

#######################################################################################
# BELOW ARE VARIOUS HELPER FUNCTIONS FOR THE CORE FUNCTIONS

def is_valid_url(url):
    request = Request(url)
    try:	
        response = urlopen(request)
    except URLError:
        return False
    else:
        return True
        
# this code was copied from Stack Overflow; http://stackoverflow.com/questions/5538280/determining-redirected-url-in-python
def get_redirected_url(url):
    opener = build_opener(HTTPRedirectHandler)
    request = opener.open(url)
    return request.url

def different_by_trailing_slash(url1, url2):
    if url1 == url2:
        return True
    else:
        return (url1[-1] == '/' and url1[:-1] == url2) or (url2[-1] == '/' and url2[:-1] == url1)

def extract_text(raw_html):
    return ''.join(raw_html.findAll(text=True)).strip()

def load_html(url):
    try: 
        html = urlopen(url).read().decode('utf-8')
    except: 
        html = ''
    html = BeautifulSoup(html, 'html5')
    return html    

# this function determines whether a page has Google Analytics code embedded; returns True or False	
def GA_is_installed(html):
    pattern = r'UA\-[0-9]+\-[0-9]+'
    ua_code = re.findall(pattern, str(html.html))
    return len(ua_code) != 0

# this function is a quick method to check if developer considered responsiveness of his webpage
# this is NOT a full-proof method whether a site correctly adjusts to a mobile viewport 
def is_responsive_page(html):
    return 'viewport' in html

# this function determines whether a site is canonicalized (returns True or False)
def canonical_site_is_set(url):
    redirected_url1 = get_redirected_url(url)
    if 'www.' in url:
        alt_url = url.split('www.', 1)
        alt_url = alt_url[0] + alt_url[1]	
        redirected_url2 = get_redirected_url(alt_url)
    else:
    	insertion_index = url.index('//') + 2
    	alt_url = url[:insertion_index] + 'www.' + url[insertion_index:]
    	redirected_url2 = get_redirected_url(alt_url)
    return (redirected_url1 == redirected_url2) or different_by_trailing_slash(redirected_url1, redirected_url2)		

# this function returns True if a link is pointed to a static file (e.g. pdf, png, jpg, mp3, etc.) and hence is not a page link
def is_not_page_link(link):
    return link[-4:] in static_file_types

### DETERMINE WHETHER A SITE HAS A MOBILE SITE SET UP 
def is_mobile_site_set(url):
    pass
	
def find_mobile_site(url):
    pass