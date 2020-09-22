tutorial = '''1 Main window

1.1 Main menu: Open->, Side-by-side report, Open recent report->, help->, Exit
1.1.1 Menu open-> New config, Open config, Recent config->
1.1.1.1 New config
	Create a new blank configuration (see 2.0)

1.1.1.2 Open config
	Open an existing configuration chosing a file on the list folder

1.1.1.3 Recent conifg -> Clear list, <recente config list.cnf>
1.1.1.3.1 Clear list
Clear the recent config list

1.1.1.3.2 <recente config list.cnf>
	Open config from a list of last 20 configs recently opened

1.1.2 Side-by-side report
	Open the side-by-side window (see 3.0)

1.1.3 Open recent report: Busload report ->, Side-by-side report ->
1.1.3.1 Busload report: Clear list, <recente reprot list.html>
1.1.1.3.1 Clear list
	Clear the recent report list
	
1.1.1.3.2 <recente report list.html>
	Open report, html file, from a list of last 20 report recently opened
	
1.1.3.2 Side-by-side report: Clear list, <recente side-by-side list.html>
1.1.1.3.1 Clear list
	Clear the recent side-by-side list
	
1.1.1.3.2 <side-by-side report list.html>
	Open side-by-side, html file, from a list of last 20 side-by-side recently opened

1.1.4 Help: Welcome, Tutorial, About
1.1.4.1 Welcome
	Open a window with a welcome window with information about the main features of this app

1.1.4.2 Tutorial
	Open this tutorial

1.1.4.4 About
	Open the about window with this app version, email of the author and rights

1.2 Main area
	This area is used to manage the windows used in this app.
	
1.3 Status bar
1.3.1 Responsible
	This area is used to configure the user of this app. Every time a new bank config is created (see 2.0) in order to automatically fulfill the field 'responsible'
	
1.3.2 Hint
	In this area are presented basic hints to how use the current window or frame opened.

2 Configuration window
2.1 New configuration
	A new configuration is a window with default parameters configured. 
	If there is a name in the 'responsible' status bar (see 1.3.1) the field 'responsible' is automatically fulfilled.
	A config name is automatically created with a sequential number from 0 to 999 each time a new configuration is created.
	see 2.2 for general information about configuration's definition.

2.2 General uses
2.2.1 Config menu: Save, Save as, Duplicate, Run calc, Exit
2.2.1.1 Save
	Save the current configuration. If it's a new configuration or the file name already exists or config name was changed, it will work as Save as (see 2.2.1.2)
	
2.2.1.2 Save as
	This option will open a window asking to find a folder location and file name.
	
2.2.1.3 Duplicate
	This option will duplicate the current configuration, after save it, in a new configuration window. The new configuration will have the same parameters and a config name generated as a new config (see 2.1)

2.2.1.4 Run Calc
	The current config should be saved before proceed with the busload calculation. This opetion will apply the configuration to the DBC and run the calculation. The result is presented in sequence (see xxx)
	
2.2.1.5 Exit
	Ask to save the current configuration and close the config window.
	
2.2.2 Basic fields: DBC file, baudrate, bit stuffing, id size
	In order to proceed with the Calc of busload, the only required field is the DBC file, otherwise, some other fields are important in order to correct adjust the DBC parameters. 
	
	
2.2.2.1 DBC file
	Represents the location and the name of the .dbc file. The .dbc file is checked and only valid .dbc is accepted.

2.2.2.2 baudrate
	Baudrate is the speed of the newtwork in kbps.
	
2.2.2.3 bit stuffing
	This information is the percentage of bits added to the message length. 
	The CAN message has a synchronization mechanism that add one inverted bit signal at each 6 bits with the same level. This mechanism, called bit stuffing, made the total bit length increase, depending of the message content. 
	This field simulate the bit stuffing adding the extra size.

2.2.2.4 id size
	This field informs the standard bit size to be used during the calc.
	
2.2.3 Information field: Title, Description, Graph type
2.2.3.1 Title
	Title is used to identify the the particular calculation on the report (see xxx)

2.2.3.2 Description
	This field is used to better describe, in details,  the calculation on the report (see xxx)

2.2.3.2 Graph type
	This field is used to chose the way to present the busload result on the report (see xxx)
	
2.2.4 Message manipulation: Erase ECU, Erase Message, Modify message, Add message
	Message manipulation is the way to create variation of the current DBC. The manipulation does not modify the DBC. It's only used to apply the changes during the calculation. In some way, is like to create a small piece of DBC. This piece is combined to simulate variation of the original DBC in order to have a very fast analysis of new messages and modules.
	
2.2.4.1 Erase ECU
2.2.4.1.1 Search
	It's possible to look for a ECU in the DBC's list. At each click, on the button the next item is found until the end of the list.
	
2.2.4.1.2 DBC ECU's list
	It's possible to select an ECU with the left mouse button. A blue garbage signal will represent the ECU is selected to be erased from the DBC. The ECU will be added in the Selected ECU's list.
	Erase an ECU means all exclusive messages from that ECU will be 'erased' during the busload calc. If there are other modules sending the same message, that message will not be erased.
	Clicking in an ECU with the blue garbage will change to red garbage and the '*' will appear in the Selected ECUs list. It means all messages will be erased, even if it is sending from other modules.
	Another click will remove the ECU from the Selected ECUs list.
	Clicking on ECU with the right mouse button will present a list of messages sent by that ECU.
		
2.2.4.1.3 Selected ECUs 
	This is the list with all selected ECUs to be deleted form the DBC during the busload calc (see 2.2.4.1.2).
	Clicking in an ECU in this list will remove it.

2.2.4.1.4 Clear list
	This button will clear all ECUs in the list.
	
2.2.4.1.5 Cancel
	This button will cancel all changes and return to the configuration frame.

2.2.4.1.6 Confirm
	This button will save all changes and return to the configuration frame.
	
2.2.4.2 Erase Message
2.2.4.2.1 Search
	It's possible to look for a Message in the DBC's list. At each click, on the button the next item is found until the end of the list.
	
2.2.4.2.2 DBC Message's list
	It's possible to select a Message with the left mouse button. A red garbage signal will represent the Message is selected to be erased from the DBC. The Message will be added in the Selected Messages list.
	Erase an Message means that message will be 'erased' during the busload calc.
	Another click will remove the Message from the Selected Messages list.
	Clicking on Message with the right mouse button will present a list of senders ECU's for that message.
		
2.2.4.2.3 Selected Messages 
	This is the list with all selected Messages to be deleted form the DBC during the busload calc (see 2.2.4.2.2).
	Clicking in an Message in this list will remove it.

2.2.4.2.4 Clear list
	This button will clear all Messages in the list.
	
2.2.4.2.5 Cancel
	This button will cancel all changes and return to the configuration frame.

2.2.4.2.6 Confirm
	This button will save all changes and return to the configuration frame.

2.2.4.3 Modify message
2.2.4.3.1 Search
	It's possible to look for a Message in the DBC's list. At each click, on the button the next item is found until the end of the list.
	
2.2.4.3.2 DBC Message's list
	On this list is possible to see the list of DBC messages and the message size and cycle time.
	Click in the message will select it to be modified, on the Selected messages list. A pencil in from the message means it is selected to be modified.
	If the option Auto set values is selected, the message will be added to Selected message with the values in that boxes.
	Clicking again in a message already selected, the pen will disappear and the message will be removed from the selected messages list.

2.2.4.3.3 Auto set values
	This option permits an easy way to modify several messages with a simple click. The values of cycle time and size of the message on the box will be automatically used to modify the message when it is selected (see 2.2.4.3.2)
		
2.2.4.3.4 Selected Messages 
	This is the list with all selected Messages to be modified form the DBC during the busload calc (see 2.2.4.3.2).
	The cycle time and the message size information are displayed in an text box in order to be modified.
	Clicking in an Message in this list will remove it.

2.2.4.3.5 Clear list
	This button will clear all Messages in the list.
	
2.2.4.3.6 Cancel
	This button will cancel all changes and return to the configuration frame.

2.2.4.3.7 Confirm
	This button will save all changes and return to the configuration frame.
	
2.2.4.4 Add message
2.2.4.4.1 Messages added
	This list shows the list of message added, including the message id, cycle time and message size.
	Clicking in a message in this list will remove it from the list. Removing the message, the values are automatically copied to the entry fields bellow giving the opportunity to change the values and add it again, or not.

2.2.4.4.2 Clear list
	This button will clear all Messages in the list.
	
2.2.4.4.2 Auto generate values
	This option is a fast way to auto generate a message. The message name will created with an incremental number ate the end. The ID will be automatically increased at each new generation. The cycle time and id size generated will be the same used in the last message addition.
		
2.2.4.4.3 Message generation fields: Message name, Cycle time, size, id
	All those fields are required in order to create a new message. Missing or wrong values will not add a message, and the fields will be removed.
	
2.2.4.3.4 Cancel
	This button will cancel all changes and return to the configuration frame.

2.2.4.3.5 Confirm
	This button will save all changes and return to the configuration frame.	

2.3 Outpu report: log result, html, csv
2.3.1 log result
	After each busload calculation the result is presented with all information tracking the configuration and dbc file used. 
	It's possible to save the log in a .txt file.
	If the option to save the HTML report is set, the button to open the HTML report will appear and the report is added to the main menu recent report list (see 1.1.1.3.2).
	If the option to save the CSV report is set, the button to open the CSV report will appear.
	
2.3.2 HTML report
	The HTML report is a complete report with all information regarding configuration and dbc file used, including the log (see 2.3.1).
	In addition at all information the busload result is presented in dynamic graph, generated in Java Script. It's possible select the type of graphic on the configuration options (see 2.2.3.2).
	The HTML report is available on the main menu recent report list (see 1.1.1.3.2).
	
2.3.3 CSV report
	The CSV report is a complete report with all information regarding configuration and dbc file used, including the log (see 2.3.1).
	The CSV report permits to open the report in the MS EXCEL to addition analysis on the result.
	
3 Side-by-side report
3.1 window
	Side-by-side is an option to see the results from several HTML report in only one document. The output is an HTML whit Java Script features, permitting select one by one the results we would like to see.
	
3.1.2 Side-by-side file name
	In order to save the output, is necessary to define a name to the output. It's possible to auto generate a name, clicking in the button beside.

3.1.3 HTML's report	list
	A list HTML is present with all valid HTML reports. When a HTML report is generated, a meta data is embedded in order to permit to be easily reused to generate the side-by-side function. Only HTML generated with the appropriated version of Busload calc could be used.
	One or more HTML report should be selected to generate a side-by-side report.

3.1.4 Clear selection
	This button will clear all selection in the list.

3.1.5 Select all
	This button will select all reports in the list.
	
3.1.6 Side-by-side report
	This button will generate the side-by-side report and open it in the default browser.
	The side-by-side report will be added to the main menu recent side-by-side report list (see 1.1.3.2)

3.1.7 Close
	This button will close the side-by-side window'''

	
	