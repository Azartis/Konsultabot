@echo off
echo Finding your computer's IP address for mobile app configuration...
echo.
echo Your IP addresses:
ipconfig | findstr /i "IPv4"
echo.
echo Copy one of these IP addresses and use it in the mobile app configuration.
echo The format should be: http://YOUR_IP_ADDRESS:8000/api
echo.
pause
