import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
from psycopg2.errors import *
import numpy as np
import cv2
import easyocr
import time
import re
from PIL import Image
import pandas as pd

class App:
    def __init__(self):
        pass

    #page congiguration
    def set_page_config(self):
        icon = Image.open("biz_cards/icon.jpeg")
        st.set_page_config(page_title= "BizCardX",
                        page_icon= icon,
                        layout= "wide",)
        st.markdown("<h1 style='text-align: center; color: black; font-size:70px;'>BizCardX</h1>", unsafe_allow_html=True)
        st.markdown(""" 
            <style>
                    .stApp,[data-testid="stHeader"] {
                        background: url("https://wallpaper-mania.com/wp-content/uploads/2018/09/High_resolution_wallpaper_background_ID_77700405853-1200x750.jpg");
                        background-size: cover
                    }

                    
                    [data-testid="stSidebar"] {
                        background: url("https://wallpaper-mania.com/wp-content/uploads/2018/09/High_resolution_wallpaper_background_ID_77700014728.jpg");
                        color: 	#FFFFFF !important;
                    }
                    
                    
                    p {
                        color: black; font-weight:bold;
                    }

                    [data-testid="stFileUploader"]{
                        color: black; font-size:18px; font-weight:bold;
                    }
            </style>""",unsafe_allow_html=True)



    def home_page(self):
            left,centre,right=st.columns((3,0.25,1))
            with right:
                st.markdown('<p style="color: black; font-size:25px; font-weight:bold">TECHNOLOGIES USED :</p>',unsafe_allow_html=True)
                st.markdown("""
                            <p style="color: black; font-size:18px; font-weight:bold">*<span style="color: red; font-size:18px; font-weight:bold"> Python</span> *
                            <span style="color: red; font-size:18px; font-weight:bold"> Streamlit</span> *
                            <span style="color: red; font-size:18px; font-weight:bold"> EasyOCR</span> *
                            <span style="color: red; font-size:18px; font-weight:bold"> OpenCV</span> *
                            <span style="color: red; font-size:18px; font-weight:bold"> MySQL</span></p>""",unsafe_allow_html=True)
                st.markdown("""
                            <p style="color: black; font-size:18px; font-weight:bold">
                            To Learn more about easyOCR  <span><a style="color: #f2920c; font-size:18px; font-weight:bold" href="https://pypi.org/project/easyocr/">press here</a></span></p> """,unsafe_allow_html=True)
            
            with centre:
                st.markdown('<div style="height: 350px; border-left: 4px solid black;"></div>', unsafe_allow_html=True)
            
            with left:
                st.markdown("""<p style="color: black; font-size:30px; font-weight:bold">Welcome to the Business Card Application!</p>""",unsafe_allow_html=True)
                st.divider()
                st.markdown("""<p style="color: #fc0349; font-size:20px; font-weight:bold"> Bizcard is a Python application designed to extract information from business cards. It utilizes various technologies such as Streamlit, Python, EasyOCR , RegEx function, OpenCV, and MySQL database to achieve this functionality.""",unsafe_allow_html=True)
                st.markdown("""<p style="color: #f28f0c; font-size:20px; font-weight:bold">The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.</p>""",unsafe_allow_html=True)
                st.markdown("""<p style="color: black; font-size:18px; font-weight:bold">Click on the <span style="color: red; font-size:18px; font-weight:bold">Image to text</span> option to start exploring the Bizcard extraction.</p>""",unsafe_allow_html=True)
    
    
    def image_to_text_page(self):   
            conn = psycopg2.connect(database="card_data",host="localhost",user="postgres",password="root",port="5432")
            cursor = conn.cursor() 
            cursor.execute('''CREATE TABLE IF NOT EXISTS card(
                 name VARCHAR(255),
                 designation VARCHAR(255),
                 company VARCHAR(255),
                 contact VARCHAR(30) UNIQUE,
                 email VARCHAR(255),
                 website VARCHAR(255),
                 address VARCHAR(255),
                 city VARCHAR(255),state VARCHAR(255),pincode VARCHAR(255),
                 image BYTEA)''') 
            st.markdown('<p style="color: black; font-size:25px; font-weight:bold">IMAGE TO TEXT <img src="https://w7.pngwing.com/pngs/542/60/png-transparent-computer-icons-editing-font-awesome-video-editing-register-icon-angle-text-logo-thumbnail.png" alt="Custom Image" style="width: 30px; height: 30px;"></p>',unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Choose an image of a business card", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                clicked = st.button('IDENTIFY TEXT FROM IMAGE')
                col1,col2 = st.columns((2,2))
                with col1:
                    #===== Real Image =====#
                    nparr = np.frombuffer(file_bytes, np.uint8)
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    st.image(image,channels='BGR' ,use_column_width=True)
                    
                with col2:
                    #===== text extraction from image =====#
                    if clicked:
                        with st.spinner('Detecting text............'):
                            time.sleep(2)
                            
                        # cv2.cvtColor() method - used to convert an image from one color space to another    
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                        # Apply threshold to create a binary image
                        new, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

                        # Find contours in the binary image
                        contours,new = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                        # Iterate through each contour and draw it with a different color
                        for i in contours:
                            # Get the bounding rectangle coordinates
                            x, y, w, h = cv2.boundingRect(i)
                            # Change the text color to blue (BGR format)
                            color = (0, 255, 255)
                            # Draw a rectangle around the contour with the specified color
                            new=cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

                        st.image(new,use_column_width=True)
                    
            st.markdown('<p style="color: black; font-size:25px; font-weight:bold">TEXT EXTRACTION <img src="https://w7.pngwing.com/pngs/542/60/png-transparent-computer-icons-editing-font-awesome-video-editing-register-icon-angle-text-logo-thumbnail.png" alt="Custom Image" style="width: 30px; height: 30px;"></p>',unsafe_allow_html=True)
            st.markdown("###### Press below extract button to view structered text format & upload to database")
            st.write('Please note: This tab is only for business card image alone it will not accept random image')
            if st.button('EXTRACT & UPLOAD'):
                    with st.spinner('Extracting text...'):
                        reader=easyocr.Reader(['en'])
                        results = reader.readtext(image)
                        # print(results)
                        card_info = [str(i[1]) for i in results]
                        # print(card_info)
                        
                        card = ' '.join(card_info)  #convert to string
                        replacements = [
                            (";", ""),
                            (',', ''),
                            ("WWW ", "www."),
                            ("www ", "www."),
                            ('www', 'www.'),
                            ('www.', 'www'),
                            ('wwW', 'www'),
                            ('wWW', 'www'),
                            ('.com', 'com'),
                            ('com', '.com'),

                        ]
                        for old, new in replacements:
                            card = card.replace(old, new)

                        # ----------------------Phone------------------------------------
                        ph_pattern = r"\+*\d{2,3}-\d{3}-\d{4}"
                        ph = re.findall(ph_pattern, card)
                        for num in ph:
                            card = card.replace(num, '')
                        Phone_nos = ' , '.join(ph)

                        # ------------------Mail id--------------------------------------------
                        mail_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}\b"
                        mail = re.findall(mail_pattern, card)
                        Email_id = ''
                        for ids in mail:
                            Email_id = Email_id + ids
                            card = card.replace(ids, '')

                        # ---------------------------Website----------------------------------
                        url_pattern = r"www\.[A-Za-z0-9]+\.[A-Za-z]{2,3}"
                        url = re.findall(url_pattern, card)
                        URL = ''
                        for web in url:
                            URL = URL + web
                            card = card.replace(web, '')

                        # ------------------------pincode-------------------------------------------
                        pin_pattern = r'\d+'
                        match = re.findall(pin_pattern, card)
                        Pincode = ''
                        for code in match:
                            if len(code) == 6 or len(code) == 7:
                                Pincode = Pincode + code
                                card = card.replace(code, '')

                        # ---------------name ,designation, company name-------------------------------
                        name_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
                        names = []  # empty list
                        for i in card_info:
                            if re.findall(name_pattern, i):
                                if i not in 'WWW':
                                    names.append(i)
                                    card = card.replace(i, '')
                        name = names[0]
                        designation = names[1]

                        if len(names) == 3:
                            company = names[2]
                        else:
                            company = names[2] + ' ' + names[3]
                        card = card.replace(name, '')
                        card = card.replace(designation, '')

                        #city,state,address
                        new = card.split()
                        print(new)
                        if new[4] == 'St':
                            city = new[2]
                        else:
                            city = new[3]
                        # state
                        if new[4] == 'St':
                            state = new[3]
                        else:
                            state = new[4]
                        # address
                        if new[4] == 'St':
                            s = new[2]
                            s1 = new[4]
                            new[2] = s1
                            new[4] = s  # swapping the St variable
                            Address = new[0:3]
                            Address = ' '.join(Address)  # list to string
                        else:
                            Address = new[0:3]
                            Address = ' '.join(Address)  # list to string
                        st.write('')
                        st.write('###### :red[Name]         :', name)
                        st.write('###### :red[Designation]  :', designation)
                        st.write('###### :red[Company name] :', company)
                        st.write('###### :red[Contact]      :', Phone_nos)
                        st.write('###### :red[Email id]     :', Email_id)
                        st.write('###### :red[URL]          :', URL)
                        st.write('###### :red[Address]      :', Address)
                        st.write('###### :red[City]         :', city)
                        st.write('###### :red[State]        :', state)
                        st.write('###### :red[Pincode]      :', Pincode)

                        #====================insert into database=================================
                        try:
                            sql = "INSERT INTO card (name,designation,company,contact,email,website,address,city,state,pincode,image) " \
                                                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            val = (name,designation,company,Phone_nos,Email_id,URL,Address,city,state,Pincode,file_bytes)
                            cursor.execute(sql, val)
                            conn.commit()
                            conn.close()
                            st.success('Text extracted & successfully uploaded to database', icon="☑️")
                        except UniqueViolation as e:
                            st.toast("🔥 Data already present in DB, Please check !!!")



    def show_from_Db(self):
        conn = psycopg2.connect(database="card_data",host="localhost",user="postgres",password="root",port="5432")
        cursor = conn.cursor() 
        with st.spinner('Connecting...'):
            time.sleep(1)
        
            option = option_menu(None, ['Image data', "Update data", "Delete data"],
                                 icons=["image", "pencil-fill", 'exclamation-diamond'], default_index=0)
            
            cursor.execute("SELECT name,designation FROM card")
            rows = cursor.fetchall()
            names = [row[0] for row in rows]   
            designations = [row[1] for row in rows]

            # showing the image for selected name and designation
            if option=='Image data':
                left, right = st.columns([2, 2.5])
                with left:
                    selection_name = st.selectbox("Select name", names)     
                    selection_designation = st.selectbox("Select designation", designations)
                    if st.button('Show Image'):
                        with right:
                            cursor.execute("SELECT image FROM card WHERE name = %s AND designation = %s", (selection_name, selection_designation))
                            result = cursor.fetchone()
                                # Check if image data exists
                            if result is not None:
                                    # Retrieve the image data from the result
                                image_data = result[0]
                                # Create a file-like object from the image data
                                nparr = np.frombuffer(image_data, np.uint8)
                                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                                st.image(image, channels="BGR", use_column_width=True)
                            if result is None:
                                st.error("Image not found for the given name and designation.")
            
            #update data in database for selected name and designation
            elif option=='Update data':
                col1,col2=st.columns(2)
                with col1:
                    selection_name = st.selectbox("Select name to update", names)
                    selection_designation = st.selectbox("Select designation to update", designations)
                with col2:
                    # Get the column names from the table
                    cursor.execute("""SELECT column_name
                                FROM information_schema.columns
                                WHERE table_schema = 'public' AND table_name = 'card'""")
                    columns = cursor.fetchall()
                    column_names = [i[0] for i in columns if i[0] not in ['image','name','designation']]

                    # Display the selection box for column name
                    selection = st.selectbox("Select specific column to update", column_names)
                    new_data = st.text_input(f"Enter the new {selection}")

                    # Define the SQL query to update the selected rows
                    sql = f"UPDATE card SET {selection} = %s WHERE name = %s AND designation = %s"

                    # Execute the query with the new values
                    if st.button("Update"):
                        cursor.execute(sql, (new_data, selection_name, selection_designation))
                        # Commit the changes to the database
                        conn.commit()
                        st.success("updated successfully",icon="👆")


            #===delete data for selected name and dsignation===
            else:
                left,right=st.columns([2,2.5])
                with left:
                    selection_name = st.selectbox("Select name to delete", names)
                with right:
                    selection_designation = st.selectbox("Select designation to delete", designations)
                with left:
                    if st.button('DELETE'):
                        sql = "DELETE FROM card WHERE name = %s AND designation = %s"
                        cursor.execute(sql, (selection_name, selection_designation))
                        conn.commit()
                        st.success('Deleted successfully',icon='✅')
                #convert into dataframe using pandas
                
                st.write('')
                st.markdown('### Result')
                st.write('To provide a user-friendly interface, Bizcard utilizes Streamlit, a Python framework for building interactive web applications. Users can upload business card images through the Streamlit interface, and the application will process the images, extract the information, and display it on the screen. The application also provides options to view, update, and analyze the extracted data directly from the database.')
                st.info('The detected text on image might be inaccurate. Still application under development fixing bugs.There is lot to explore on easyOCR and openCV',icon='ℹ️')

            cursor.execute("SELECT * FROM card")
            myresult = cursor.fetchall()
            df=pd.DataFrame(myresult,columns=['name','designation','company','contact','email','website','address','city','state','pincode','image'])
            st.write(df)
            conn.close()


    def app_properties(self):
        with st.sidebar:
            selected = option_menu('Menu', ['Home',"Image to Text","Database"],
                    icons=["house",'file-earmark-font','gear'],
                    menu_icon= "menu-button-wide",
                    default_index=0,
                    styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#B1A3F7"}})
    
        if selected == 'Home':
            self.home_page()

        if selected == 'Image to Text':
            self.image_to_text_page()

        if selected=='Database':
            self.show_from_Db()


if __name__=="__main__":
    app=App()
    app.set_page_config()
    app.app_properties()
