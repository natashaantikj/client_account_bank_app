import sqlite3
import pprint
from PyInquirer import prompt
from datetime import datetime, date


pp=pprint.PrettyPrinter(indent=2)


#Creating connection with the database
connection=sqlite3.connect('bank/bank.sqlite3')
cursor=connection.cursor()



#Creating new client
class Client:
    def __init__(self,name,surname,embg,birth_date,location):
        
        self.name=name
        Client.validate_text(name)
        self.surname=surname
        Client.validate_text(surname)
        self.embg=embg
        Client.validate_embg(embg)
        self.birth_date=birth_date
        self.location=location
        Client.validate_text(location)
        self.date_of_creation_client=str(date.today().strftime('%d-%m-%y%y'))


        self.sql='insert into client (name,surname,embg,birth_date,location,date_of_creation_client) values (?,?,?,?,?,?);'
        cursor.execute(self.sql,(self.name,self.surname,self.embg,self.birth_date,self.location,self.date_of_creation_client))



    @staticmethod
    def validate_embg(embg):
        if len(embg)!=13:
            raise Exception('Invalid EMBG : {}'.format(embg))
        return True

    @staticmethod
    def validate_text(text):
        for element in text:
            if not element.isalpha():
                raise Exception('Invalid input: {} . Please enter a valid input. The value of this input has to be text.')
        return True


    
#Update client
class Update_client:

    def __init__(self,embg,subject,value):

        self.embg=embg
        self.subject=subject
        self.value=value

        sql_update_client="update client set ({})=? where embg = ?;".format(self.subject)
        update_tuple=(self.value,self.embg)

        cursor.execute(sql_update_client,update_tuple)
        result='The client with embg: {} has been updated.'.format(self.embg)
        print(result) 


#Delete client
class Delete_client:

    def __init__(self,embg):
        self.embg=embg

        self.sql_delete_client="delete from client where embg=?;"
    
        cursor.execute(self.sql_delete_client , (self.embg,))

        result="The client with embg: {} has been deleted.".format(embg)

        print(result) 

    
#Search for a client by embg
class Search_client_by_embg:

    def __init__(self,embg):
        self.embg=embg
        self.sql_search_embg="SELECT * from client inner join account where client.id=account.id_client and client.embg=?;"
        cursor.execute(self.sql_search_embg ,(self.embg,))
        result=cursor.fetchall()
        print(result)

#Search for a client by account number
class Search_client_by_account_number:
    def __init__(self,account_number):
        self.account_number=account_number
        self.sql_search_client_by_account_number="select * from client inner join account where account.id_client=client.id and account.account_number=?;"
        cursor.execute(self.sql_search_client_by_account_number ,(self.account_number,))
        result=cursor.fetchall()
        print(result)


# List of all clients
class List_all_clients:
    def __init__(self,ordered_by):
     
        self.ordered_by=ordered_by
        self.offset=0
        self.sql_list_all_clients="select * from client order by ({}) limit 5 offset ?;".format(self.ordered_by)
        self.sql_number_of_rows="SELECT count() from client;"
        self.number_of_rows=cursor.execute(self.sql_number_of_rows).fetchone()[0]


    def __next__(self):
        if self.offset> self.number_of_rows:
            raise StopIteration
        

        cursor.execute(self.sql_list_all_clients, (self.offset,))
        self.offset+=5
        result=cursor.fetchall()
        pp.pprint(result)
        return(result)



#Create an account
class Account:
    def __init__(self,account_number,balance,id_currency,id_type_of_account,id_client):


        self.account_number=account_number
        Account.validate_account_number(account_number)
        self.balance=float(balance)
        self.date_creation_account=str(date.today().strftime('%d-%m-%y%y'))
        self.id_currency= id_currency
        self.id_type_of_account= id_type_of_account
        self.id_client=id_client

        self.sql='insert into account (account_number,balance,date_creation_account,id_currency,id_type_of_account,id_client) values(?,?,?,?,?,?);'
        cursor.execute(self.sql,(self.account_number,self.balance,self.date_creation_account,self.id_currency,self.id_type_of_account,self.id_client))


    @staticmethod
    def validate_account_number(account_number):
        if len(account_number)!=8:
            raise Exception('Invalid input. The length of the account number has to be 8 digit number.')
        for number in account_number:
            if number.isalpha():
                return Exception("Invalid input. The value of account number has to be 8 digit number.")


#Update Account
class Update_account:
    def __init__(self,account_number,subject,value):
        self.account_number=account_number
        self.subject=subject
        self.value=value

        
        sql_update_account="update account set ({})=? where account_number = ?;".format(self.subject)
        update_tuple=(self.value,self.account_number)

        cursor.execute(sql_update_account,update_tuple)
        result='The account with account_number: {} has been updated.'.format(self.account_number)
        print(result) 


#Delete Account
class Delete_account:
    def __init__(self,account_number):
        self.account_number=account_number
        self.sql_delete_account="delete from account where account_number=?;"
    
        cursor.execute(self.sql_delete_account ,(self.account_number,))

        result="The account with account number: {} has been deleted.".format(account_number)

        print(result) 




