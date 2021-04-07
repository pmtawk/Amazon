#Import the necessary Libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
import time
import streamlit as st
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64

hide_streamlit_style = """
<style>
#MainMenu {​​​​​visibility: hidden;}​​​​​
footer {​​​​​visibility: hidden;}​​​​​
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.sidebar.image('1_AVZCVbIwuldUYrElrQ34bA.png', width = 250, height = 150)

password = st.sidebar.text_input("Please enter your password", type="password")
if password == 'MS42':


    st.sidebar.title("eWOM")
    st.sidebar.markdown("Visit Amazon website and pick any product that you would like to collect its reviews")
    st.sidebar.write(" https://www.amazon.com/")


    st.title("Opinion Mining")
    st.write("Do You Know What Your Customers Say About  ... ?")
    K=st.text_input("Enter an URL for a specific AMAZON product or write MS42 to generate a random link")
    agree= st.checkbox("Export the data into an excel file")

    if (K == []) or (K == ""):
        st.write("You are required to enter the URL for mining the reviews of a certain product of write MS42 ")

    else:
        if K == "MS42":
            driver = webdriver.Chrome('/Users/patriciatawk/Downloads/chromedriver') # Connect to the Chrome Driver
            driver.get('https://www.amazon.com/Shiseido-Ultimune-Power-Infusing-Concentrate/dp/B0126TMUMS/ref=cm_cr_arp_d_product_top?ie=UTF8')
        else:
            driver = webdriver.Chrome('/Users/patriciatawk/Downloads/chromedriver 2') # Connect to the Chrome Driver
            driver.get(K)

        #time.sleep(3)
        driver.find_element(By.PARTIAL_LINK_TEXT, 'See all reviews').click()
        time.sleep(3)

        url_list = []
        while len(driver.find_elements_by_xpath('//li[@class="a-last"]')) ==1:
            url_list.append(driver.current_url)
            driver.find_elements_by_xpath('//li[@class="a-last"]')[0].click()
            time.sleep(3)
        url_list.append(driver.current_url)
        print(url_list)

        name_list=[]
        review_list=[]
        purchase_list=[]
        date_list=[]
        rating_list=[]
        helpful_list=[]
        title_list=[]

        for i in range(len(url_list)):

            driver.get(url_list[i])
            time.sleep(1)
            name = driver.find_elements_by_xpath('//span[@class="a-profile-name"]')
            for i in range (len(name)):
                name_list.append(name[i].text)
            review = driver.find_elements_by_xpath('//span[@class="a-size-base review-text review-text-content"]')
            for i in range (len(review)):
                review_list.append(review[i].text)
            title = driver.find_elements_by_css_selector("a[data-hook='review-title']")
            for i in range (len(title)):
                title_list.append(title[i].text)
            purchase = driver.find_elements_by_xpath('//span[@class="a-size-mini a-color-state a-text-bold"]')
            for i in range (len(purchase)):
                purchase_list.append(purchase[i].text)
            date = driver.find_elements_by_xpath('//span[@class="a-size-base a-color-secondary review-date"]')
            for i in range (len(date)):
                date_list.append(date[i].text)
            rating = driver.find_elements_by_xpath('//span[@class="a-icon-alt"]')
            for star in rating:
                rating_list.append(star.get_attribute('innerHTML').split('stars')[0])
            helpful = driver.find_elements_by_xpath('//span[@class="a-size-base a-color-tertiary cr-vote-text"]')
            for i in range (len(helpful)):
                helpful_list.append(helpful[i].text)


        df = pd.DataFrame()
        df['customer']= pd.Series(name_list)
        df['title']= pd.Series(title_list)
        df['reviews']= pd.Series(review_list)
        df['date']= pd.Series(date_list)
        df['rating']= pd.Series(rating_list)
        df['helpful']= pd.Series(helpful_list)
        df['Verification']= pd.Series(purchase_list)

        st.write(df)

        driver.close()


        #agree= st.checkbox("Export the data into an excel file")
        if agree:
            st.checkbox("Great", value = True)
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click on the link and Save Link as FileName.csv)'
            st.markdown(href, unsafe_allow_html=True)

elif password != 'MS42':
    st.write('Please Enter the Correct Password')
