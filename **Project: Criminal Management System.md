**Project: Criminal Management System Part 2**
**Introduction:**
This project builds upon the Criminal Management System developed in Part 1. It introduces additional features and functionalities to enhance the system's capabilities in managing criminal records and facilitating efficient law enforcement.

**Running the Application:**
To run the application, follow these steps:

1. **Install Dependencies:**
   Ensure that the necessary Python libraries are installed. You can do this by running the following command in your terminal:
   ```
   pipenv install
   ```
2. **Activate Virtual Environment:**
   ```
   pipenv shell
   ```

3. **Run the Application:**
   Navigate to the project directory and run the following command:
   ```
   python app/models.py
   ```
   This will start the application.

**Usage**
The application is a simple CLI (Command Line Interface) that allows users to interact with it through keyboard.
After Running the application do this :
- To add a new criminal, use this format in the terminal:
   ```
   python app/models.py  add-criminal
   ```
(Basically type or copy the command after you want to use)


**Code Overview:**

**1. Data Model:**
   The `app/models.py` file defines the data model for the application. It includes classes for representing criminals, crimes, and other relevant entities. Here's an example of the `Criminal` class:
   ```python
   class Criminal:
       def __init__(self, name, age, gender, crimes):
           self.name = name
           self.age = age
           self.gender = gender
           self.crimes = crimes
   ```
   This class represents a criminal with attributes such as name, age, gender, and a list of crimes they have committed.

**2. Database Configuration:**
   The application uses a SQLite database to store the criminal records. The database is configured in the `app/models.py` file. Here's an example of the database configuration:
   ```python
   from sqlalchemy import create_engine
   engine = create_engine('sqlite:///criminals.db')
   ```
   This code creates a connection to the SQLite database named `criminals.db`.

**3. CRUD Operations:**
   The application provides CRUD (Create, Read, Update, Delete) operations for managing criminal records. Here are some examples of these operations:
   - **Create:** To add a new criminal record, you can use the `add_criminal()` function:
     ```python
     def add_criminal(name, age, gender, crimes):
         criminal = Criminal(name, age, gender, crimes)
         db.session.add(criminal)
         db.session.commit()
     ```

### Author : Dave Mutisya
This is an open-source project under the MIT License. You are free to modify or fork this repositories
