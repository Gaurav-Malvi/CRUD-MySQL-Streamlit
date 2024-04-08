import mysql.connector
import streamlit as st
from validate_email import validate_email
    

# Establish a connection with MySQL serve
my_database = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "your_password",
    database = "mydb"
)


my_cursor = my_database.cursor()
print("Connection Established")


# Create Streamlit app
def main():
    st.title("CRUD with MySQL")

    # Display options of CRUD
    option = st.sidebar.selectbox("Select an Operation", ("Create", "Read", "Update", "Delete"))

    # INSERT or CREATE
    if option == "Create":
        st.subheader("Create Record")

        name = st.text_input("Enter Name")
        email = st.text_input("Enter Email")

        # to insert record at first available id
        my_cursor.execute("select * from users")
        occupied_id = set(row[0] for row in my_cursor.fetchall())
        available_id = 1
        while available_id in occupied_id:
            available_id += 1


        if st.button("Create"):

            # if email or name field is empty
            if not name or not email:
                st.warning("Please enter the field!")
            
            # check if email is valid
            elif not is_valid_email(email):
                st.warning("Invalid Email Address")

            # insert record
            else:
                sql = f"insert into users(id, name, email) values({available_id}, '{name}', '{email}')"
                my_cursor.execute(sql)
                my_database.commit()
                st.success("Record created successfully")
            
    
    # READ
    elif option == "Read":
        st.subheader("Read Record")

        # fetch the records
        my_cursor.execute("select * from users")
        result = my_cursor.fetchall()

        # check if there is any records
        if not result:
            st.warning("No records exist!")

        # display the records
        else:
            records = [dict(zip(my_cursor.column_names, row)) for row in result]
            st.table(records)

    # UPDATE
    elif option == "Update":
        st.subheader("Update Record")

        id = st.number_input("Enter ID", min_value = 1)
        name = st.text_input("Enter New Name")
        email = st.text_input("Enter new Email")

        if st.button("Update"):

            # check if id exist
            my_cursor.execute("select * from users where id = %s", (id,))
            result = my_cursor.fetchone()
            if not result: 
                st.warning("ID not exist")
            
            # if id or name or email is empty
            elif not name or not email or not id:
                st.warning("Please enter the field!")

            # check if email is valid
            elif not is_valid_email(email):
                st.warning("Invalid Email Address")

            # update the record at given id
            else:
                sql = "update users set name = %s, email=%s where id = %s"
                val = (name, email, id)
                my_cursor.execute(sql, val)
                my_database.commit()
                st.success("Updated Successfully")
        

    # DELETE
    elif option == "Delete":
        st.subheader("Delete Record")

        id = st.number_input("Enter ID", min_value = 1)


        if st.button("Delete"):

            # check if id exist
            my_cursor.execute("select * from users where id = %s", (id,))
            result = my_cursor.fetchone()
            if not result: 
                st.warning("ID not exist")
            
            # delete the record at given id
            else:
                sql = "delete from users where id = %s"
                val = (id,)
                my_cursor.execute(sql, val)
                my_database.commit()
                st.success("Deleted Successfully")
            

           
# for email string validation
def is_valid_email(email):
    return validate_email(email)


if __name__ == "__main__":
    main()
