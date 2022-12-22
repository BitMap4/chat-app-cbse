import tkinter as tk
import mysql.connector

conn = mysql.connector.connect(
        host='localhost',
        user ="login",
        password ="akshattesu",
        database='student'
    )
cursor = conn.cursor()

class ChatApp:
    def __init__(self, master):
        # Create the main window
        self.master = master
        self.master.title('Chat App')
        self.master.geometry('800x600')
        # Create a text field for displaying messages
        self.messages_text = tk.Text(self.master, height=40, width=110)
        self.messages_text.pack()
        # Create a text field for inputting messages
        self.message_input = tk.Entry(self.master, width=85)
        self.message_input.pack()
        # Create a button for sending messages
        self.send_button = tk.Button(self.master, text='Send', command=self.send_message)
        self.send_button.pack()
        # Create the messages table if it doesn't already exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                message TEXT
            )
        ''')
        # Load the existing messages from the database
        self.load_messages()
    def send_message(self):
        # Get the message from the input field
        message = self.message_input.get()
        # Insert the message into the database
        cursor.execute('''
            INSERT INTO messages (message) VALUES (%s)
        ''', (message,))
        conn.commit()
        # Clear the input field
        self.message_input.delete(0, 'end')
        # Load the updated list of messages
        self.load_messages()
    def load_messages(self):
        # Clear the messages text field
        self.messages_text.delete('1.0', 'end')
        # Get all of the messages from the database
        cursor.execute('''
            SELECT * FROM messages
        ''')
        messages = cursor.fetchall()
        # Display the messages in the text field
        for message in messages:
            self.messages_text.insert('end', message[1] + '\n')

# Create the main window and run the chat app
root = tk.Tk()
app = ChatApp(root)
root.mainloop()
