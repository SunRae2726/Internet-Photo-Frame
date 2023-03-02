from subprocess import run
import time
import os
import urllib.request
import random
import RPi.GPIO as GPIO
import requests
import re

timestr = time.strftime("%Y%m%d-%H%M%S")
random.seed(timestr)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
button = 18
LED = 17
skip = 23
modeButton = 24
LEDskip = 6
LEDmode = 19
GPIO.setup(button, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(skip, GPIO.IN)
GPIO.setup(LEDskip, GPIO.OUT)
GPIO.setup(modeButton, GPIO.IN)
GPIO.setup(LEDmode, GPIO.OUT)

website = ["https://cn.bing.com/discover/anime?FORM=IRST01","https://cn.bing.com/images/search?q=anime+cute&qs=n&form=QBILPG&sp=-1&pq=anime+cute&sc=8-7&sk=&cvid=AEA2EDB6AA7744199D8D296688173F3E","https://cn.bing.com/images/search?q=anime%20sAO&qs=n&form=QBIR&sp=-1&pq=anime%20sao&sc=8-9&sk=&cvid=8D42BEF0945A45929864086A775B78C7","https://cn.bing.com/images/search?q=anime%20cute%20with%20headphones&qs=n&form=QBIR&sp=-1&pq=anime%20cute%20with%20headphones&sc=0-25&sk=&cvid=757FEA92D86E4D9280959029F7C00E4B","https://cn.bing.com/images/search?q=anime%20happy&qs=n&form=QBIR&sp=-1&pq=anime%20happy&sc=8-11&sk=&cvid=84B4F091F4BA4AD9BDBF26103FC98B8A","https://cn.bing.com/images/search?q=anime%20angel%20beats&qs=n&form=QBIR&sp=-1&pq=anime%20angel%20beats&sc=8-11&sk=&cvid=468D8A73DD584417A076CD1869EC6DA0","https://cn.bing.com/images/search?q=anime%20kanna&qs=n&form=QBIR&sp=-1&pq=anime%20kanna&sc=8-6&sk=&cvid=83B3952DBABA4D12AADA5146E1D75E75","https://cn.bing.com/images/search?q=anime%20fall&qs=n&form=QBIR&sp=-1&pq=anime%20fall&sc=8-6&sk=&cvid=3488728AD50E48C79C310579ECA97E0F","https://cn.bing.com/images/search?q=anime%20winter&qs=n&form=QBIR&sp=-1&pq=anime%20winter&sc=8-6&sk=&cvid=5D1063CB083C48E8B33776889B251398","https://cn.bing.com/images/search?q=anime%20vocaloid&qs=n&form=QBIR&sp=-1&pq=anime%20vocaloid&sc=8-8&sk=&cvid=E6382564E68F4231970CB91C60968DAA","https://cn.bing.com/images/search?q=anime%20kawaii&qs=n&form=QBIR&sp=-1&pq=anime%20kawaii&sc=8-8&sk=&cvid=87FC581459314FD6A8578621DB305D77","https://cn.bing.com/images/search?q=anime%20madoka%20magica&qs=n&form=QBIR&sp=-1&pq=anime%20madoka%20magica&sc=7-19&sk=&cvid=4CE3DA1823BB4D13AFD6DD161226B8E2","https://cn.bing.com/images/search?q=anime%20girl&qs=IM&form=QBIR&sp=1&pq=anime%20&sc=8-6&cvid=297E80593A3C45519A7B9B617FDD74D3","https://cn.bing.com/images/search?q=anime%20snow&qs=n&form=QBIR&sp=-1&pq=anime%20snow&sc=5-14&sk=&cvid=89702092BCC441D1AED4DFFC84CC855D","https://cn.bing.com/images/search?q=anime%20wallpaper&qs=IM&form=QBIR&sp=6&pq=anime&sk=IM5&sc=8-5&cvid=554BC78555994A6880B03ED460BDD540","https://cn.bing.com/images/search?q=re%20zero&qs=n&form=QBIR&sp=-1&pq=re%20zero&sc=8-4&sk=&cvid=2304AA4441D74B839C5113C4D471E641","https://cn.bing.com/images/search?q=konosuba%20wallpaper&qs=n&form=QBIR&sp=-1&pq=konosuba%20wallpaper&sc=3-17&sk=&cvid=37F75E09711F449B8943FC87FEF11A81","https://cn.bing.com/images/search?q=your%20name%20anime%20wallpaper&qs=IM&form=QBIR&sp=2&pq=your%20name%20anim&sk=IM1&sc=5-14&cvid=FF4C243D1A6C4F9A99010C7EC38F4857","https://cn.bing.com/images/search?q=charlotte%20anime%20wallpaper&qs=n&form=QBIR&sp=-1&pq=charlotte%20anime%20wallpaper&sc=2-22&sk=&cvid=35511FB3676841059098ED576D69E2E0","https://cn.bing.com/images/search?q=Anime%20water%20Stars&qs=n&form=QBIR&sp=-1&pq=anime%20water%20stars&sc=0-17&sk=&cvid=5F5C833FB32748EC885D77B4930EF670","https://cn.bing.com/images/search?q=Anime%20angel%20%20Stars&qs=n&form=QBIR&sp=-1&pq=anime%20angel%20stars&sc=0-17&sk=&cvid=558531514E044CA9A461CC9369C48E3D","https://cn.bing.com/images/search?q=magic%20the%20gathering&qs=SC&form=QBIR&sp=1&pq=magic%20tg&sc=8-8&cvid=9996DACABCC740CAA4D68B"] 

def debounce(pin):
    result = GPIO.input(pin)
    time.sleep(0.05)
    return result


#run (["sudo","fbi","-T","1","--noverbose", "-a","image.jpg"])

def downloader(image_url):
    try:
        file_name = "RC1"
        full_file_name = str(file_name)+ '.jpg'
        urllib.request.urlretrieve(image_url,full_file_name)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        run(['sudo','killall','fbi'])
        exit(1)
    except:
        print("Problem acessing the picture url.")

def save(image_url):
    try:
        file_name = "Saves/"+str(timestr)
        full_file_name = str(file_name)+ '.jpg'
        urllib.request.urlretrieve(image_url, full_file_name)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        run(['sudo','killall','fbi'])
        exit(1)
    except:
        print("Problem saving.")

def findImage(): 
    try:
        www = requests.get(website[z])
        html = www.text
        #print(html)
        matches = re.findall("https?:\S+\.jpe?g",html)
        print(matches)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        run(['sudo','killall','fbi'])
        exit(1)
    except ValueError:
        print("Error. A internet procblem has occured.")
        matches = 0
    finally:
        return matches

previouspress = False
previouskip = False
previousMode = False
internetMode = True
while(True):
    if(internetMode):
        for i in range(100):
            if(not internetMode):
                break
            print("Displaying...")
            z = random.randint(0,20)    
            image = findImage()
            x = random.randint(0, len(image)-1)
            print(x)
            GPIO.output(LEDskip, GPIO.LOW)
            downloader(image[x])
            GPIO.output(LEDmode, GPIO.LOW)
            GPIO.output(LED, GPIO.LOW)
            run(['sudo','killall','fbi'])
            run (["sudo","fbi","-T","1","--noverbose", "-a","RC1.jpg"])
            try:  
                for a in range(110):
                    pressMode = debounce(modeButton)
                    pressed = debounce(button)
                    presskip = debounce(skip)
                    #print(pressMode)
                    if(pressed == True and previouspress == False):
                        timestr = time.strftime("%Y%m%d-%H%M%S")
                        print('saving...')
                        GPIO.output(LED, GPIO.HIGH)
                        save(image[x])
                        previouspress = True
                    if(pressed == True and previouspress == False):
                        previouspress = False
                    if(pressed == False):
                        previouspress = False
                    if(presskip == True and previouskip == False):
                        GPIO.output(LEDskip, GPIO.HIGH)
                        print("skipping...")
                        previouskip = True
                        break
                    if(presskip == True and previouskip == False):
                        Previouskip == False
                    if(presskip == False):
                        previouskip = False
                    if(pressMode == True and previousMode == False):
                        GPIO.output(LEDmode, GPIO.HIGH)
                        print("Changing mode...")
                        previousMode == True
                        internetMode = False
                        break
                    if(pressMode == True and previousMode == False):
                        previousMode == False
                    if(pressMode == False):
                        previousMode = False
            except:
                print("problem occured while checking button.")
                run(['sudo','killall','-9','fbi'])
                exit(0)
                
    if(not internetMode):
        for t in range(10):
            if(internetMode):
                break
            print("The mode changed.")
            GPIO.output(LEDmode, GPIO.LOW)
            GPIO.output(LEDskip, GPIO.LOW)
            files = os.listdir('Saves')
            randomPic = random.randint(0, len(files)-1)
            display = "Saves/"+files[randomPic]
            run(['sudo','killall','-9','fbi'])
            run(['sudo','fbi','-a','-T','1','-noverbose',display])
            try:
                for a in range(100):
                    pressMode = debounce(modeButton)
                    presskip = debounce(skip)
                    if(presskip == True and previouskip == False):
                        GPIO.output(LEDskip, GPIO.HIGH)
                        print("skipping...")
                        previouskip = True
                        break
                    if(presskip == True and previouskip == False):
                        Previouskip == False
                    if(presskip == False):
                        previouskip = False
                    if(pressMode == True and previousMode == False):
                        GPIO.output(LEDmode, GPIO.HIGH)
                        print("Changing mode...")
                        previousMode == True
                        internetMode = True
                        break
                    if(pressMode == True and previousMode == False):
                        previousMode == False
                    if(pressMode == False):
                        previousMode = False
            except:
                run(['sudo','killall','fbi'])
                exit(1)
        run(['sudo','killall','fbi'])
