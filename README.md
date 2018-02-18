# Audit Cleanse
---
This program is developed for technicians to have the ability to audit the devices in their IT Office, so long as their branch uses ServiceNow as their main asset host. Currenty, the program only works for Liberty University staff members with the subdomain of `liberty.service-now.com` or `libertydev.service-now.com`. The intention for this project is the ability for it to expand to any subdomain, but has only been tested and verified on Liberty's network.

The program has several main audit forms, which will be covered in the following sections.


### Package Requirements
---
This program requires the following libraries to be installed, and the comments following each are
the reasons for each. Use `$ <sudo> pip install [package]` to set up each package.
(If Python 2 is your system default, you may need to use 'pip3' instead.

* pyperclip - To copy the list of items in your clipboard. Specifically used to capture the list
  for the storage and loaner audits. This may not be needed in future commits.

* pysnow - The primary integration of ServiceNow into python, and functions/queries to pull
  and push information from and to ServiceNow.

* colorama - To color the output of certain parts of the program. Specifically during the
  scanning process, where the items are colored differently based on certain points.
  For example, 'Work In Progress' might be colored red, and 'Open' is blue.

* termcolor - Required by colorama, this colors entire terms.

* getch - To get characters in console without requiring the user to press 'Enter'. This is
  particularly useful in a Wait() command, which waits for the user to press any key, not
  specifically requiring 'Enter'.

