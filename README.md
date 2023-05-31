# Chatroom Application

Chatroom is a simple chatroom application implemented in Python using sockets and Tkinter. It allows multiple clients to connect to a server and exchange messages with each other in real-time.

## Features

- **Multiple clients** can connect to the server.
- Clients can send messages that will be **broadcasted** to all connected clients.
- Clients can **see** when other **clients join or leave** the chatroom.
- Client can view and update their profile picture.
- **Text-to-Speech**: allows users to convert selected text to speech.
- **Web Search**: allows users to directly google search the selected text.
- **Find**: user can search for specific string within entire chat.

## Prerequisites

- Python 3.6 or higher
- External dependencies (specified in the **requirements.txt** file)

## Installation

1.  Clone the repository:

```shell
    git clone <repository-url>
```

2.  Navigate to the project directory:

```shell
    cd chatroom
```

3.  Create and activate a virtual environment:

```shell
    python -m venv venv
```
        For Windows:

```shell
    venv\Scripts\activate
```
        For macOS/Linux:

```shell
    source venv/bin/activate
```

4.  Install the required dependencies:

```shell
    pip install -r requirements.txt
```

5.  Start the server:

``` shell
    python server.py
```

6.  Run the client(s):

``` shell
    python client.py
```  

7.  Clients can now connect to the server using the provided IP address and port.	 


## Usage

    Clients can connect to the chatroom by running the client.py file and entering their name.
    Once connected, clients can send and receive messages in the chatroom.
    Messages sent by any client will be broadcasted to all connected clients.

## File Structure

The project consists of the following files:

***server.py***: The server-side implementation of the chatroom application.  
***client.py***: The client-side implementation for connecting to the chatroom.  
***requirements***.txt: The list of external dependencies required by the application.  
***README.md***: This file, providing an overview and instructions for the chatroom application.  


## Contributing

Contributions to the chatroom application are highly appreciated! If you find any issues, have suggestions for improvements, or would like to add new features, please consider contributing. To contribute, you can follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch from the main branch to work on your changes.
3. Make the necessary modifications and improvements to the codebase.
4. Write tests to ensure the stability and correctness of your changes.
5. Commit your changes and push them to your forked repository.
6. Open a pull request against the main repository, describing your changes in detail.

Please ensure that your contributions align with the following guidelines:

- Follow the existing coding style and conventions used in the project.
- Write clear and concise commit messages and provide an informative description in your pull request.
- Test your changes thoroughly and ensure they do not introduce any regressions.
- Provide proper documentation and comments to help others understand your contributions.

By contributing to the chatroom application, you'll be helping to improve its functionality, stability, and user experience for everyone. Thank you for your contributions in advance!.