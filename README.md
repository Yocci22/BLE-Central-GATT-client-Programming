# BLE-Central-GATT-client-Programming

Write a Python BLE program (BLE Central) in a Linux host (Raspberry Pi 3) to communicate with a test app, say BLE Tool,  in an Android phone.

Your BLE program is required to demo some CCCD setting, such as setting the CCCD value of your App at the Android phone to 0x0002. 
     (Due to the limitations of  the "BLE Tool" app, the CCCD value might not be changed and viewed in the UI. It's OK to show the server log of the BLE Tool as a proof of your program.)

The test program in your Android phone can be others, for example, BLE scanner App (by Bluepixel). iPhone probably has a similar app.

对Raspberry Pi 3的操作：

1、首先连接电源线，网线，键盘，鼠标

2、打开yocci文件夹的终端

（非必须）安装bluepy：

sudo apt update

sudo apt install libglib2.0-dev

sudo apt install python3-pip

sudo pip3 install bluepy --break-system-packages

3、打开手机app（BLE Tool）--Gatt Server--Start Advertising

4、运行python脚本：

sudo python3 ble_central_cccd.py