option_prompt = {
    'type': 'list',
    'name': 'options',
    'message': 'Please pick an option: ',
    'choices': ['Insert (client or account)', 'Delete (client or account)', 'Update (client or account)', 'Search for a client', 'List of all clients']
}
answers = prompt(option_prompt)

if 'Insert (client or account)' in answers.values():
    option_prompt_insert = {
        'type':'list',
        'name':'insert_options',
        'message':'Insert (client or account):',
        'choices':['Client','Account']


    }
    insert_answers=prompt(option_prompt_insert)

    if 'Client' in insert_answers.values():
        print('Inserting new client. Fill in the following: ')

        name=input('Name:')
        surname=input('Surname: ')
        embg=input('EMBG: ')
        birth_date=input('Birth date (dd-mm-yyyy): ')
        location= input('Location: ')

        

        new_client=Client(name,surname,embg,birth_date,location)
        print("\nNew client has been added to the data base.")
    
    elif 'Account' in insert_answers.values():
        print("Inserting new account. Fill in the following: ")
        account_number=input("Account number: ")
        balance=float(input("Balance: "))
        id_currency=int(input("Id of the currency (<1>EUR  <2>USD  <3>MKD): "))
        id_type_of_account=int(input("Id of type of the account (<1>Current Account  <2>Term Deposit  <3>Savings  <4>Loans ):  "))
        id_client=int(input("Id of the client: "))
        new_account=Account(account_number,balance,id_currency,id_type_of_account,id_client)
        print("New account has been added to the data base.")

elif 'Delete (client or account)' in answers.values():
    option_prompt_delete = {
        'type':'list',
        'name':'delete_options',
        'message':'Delete (client or account): ',
        'choices':['Client','Account']

    }
    delete_answers=prompt(option_prompt_delete)

    if 'Client' in delete_answers.values():
        embg=input("Please enter the EMBG of the client that you want to delete: ")
        delete_client=Delete_client(embg)
    elif 'Account' in delete_answers.values():
        account_number=input("Please enter the account number of the account that you want to delete: ")
        delete_account=Delete_account(account_number)

elif 'Update (client or account)' in answers.values():
    option_prompt_update = {
        'type':'list',
        'name':'update_options',
        'message':'Update (client or account): ',
        'choices':['Client','Account']
    }

    
    update_answers=prompt(option_prompt_update)

    if 'Client' in update_answers.values():
        embg=input("Enter the EMBG of the client that you want to update: ")
        subject=input("Enter the subject that you want to update (name,surname,birth_date,location): ")
        value=input("Enter the value that you want to update: ")

        update_client=Update_client(embg,subject,value)

    elif 'Account' in update_answers.values():
        
        account_number=input("Enter the account number of the account that you want to update: ")
        subject=input("Enter the subject that you want to update (id_currency,balanace,id_type_of_account,id_client): ")
        value=input("Enter the value that you want to update: ")
        update_account=Update_account(account_number,subject,value)

elif 'Search for a client' in answers.values():
    print("Search a client by: ")
    option_prompt_search = {
        'type':'list',
        'name':'search_options',
        'message':'Search a client by: ',
        'choices':['EMBG','Account number']


    }
    search_answers=prompt(option_prompt_search)
    if 'EMBG' in search_answers.values():
        embg=input("Please enter the EMBG for the client: ")
        search_client_by_embg=Search_client_by_embg(embg)
    
    elif 'Account number' in search_answers.values():
        account_number=input("Please enter the account number: ")
        search_client_by_account_number=Search_client_by_account_number(account_number)

elif 'List of all clients' in answers.values():
    print('List of all clients ordered by: ')

    option_prompt_list = {
        'type':'list',
        'name':'list_option',
        'message':'List of all clients ordered by: ',
        'choices':['Name','Surname','Date of creation']

    }
    list_answers=prompt(option_prompt_list)

    if 'Name' in list_answers.values():
        ordered_by='name'
        list_of_clients=List_all_clients(ordered_by)
        list_of_clients.__next__()
        can_continue=input('Do you want to see the next 5 clients? (y/n)').strip().lower()
        while can_continue=='y':
            list_of_clients.__next__()
            can_continue=input('Do you want to see the next 5 clients? (y/n)').strip().lower()
        

    elif 'Surname' in list_answers.values():
        ordered_by='surname'
        list_of_clients=List_all_clients(ordered_by)
        list_of_clients.__next__()
        can_continue=input('Do you want to see the next 5 clients? (y/n)').strip().lower()
        while can_continue=='y':
            list_of_clients.__next__()
            can_continue=input('Do you want to see the next 5 clients? (y/n)').strip().lower()

    elif 'Date of creation' in list_answers.values():
        ordered_by='date_of_creation_client'
        list_of_clients=List_all_clients(ordered_by)
        list_of_clients.__next__()
        can_continue=input('Do you want to see the next 5 clients? (y/n)').strip().lower()
        while can_continue=='y':
            list_of_clients.__next__()
            can_continue=input('Do you want to see the next 5 clients? (y/n)').strip().lower()




connection.commit()
connection.close()

