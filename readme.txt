/********************************************************
*		CPSC 852				*
*	     Final Project				*
*    File management and Synchronization		*
*							*
*	By,						*
*	 Pratik S Desai					*
*	 Nikhil Bendre					*
*********************************************************/

Requirements to run this code:
-----------------------------

	Server:
	------
	- Python v2.6 and above
	- host_sync.py and file_sync.py

	Client:
	------
	- Android virtual device using android-sdk 2.2
		(http://developer.android.com/guide/developing/tools/avd.html)
	- Scripting Layer for Android (SL4A)
		(http://code.google.com/p/android-scripting)
	- Python for android
		(http://code.google.com/p/android-scripting/downloads/detail?name=python_for_android_r1.apk&can=2&q=)
	- Transfer android_sync.py and file_sync.py to the AVD (must be sunning):
		$ adb push android_sync.py file_sync.py /sdcard/sl4a/scripts
	

Executing the Code:
------------------

	Start the server first

	Server:
	------
	the server runs the code as:
	$ ./host_sync <port-number>

	Client:
	------
	the python on Android cannot be given command line arguments. So we hardcode the host IP and port number
	1) On AVD, open up the menu
	2) Open SL4A
	3) Select the android_sync.py (edit the host IP, host port if necessary)
	4) Click on the terminal button to execute

