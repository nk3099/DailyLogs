<img width="1447" alt="Screenshot 2025-06-01 at 8 31 26 PM" src="https://github.com/user-attachments/assets/bdd39fbd-c3c8-49d0-8cd3-ce88adeed31c" /># JWT Token Authentication:
-> the API doesn't track anything, ie. no info to be stored on API <br>
-> Instead, the client holds on the token - and provides to us (via a Header of the request) to access any resource/endpoint (that requires user to be logged in) <br>
-> API will validate if token is valid - thereby, API then sends backs the data. <br>

<img width="1437" alt="Screenshot 2025-06-01 at 8 04 32 PM" src="https://github.com/user-attachments/assets/35b673e7-e75a-4d10-817f-fe9d20467864" />

**Please note**: JWT token is not Encrypted. <br>
Instead made up of:<br>
a)Header<br>
b)Payload <br>
c)Signature (ie. Hashing) : whichcontains secret (which is not exposed)<br>

<img width="1417" alt="Screenshot 2025-06-01 at 8 12 33 PM" src="https://github.com/user-attachments/assets/5c66a686-c452-46d3-b5b7-ac94e98aba58" />

<img width="1457" alt="Screenshot 2025-06-01 at 8 24 29 PM" src="https://github.com/user-attachments/assets/efb4c560-f6ec-43f9-bcdc-7fbcefde4e25" />


# Logging of User:
-> We try to compare the User_typed_plain-password(string mostly) with Hashed_password(stored in DB) <br>
-> by converting the plain-password using Hash method and if matches, then token is passed to User.<br>
<img width="1447" alt="Screenshot 2025-06-01 at 8 31 26 PM" src="https://github.com/user-attachments/assets/723321fd-c584-4bc9-bc1c-94757eba47e4" />
