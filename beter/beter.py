#! python3
# beter.py - gets images from r/whothefuckup

import requests, os, bs4 ,random, discord,time,pyperclip,shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from discord.ext import commands
from PIL import Image,ImageDraw,ImageEnhance

TOKEN= 'NDg3OTI4MjY1MjU2OTkyNzY5.XTwa3g.cDVrNbilT8tzcPgEsphsXG2H9IQ'

reddit_index=-1
post=''
insta_index=-1
previous_iguser=''
private_account = []
# visited_iguser={}


def reddit_meme(subname):
    url = 'https://www.reddit.com/r/'+ subname # starting url
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    # Find the URL of the comic image.
    reddit_elem = soup.select('._2_tDEnGMLxpM6uOa2kaDB3.ImageBox-image.media-element')
    if reddit_elem == []:
        return 'Could not find reddit image.'
    else:
        global reddit_index
        reddit_index= reddit_index+1
        if(reddit_index>len(reddit_elem)-1):
            reddit_index=0
        return reddit_elem[reddit_index].get('src')

def deepfry(deep_fried_pfp):
    emoji_size = 300
    devil_filename = 'devil.png'
    hundred_filename = '100.png'

    devil_emoji = Image.open(devil_filename)
    hundred_emoji = Image.open(hundred_filename)

    devil_emoji = devil_emoji.resize((emoji_size,emoji_size))
    hundred_emoji = hundred_emoji.resize((emoji_size,emoji_size))

    width, height = deep_fried_pfp.size

    deep_fried_pfp.paste(hundred_emoji,(width-hundred_emoji.size[0], height-hundred_emoji.size[1]),hundred_emoji)
    deep_fried_pfp.paste(devil_emoji,(0,devil_emoji.size[1]),devil_emoji)

    contrast = ImageEnhance.Contrast(deep_fried_pfp)
    deep_fried_pfp=contrast.enhance(50)
    deep_fried_pfp.save(os.path.join('.','test_deepfried.png'))
    

class InstagramBot:

    
    def __init__(self,username,password):
        self.username= username
        self.password= password
        self.driver= webdriver.Firefox()

    def close_browser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        loginButton= driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        loginButton.click()
        time.sleep(2)
        usernameElem = driver.find_element_by_xpath("//input[@name='username']")
        usernameElem.clear()
        usernameElem.send_keys(self.username)
        passwordElem = driver.find_element_by_xpath("//input[@name='password']")
        passwordElem.clear()
        passwordElem.send_keys(self.password)
        passwordElem.send_keys(Keys.RETURN)
        time.sleep(3)
        
    def insta_meme(self,iguser):
        driver= self.driver
        driver.get("https://www.instagram.com/"+iguser)
        #htmlElem = browser.find_element_by_tag_name('html')
        links = driver.find_elements_by_css_selector('div.v1Nh3.kIKUG._bz0w a')
        # posts=links[:]
        # global insta_index
        # no_of_posts= int(driver.find_elements_by_css_selector('span.g47SY')[0].text)
        global insta_index,post,private_account
        insta_index= insta_index+1
        if(insta_index>len(links)-1):
            insta_index=0
        if links != []:
            post=links[insta_index].get_attribute('href')
        private_account = driver.find_elements_by_css_selector('h2.rkEop')

    def download_pic(self):
        driver = self.driver
        driver.get('https://dinsta.com')
        global post
        pyperclip.copy(post)
        pic = pyperclip.paste()
        download_elem = driver.find_element_by_css_selector('input#url')
        download_elem.clear()
        download_elem.send_keys(pic)
        download_elem.send_keys(Keys.RETURN) 
        time.sleep(3)
        download_site = driver.find_element_by_css_selector('button a')
        download_site.click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL,'a')
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL,'c')
        #pyperclip.copy(driver.find_element_by_tag_name('img').get_attribute('src'))
        return pyperclip.paste()

client = discord.Client()

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    author= message.author
    content= message.content
    channel=message.channel
    print('{}: {}'.format(author,content))
    if content.startswith('beter reddit'):
        await channel.send(reddit_meme(content[11:]))
    if content.startswith('beter insta'):
       IG= InstagramBot("niciocioarazdreanta","my_password_secret_;)")
       IG.insta_meme(content[12:])
       if private_account == [] :
           print('Public')
           await channel.send(post)
       else:
           print('Private')
           IG.login()
           IG.insta_meme(content[12:])
           await channel.send(IG.download_pic())
    
    if content.startswith('beter pfp'):
        if(message.mentions.__len__()>0):
            for user in message.mentions:
                os.chdir('D:\\BeterBot\\Deep Fried Memes')
                response= requests.get(user.avatar_url_as(format="png"),stream= True)
                pfp_image = open('pfp.png','wb')
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, pfp_image)
                pfp_image.close()
                pfp = Image.open('pfp.png')
                deepfry(pfp) 
                await channel.send(file=discord.File('test_deepfried.png'))
'''
@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel=message.channel
    await channel.send('{}: {}'.format(author,content))
'''

client.run(TOKEN) 