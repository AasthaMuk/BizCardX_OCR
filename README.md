# BizCardX_OCR

Video Link : [Click here](https://www.linkedin.com/feed/update/urn:li:activity:7144255729338580992/ "Click here")

### About the Project

It is a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR and opencv.

**Problem Statement:**

 The application should have the following features:

1. Install the required packages: You will need to install Python, Streamlit,
   easyOCR, and a database management system like SQLite or MySQL.
2. Design the user interface: Create a simple and intuitive user interface using
   Streamlit that guides users through the process of uploading the business
   card image and extracting its information. You can use widgets like file
   uploader, buttons, and text boxes to make the interface more interactive.
3. Implement the image processing and OCR: Use easyOCR to extract the
   relevant information from the uploaded business card image. You can use
   image processing techniques like resizing, cropping, and thresholding to
   enhance the image quality before passing it to the OCR engine.
4. Display the extracted information: Once the information has been extracted,
   display it in a clean and organized manner in the Streamlit GUI. You can use
   widgets like tables, text boxes, and labels to present the information.
5. Implement database integration: Use a database management system like
   SQLite or MySQL to store the extracted information along with the uploaded
   business card image. You can use SQL queries to create tables, insert data,
   and retrieve data from the database, Update the data and Allow the user to
   delete the data through the streamlit UI
6. Test the application: Test the application thoroughly to ensure that it works as
   expected. You can run the application on your local machine by running the
   command streamlit run app.py in the terminal, where app.py is the name of
   your Streamlit application file.
7. Improve the application: Continuously improve the application by adding new
   features, optimizing the code, and fixing bugs. You can also add user
   authentication and authorization to make the application more secure.

### Tools and Techniques :

**Python Libraries used :** pandas , numpy , streamlit , easyocr, opencv, psycopg2

### Workflow :

1. Home page:

   ![1703326254084](image/README/1703326254084.png)
2. Image to Text Page : Upload an image and then extract the text and upload it into database.

   ![1703326302510](image/README/1703326302510.png)

   ![1703326328150](image/README/1703326328150.png)
3. Show Image, Update Data and Delete Data :

   Show Image button -> shows the image of the business card for a particular name

   ![1703326449568](image/README/1703326449568.png)

   ![1703326535084](image/README/1703326535084.png)

   ![1703326565462](image/README/1703326565462.png)
