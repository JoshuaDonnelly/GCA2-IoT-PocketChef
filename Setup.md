**Make sure All TCP is set to 0.0.0.0/0 in AWS Security Groups launch-wizard-1**

**Import/Create pub_server.py & pub_reciever.py on AWS EC2**
**Import/Create pub_sender.py on Raspberry Pi**

**Create & activate a Python virtual environment**
Only for the AWS SSh

    # Navigate to your project folder
    cd ~/yourFolderHere

    # Create a virtual environment
    python3 -m venv venv

    # Activate it
    source venv/bin/activate

**Install dependencies inside the virtual environment**

    # Upgrade pip first (optional but recommended)
    pip install --upgrade pip

    # Install PubNub SDK and Flask
    pip install pubnub flask requests

**On PI**
**Install dependancies**

    sudo pip3 install pubnub requests --break-system-packages

**Reminder:**
Replace all placeholder keys in your Python files with your actual PubNub keys ("subscribe_key", "publish_key", "secret_key")
    
    pnconfig.subscribe_key = "subscribe_key"
    pnconfig.publish_key = "publish_key"
    pnconfig.secret_key = "secret_key"

Replace all "https://AWS:5000" lines in your Python files with your actual AWS IPV4
    
    EC2_SERVER = "http://AWS:5000"

**Run the server (token generator) in the background**
    
    # Run pub_server.py in background
    python pub_server.py &

    # Allow it to survive SSH disconnects
    disown

**Run the subscriber (receiver) in the background**
    
    # Run pub_receiver.py in background
    python pub_receiver.py &

    # Allow it to survive SSH disconnects
    disown

**Run the Pi sender**

    python pub_sender.py

**Verify running Python processes**
    
    ps aux | grep python

Look for lines like:
    
    ubuntu   12345  0.5  1.2 ... python pub_server.py
    ubuntu   12346  0.4  1.1 ... python pub_receiver.py

**Stop the server or receiver**
    
    # Kill the server
    kill 12345

    # Kill the receiver
    kill 12346


