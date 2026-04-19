<img width="2850" height="1768" alt="image" src="https://github.com/user-attachments/assets/aae7733e-5521-4abd-8e3a-e06265884138" />

<br>

**_Why does a FastAPI DELETE endpoint work in Postman but not in the browser?_**
<br>
Issue: Browser fails but Postman works
<br>
Cause: Browser only supports GET, FastAPI requires DELETE
<br>
Fix: Use Postman/curl/docs OR change method to GET
