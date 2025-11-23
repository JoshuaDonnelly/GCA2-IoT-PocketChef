# Security

This section will outline all of the security measures we have implemented. As well as some that will be in the BETA version of our project. We will look at data in rest and in transit, 
throughout our architecture including places like: Pubunb, Apache server on our EC2 AWS instance and our Raspberry Pi itself.

---

# Security of the IOT Device
- The Raspberry Pi is configured with a non-default user, SSH Key authentication. We are looking at other security details to be added to this section, such as : Unnecessary services to be disabled to minimise surface attacks.

- Any config files such as `.env` contain secrets like our API keys, which are ignored using `.gitignore`. This ensures our credentials are not exposed to the client.

- Pubnub publish/subscribe keys are stored in the `.env` also. This should have chmod 600 permissions, so the owner (us) can only read/write.

- The device should always communicate outbound only and never expose ports publicly.

### SSH Security
- RSA Key-based authentication
- Root SSH is enabled, however is password protected.
- We must monitor our SSH logins.

# Security of communication channels (Pubnub -> AWS)

### Pubnub Access Control
- Channel access to be restricted to only allow authorised personnel
- Pubnub uses, AES-256 message encryption. This is a very secure encryption method. Also 
strict certification validation.
- All incoming data should be validated on our server, to make sure no malicious payloads make it through.
- We may introduce rate limiting to prevent DDoS or flooding.

### AWS Security
- Ports for HTTPS/HTTP requests are restricted to 443/80 respectively, which are needed for people to visit the site across the internet.
- Port 22 for this alpha, is needed to be open to enable other team members access to AWS. We cannot restrict to a single Admin IP yet, but that will be done in the BETA prototype.
- A ppk file is needed also to SSH into the database with a secure password requested on first login

# Database Security (AWS Hosted Apache/MySQL)

- A secure level 2 password is enabled to login to the database

- Logins are only permitted through private networking (localhost). This ensures no unwanted personnel access our database.

- The test db was left to enabled as it may be useful to us in the future.

- Database credentials are stored securely in the `.env` file, which of course is ignore by `.gitignore`.

- Automatic security firewall features are done via AWS security groups.

- Ports are set up as listed in the previous section.

# Data in transit
- IoT -> Pubnub -> Server
IoT messages to be encrypted using TLS encryption, which prevents man in the middle attacks.

- User -> Webserver (HTTPS)
Apache configured to use SSL certs, which encrypts our data and eliminates plaintext data.

- Internal AWS
Within AWS, service communication uses encrypted channels again ensuring no plaintext is visible.



