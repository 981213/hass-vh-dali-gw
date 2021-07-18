Intro
=============

Homeassistant component for VUNHO DALI Gateway with ethernet VH-DLGW-E

Product page: http://www.szyuanhao.com/product/675.html

Only DALI DT6 support implemented atm and I have no interest in maintaining it. Use at your own risk!

Usage
=============
Configure their gateway and scan for lights using their software. After that, add this component from Homeassistant integration page and fill the IP address and port. A light entity will be created for every discovered light during the last scan done by the gateway.