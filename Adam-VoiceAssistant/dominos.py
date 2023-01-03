from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from Adam import speak, takeCommand, engine
import config

def pizza():
    driver = webdriver.Chrome(r"C:\Users\windows 10\Desktop\chromedriver.exe")
    driver.maximize_window()
    speak ("Opening Dominos")
    
    driver.get('https://www.dominos.co.in/')
    sleep(2)

    speak("Getting ready to order")
    driver.find_element("link text", "ORDER ONLINE NOW").click()
    sleep(2)
    
    #locate me
    speak("Finding your location")
    driver.find_element("class name", "srch-cnt-srch-inpt").click()
    sleep(2)

    #entering your location
    location= "geeta colony"
    speak("Entering your location...")
    driver.find_element(
        By.XPATH,"/html/body/div[3]/div/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]/div[2]/div/div[1]/input"
    ).send_keys(location)
    sleep(2)

    #choosing option for location
#every time you run this program, the list changes maybe nested if statement would help
    driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]/div[2]/div[2]/div/ul/li[4]"
    ).click()
    sleep(2)
    #/html/body/div[3]/div/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]/div[2]/div[2]/div/ul/li[2]  if above link doesn't work

    try:
        #login/signup
        speak("Logging in")
        driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div/div[1]/div[1]/div/div[3]/div[3]/div[1]"
        ).click()
        sleep(2)
    except:
        speak("Your location could not be found. Try again later")
        exit()
    
    speak("Entering your phone number")

    

    driver.find_element(
        By.XPATH, "//*[@id='__next']/div/div/div[1]/div[1]/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div/div[2]/div/form/div[1]/div[2]/input"
    ).send_keys(config.phone_no)
    sleep(2)

    #click on submit
    driver.find_element(
        By.XPATH, "//*[@id='__next']/div/div/div[1]/div[1]/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div/div[2]/div/form/div[2]/input"
    ).click()
    sleep(2)

    speak("What is your OTP?")
    sleep(10)

    otp_log= takeCommand()

    #enter otp
    while (len(otp_log) != 6):
        engine.runAndWait()
        speak("What is you OTP? ")
        otp_log= takeCommand()
        sleep(3)
        break

    if (len(otp_log) == 6 ):
        driver.find_element(
            By.XPATH, "//*[@id='__next']/div/div/div[1]/div[1]/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/input"
        ).send_keys(otp_log)
        

    

    #submit OTP
    driver.find_element(
        By.XPATH,"//*[@id='__next']/div/div/div[1]/div[1]/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div/div[2]/div/div/div/div[2]/div[2]/button/span"
    ).click()
    speak("O T P submitted")
    sleep(2)
        
    speak("Do you want me to order from your favourites?")
    query_fav = takeCommand().lower()

    if 'yes' in query_fav:
        try:
            #pizza adding to cart
            driver.find_element(
                By.XPATH, "//*[@id='mn-lft']/div[2]/div/div[13]/div/div/div[2]/div[3]/div/button/span"
            ).click()
            sleep(1)
        
        except:
            speak("The entered OTP is incorrect.")
            exit()

        speak("Adding your favourite farm house to cart!")

        #adding extra cheese
        speak("Do you want me to add extra cheese?")
        ex_cheese= takeCommand().lower()
        if "yes" in ex_cheese:
            driver.find_element(
                By.XPATH, "//*[@id='mn-lft']/div[2]/div/div[1]/div/div/div[2]/div[3]/div[2]/button"
            ).click()
            speak("Extra cheese added")
        
        elif "no" in ex_cheese:
            driver.find_element(
                By.XPATH, "//*[@id='mn-lft']/div[2]/div/div[1]/div/div/div[2]/div[3]/div[1]/button"
            ).click()

#added path for not now  same as above
        else:
            speak("I don't know that")
            driver.find_element(
                By.XPATH, "//*[@id='mn-lft']/div[2]/div/div[1]/div/div/div[2]/div[3]/div[1]/button"
            ).click()

        speak("Adding pepsi.")
        #adding pepsi
        driver.find_element(
            By.XPATH, "//*[@id='mn-lft']/div[14]/div/div[2]/div/div/div[2]/div[2]/div/button"
        ).click()
        sleep(1)

        speak(" 1 medium Farm house pizza and 1 pepsi added to cart")
        
        #to change the quantity of food
        speak("Would you like to increase the quantity?")
        qty= takeCommand().lower()
        qty_pizza= 0
        qty_pepsi =0

        if "yes" in qty :
            speak("Would you like to increase the quantity of pizza?")
            wh_qty = takeCommand().lower()
            if "yes" in wh_qty:
                speak("How many more pizzaa would you like to add?")
                try:
                    qty_pizza= takeCommand()
                    qty_pizza = int( qty_pizza)
                    if qty_pizza > 0:
                        talk_pizza= f" Adding {qty_pizza} more pizzas"
                        speak(talk_pizza)
                        for i in range (qty_pizza):
                            driver.find_element(
                                By.XPATH, "//*[@id='__next']/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div"
                            ).click()
                
                except:
                    speak("I couldn't understand")

            else:
                pass

            speak("Would you like to increase the quantity of pepsi?")
            pep_qty = takeCommand().lower()
            if "yes" in wh_qty:
                speak("How many more pepsi would you like to add?")
                try:
                    qty_pepsi= takeCommand()
                    qty_pepsi = int( qty_pepsi)
                    if qty_pepsi > 0:
                        talk_pepsi= f" Adding {qty_pepsi} more pepsi"
                        speak(talk_pepsi)
                        for i in range (qty_pepsi):
                            driver.find_element(
                                By.XPATH, "//*[@id='__next']/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div"
                            ).click()
                
                except:
                    speak("I couldn't understand")

            else:
                pass

        elif "no" in qty:
            pass

        total_pizza= qty_pizza +1
        total_pepsi= qty_pepsi +1
        speak_num= f"This is your order list. {total_pizza} medium Pizzas and  {total_pepsi} Pepsis.  Do you want to checkout?"
        speak(speak_num)
        check_order= takeCommand().lower()

        # checkout
        if "yes" in check_order:
            speak("Checking out")
            driver.find_element(
                By.XPATH, "//*[@id='__next']/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/button"
            ).click()
            sleep(1)

            total_price= driver.find_element(
                By.XPATH, "//*[@id='__next']/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/span[2]"
            )
            total_price = f"Total price is {total_price.text}"
            speak(total_price)
            sleep(1)

        else:
            exit()

        #     Placing order
        speak("Placing your order")
        driver.find_element(
            By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div[3]/div[2]/div/div[6]/div/div/div[7]/button/span'
        ).click()
        sleep(2)
        try:
            speak("Saving your location")
            driver.find_element(
                By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div[3]/div/div/input'
            ).click()
            sleep(2)
        except:
            speak("The store is currently offline")

            # -- confirming do not say yes here unless you really wanna order -- 
        speak("Do you want to confirm your order? ")
        confirm= takeCommand()
        if "yes" in confirm:
            speak("Placing your order")
            driver.find_element(
                By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[2]/button/span'
            ).click()
            sleep(2)
            speak("Your order is placed successfully. Wait for dominos to deliver your order. Enjoy your day!")
        else:
            exit()

    else:
        exit()




pizza()