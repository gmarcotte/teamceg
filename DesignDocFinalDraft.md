

&lt;html&gt;




&lt;head&gt;



&lt;title&gt;

TeamCEG's Design Document

&lt;/title&gt;


<h1>TeamCEG's Design Document</h1>
<h3>March 13, 2009</h3>


&lt;/head&gt;





&lt;body&gt;


<h2>Outline</h2>
<p><a href='#identification'>Identification</a><br>
<a href='#primarygoal'>Primary Goal</a><br>
<a href='#overview'>Overview</a><br>
<a href='#userscenarios'>User Scenarios</a><br>
<a href='#architecture'>Architecture</a><br>
<a href='#milestones'>Milestones</a><br>
<a href='#risks'>Risks & Open Issues</a>
<br>
<br>
Unknown end tag for </ul><br>
<br>
<br>
<br>
Unknown end tag for </p><br>
<br>
<br>
<br>
<br>
<a><h2>Identification:</h2></a>
<p><ul>
<li>Project Name: Pairgramming</li>
<li>Group Name: TeamCEG </li>
<li>Group Member Names: Garrett Marcotte (<i>marcotte</i>), Christina Ilvento (<i>cilvento</i>), Ellen Kim (<i>ellenkim</i>)</li>
<li>Project Manager: Ellen Kim (<i>ellenkim</i>)</li>
<li>URL: <a href='http://code.google.com/p/teamceg/'>http://code.google.com/p/teamceg/</a></li>
</ul></p>


<a><h2>Primary Goal:</h2></a>
<p>
<blockquote>The primary goal of this project is to create a web-based interface for fully collaborative programming.</p></blockquote>


<a><h2>Overview:</h2></a>
<p>
<blockquote>Paired programming is a commonly used learning and coding practice introduced and encouraged in COS 126, 226, and 217 at Princeton.  However, students often have difficulty scheduling blocks of time to code together due to their busy schedules.  Pairgramming saves students time by enabling them to pair program remotely.  Pairgramming will save students from hikes out to Friend Center through the snow, and let them work together in spare half hour between classes or before bed, and also make working together over breaks or while traveling easier.</p>
<p>
Our solution will include the ability to pair program, where the "driver" is able to edit code and build/debug/run and the "passenger" can observe the driver's actions, and also the ability for each partner to independently work on the same project where each partner can work on different sections of the code in a subversion-like check-out environment.</p>
<p>
Features will include real-time two-way audio communication, a functional console with monospaced font and basic commands (compile, run, debug), an interactive text editor with syntax highlighting, a basic text chat, a revision browser (using Subversion), a collapsible tree-style file navigator, and the ability to "ink" or highlight text.</p>
<p>
The most well-known example of a web-based multiple user text editor is Google Documents, where two or more people can log in and edit the same document at the same time, and see changes made by the other users in almost real-time (update times may vary from less than 1 second to almost 1 minute).  However, our text will be updated frequently and consistently enough that the observing partner will be able to watch their partner code.  Additionally, our shell will also be seen by the other partner.</p>
<p>
The web application will probably be coded in Python using Pyjamas (GWT in Python) for client-side and user interface, and Django for server-side.  The testbed server is Christina's Old Mac set up with VMWare to run Ubuntu WebServer with Apache 2.0 and MySQL.</p></blockquote>


<a><h2>User Scenarios:</h2></a>
<h3>Registration, Modes and Project Creation</h3>
<blockquote><p><b>New Student</b>
Peng is a student in COS 217 who has not registered with Pairgramming.  He is starting the Buffer Overrun assignment with his partner Matt, who has already registered with Pairgramming.  He goes to the Pairgramming login page and creates a new username and password with our server.  Our login will be separate from Princeton's LDAP.  Peng will be able to create the new project with his new username and password without any additional confimation steps.</p>
<img src="login.jpg"<br>
ALT="preliminary screenshot of login page"<br>
BORDER=1><br>
<p><b>Returning Student, New Partner, New Project</b>
Garrett is a student in COS 226. He is already registered with Pairgramming. Garrett wants to work with Kathleen, who is also registered with Pairgramming, on a new project. The two have never worked together using Pairgramming. Garrett goes to the Pairgramming login page and enters his username and password; our server verifies his account and sends him to his home screen, where he enters Kathleen's Pairgramming username. No projects will populate the project selection dropdown list, because the two users have no projects in common. Garrett selects "Create new project", the only option in the list. Garrett then clicks "Create our project!" and enters the project name, and the Pairgramming application loads in the browser.</p>
<img src="login2.jpg"<br>
ALT="preliminary screenshot of login page"<br>
BORDER=1><br>
<p><b>Students Pair Programming</b>
Christina is a student in COS 217.  She is starting the Heap Manager assignment with her partner Ellen.  She goes to the login page, enters her username, password, and partner's name.  She selects HeapManager from the project selection dropdown list and opens the project.  She logged in before Ellen so she becomes the "driver" (partner who codes) by default.  Ellen logs in by the same protocol from her computer elsewhere.  Christina sees Ellen join the project and clicks to initiate Audio; Ellen sees the flashing popup and confirms.  They greet each other and Christina starts coding. Christina types, Ellen can see Christina's typing in the editor and console. They communicate via audio, text chat, and by highlighting relevant lines.</p>
<p>Christina and Ellen decide to split up so Ellen can write a function they need in an auxiliary file.  Christina selects Independent Mode in the options bar.  The layout changes to show Eavesdrop, a small version of Ellen's editor window which updates every 10 seconds; the Eavesdrop window shades out gray when the other partner is inactive for more than 20 seconds. When Ellen finishes writing the function, she tests it against the version of the code that she and Christina last edited in collaborative mode.  She decides to make a change in the file she and Christina were just editing, but discovers when she goes to the file tree to open it that Christina is already editing this file, so she cannot modify it.  Ellen fixes up the changes she has already made, and when she is satisfied that her changes won't break the existing code, she tells Christina over text chat that she is ready to go back into collaborative mode.</p>
<p>Ellen lets Christina know she's ready to switch back to collaborative mode and presses Synch to synchronize her changes with the server's version of the files, and then selects "Driver" because she wants to code this time.  Christina finishes her last changes, clicks Synch, and accepts "Passenger" role.  They are now switched back to collaborative mode and they continue coding together.</p></blockquote>

<h3>Controls and Windows</h3>
<img src="layout.jpg"<br>
ALT="preliminary screenshot of login page"<br>
BORDER=1><br>
<blockquote><p><b>Audio Controls</b>
Audio will be disabled by default when the second user logs into a session. If audio is unavailable (no microphone input from one of the users) the audio controls will be grayed out. If audio is available, when the second user logs in, the first user will be notified and must click the audio controls to enable audio communication. When one of the users mutes their microphone input or the other user's audio feed, both users' audio controls turn red.</p>
<p><b>Ink</b>
All text in the editor and console can be highlighted by either user in collaborative mode to point out specific areas that their partner may want to look at. The highlighted regions can be cleared by pressing the clear button. Each user can also select different colors of highlighter.</p>
<p><b>Window Ping/Flash</b>
Every window can be "pinged" or "flashed" by clicking a button to cause the window to flash in the other user's view and make a noise. The purpose of this functionality is to allow a user to draw their partner's attention to a specific window if they are worried that their partner is zoning out, or is not paying attention to them. This will be especially useful during times when audio is disabled or not available.</p>
<p><b>File Tree</b>
The file tree will allow users to create, open, and delete files in their project on the server. In independent mode, it will also indicate if a file has been modified by the other user.</p>
<p><b>Text Chat</b>
The text chat window will be similar to other chat applications, such as iChat, gChat, AIM, etc. Additionally, users will be allowed to use special tags to transmit formatted code in the form <pre>
<pre><code>    int hereIsSomeCode(void) {<br>
        for (int i = 0; i &lt; n; i++) <br>
            // do something<br>
        return 0;<br>
    }<br>
</code></pre>
</pre>in the spirit of GoogleCode, etc. to allow code to be transmitted in a useable form.</p>
<p><b>Editor</b>
The editor will look similar to other code editors such as Emacs, and will support automatic smart syntax coloring. All changes in the editor on the driver side will be reflected on the passenger side with as little delay as possible, and only the driver will be able to edit in collaborative mode. The passenger can highlight sections of the code using ink in collaborative mode to point out areas that they want to discuss, and can also scroll up and down in the editor to view different parts of the code in the same file. In independent mode, each user can manipulate the editor independently.</p>
<p><b>Console</b>
The rules for the console are the same as for the editor. The driver can interact with console in collaborative mode, and each user can interact separately with the console in independent mode. The console will have a limited functionality similar to the bash <a href='shell.md'>shell</a>, but will not support using plain text editors, modifying, creating or deleting files, etc. within the console window. Our hope is that users will not have to learn any new commands, but will simply have to pay attention to what sort of commands are not supported.</p>
<p><b>Eavesdrop</b>
The eavesdrop window appears only in independent mode, and shows each user a snapshot of the other users editor window updating about every 10 seconds. When the other user has been inactive (in the editor <i>and</i> the console for more than 20 seconds, the eavesdrop window turns grey. All pings/flashes to the eavesdrop window are reflected in the other user's eavesdrop window, not their editor or console.</p></blockquote>


<a><h2>Architecture:</h2></a>
<p>
Our application will have two main components: a client-side web application that<br>
the user interacts with via a web browser, and server-side code that the client<br>
application interacts with via AJAX.  We want our application to be as responsive<br>
as possible, ideally to the point that the user is not consciously aware that he<br>
is using a web application, so the AJAX communication will be of the utmost<br>
importance.</p>
<p>
The client-side application will be developed in Python using the Pyjamas toolkit.<br>
An almost exact port of Google Web Toolkit, Pyjamas allows for advanced web interfaces<br>
to be defined in a standard programming language (Python) and then compiled into<br>
Javascript to be run in the user's web browser.  We selected Pyjamas over GWT for three<br>
primary reasons.  First, our server-side code (discussed next) will also be in Python,<br>
and for ease of implementation it made sense to use the same language across our application,<br>
so that we could use the same testing, debugging and style-checking tools for all code.<br>
Second, Pyjamas has an extension called Pyjamas-Desktop (for which no corollary exists in GWT)<br>
that allows a Pyjamas web application to be run as a desktop application, and which could<br>
allow additional functionality and features should we have the time to implement them.  Finally,<br>
GWT did not show any significant advantages over Pyjamas.  They both compile into Javascript, so<br>
performance is not an issue.  Almost all of the GWT tutorials and examples that Google prepared<br>
have been adapted to Pyjamas.  And the development team and use of Pyjamas seems widespread<br>
enough to ensure that the code is stable and functional, and that we will be able to find<br>
documentation and support.</p>

<h3>Client-Side Interface (class hierarchy)</h3>
<blockquote>Container:<br>
<ul>
<li>Auto-updates with server to keep content current</li>
<li>A single region of content in the user's browser</li>
<li>Can be moved via drag-and-drop or resized</li>
<li>Can be "popped out" into a new browser window (e.g. for full-screen)</li>
<li>Can be "flashed" with a blinking color overlay (and optional sound effect) to alert the user to an item of interest.</li>
</ul>
Sketchpad extends Container (this is a wish-list feature):<br>
<ul>
<li>Full-window overlay that allows collaborative drawing/sketching.</li>
<li>Basic drawing tools: pen width, pen color, eraser, clear</li>
<li>Drawings can be saved as images to server</li>
</ul>
FileNavigator extends Container:<br>
<ul>
<li>Expandable tree navigation structure for all files in the project</li>
<li>Color-coding of files to indicate in-use/modified status</li>
</ul>
ConfigurationPanel extends Container:<br>
<ul>
<li>Allows user to control the application and customize the interface, with options for:<br>
<ul>
<blockquote><li>Setting the flash color and rate for Containers.</li>
<li>Turning sound effects on and off.</li>
<li>Changing the mode of operation (independent, collaborative, sketchpad)</li>
<li>Opening new projects</li>
<li>Customizing syntax highlighting</li>
</blockquote></ul>
</li>
</ul>
AudioControl extends Container:<br>
<ul>
<li>Iconic and color-coded indicators for connectivity</li>
<li>Sliders and mute buttons for microphone and speaker volume</li>
</ul>
RevisionBrowser extends Container (this is a wish-list feature):<br>
<ul>
<li>Displays summary of all past versions of a selected file</li>
<li>Allows for reverting, loading diffs, or loading the past revision into a CodeView container</li>
</ul>
TextContainer extends Container:<br>
<ul>
<li>For displaying text content</li>
<li>Allows any portion of text to be "highlighted" by any user, which causes that text to be highlighted on the screen of any user with that container open.  Highlighting is color-coded by user.</li>
</ul>
CodeView extends TextContainer:<br>
<ul>
<li>For displaying significant amounts of code</li>
<li>Built-in syntax highlighting, determined from filename.</li>
<li>Monospaced font</li>
<li>Line numbers</li>
<li>Not editable</li>
</ul>
CodeEdit extends TextContainer:<br>
<ul>
<li>Editable</li>
<li>Auto-saves to a user-level working copy on server periodically</li>
</ul>
TextEntry extends TextContainer:<br>
<ul>
<li>Has a small box for user to enter text, and a larger non-editable box to show the results of previously entered text.</li>
</ul>
Console extends TextEntry:<br>
<ul>
<li>Offers simulation of a very basic console.  Available commands include compile, run, and debug.</li>
</ul>
TextChat extends TextEntry:<br>
<ul>
<li>A basic chat box for text communication between users.</li>
<li>Timestamped entries</li>
<li>Color-coding of usernames</li>
</ul></blockquote>

<h3>Server-Side Functionality</h3>
<p>
The server-side application will be developed in Python and run on top of the Django web framework.<br>
The primary responsibilities of the server-side code will be management of persistent data, providing<br>
an administrative interface for the application, maintaining communication between users, and<br>
facilitating AJAX communications with the client session.</p>
<p>
The major models we will be storing are:<br>
<ul>
<li>User: basic user information</li>
<li>Class: for organizing users and projects into courses and tracking professor/TA/student status</li>
<li>Project: details about a project, especially file storage information.</li>
<li>Interactions: a single content item to be shared between users (e.g. a chat message, console command, etc.</li>
</ul>
</p>
<p>
The AJAX communication between the client and the server will be performed using the JSON protocol,<br>
and facilitated with the JSONRpc Python library.</p>
<p>
We are currently running our software on a Macbook running Ubuntu via VMWare. The database<br>
storage is via MySQL.  Our objective is to be as flexible as possible and produce<br>
software that can be installed on any server, so it will not be tied just to our setup.</p>


<a><h2>Milestones:</h2></a>
<p>
<b> By Spring Break (March 13):</b>
<ul>
<li>Set up testbed server with Apache, Python, MySQL and SSH</li>
<li>Have "Hello World" tutorial for Pyjamas + Django running</li>
<li>Have sample tests with pyUnit and Selenium running</li>
<li>Have pyLint customized for code checking</li>
<li>All team members completed Python, Django and Pyjamas tutorials</li>
<li>Completion of design document.</li>
</ul>
</p>
<p>
<b> By March 20 (End of Spring Break): </b>
<ul>
<li>Interface for user registration, class creation and confirming professors & TAs</li>
<li>Interface for one user to log in, create a project and view existing projects</li>
</ul>
</p>
<p>
<b> By March 27: </b>
<ul>
<li>Container base class core functionality: pop-out, flash/ping, AJAX updates</li>
<li>TextContainer core functionality: user-to-user highlighting</li>
<li>File navigation panel functional.  Allows: creating, deleting, uploading and downloading files. </li>
<li>(Revision browser functional, allows seeing summaries of past changes to files, reverting files to previous revisions, and comparing revisions.) - Wish-list</li>
</ul>
</p>
<p>
<b> By April 3: </b>
<ul>
<li>Single user editor fully functional with smart syntax highlighting, opening and changing files, user-level save, project-level synch</li>
<li>Console functionality: compile and run, integration with server.</li>
<li>Text Chat single-sided: enter messages, confirm receiving messages on server.</li>
</ul>
</p>
<p>
<b> By April 10 (prototype demo): </b>
<ul>
<li>Full suite of single-user tests, stable behavior, no P1 bugs outstanding.</li>
</ul>
</p>
<p>
<b> By April 17: </b>
<ul>
<li>All containers functioning with AJAX synchronization between two users</li>
<li>Audio communication between two users.</li>
<li>Fully functional collaborative mode (fixed editor + console)</li>
</ul>
</p>
<p>
<b> By April 24 (alpha test): </b>
<ul>
<li> Two-User Session Switching between Collaborative and Independent </li>
<li> Fully functional independent mode with 2 users (synch + eavesdrop)</li>
</ul>
</p>
<p>
<b> By May 1 (beta test): </b>
<ul>
<li>Full test suite of 2-user functionality</li>
<li>Test on at least 10 users</li>
</ul>
</p>
<p>
<b>By May 6 (presentation): </b>
<ul>
<li>Prepare demo of project.</li>
<li>Presentation planned & rehearsed</li>
<li>Initial documentation & new user info ready (possibly as handouts)</li>
</ul>
</p>
<p>
<b>By May 12 (Dean's Date): </b>
<ul>
<li>Extensive documentation finished. </li>
<li>Code submitted.</li>
<li>Celebrations planned/ throw a CEGger</li>
</ul>
</p>

<a><h2>Risks and Open Issues:</h2></a>
<p><b> Experience </b>
Only one of our team member has significant experience with Django, and none of us has experience using Pyjamas. This represents a risk factor because all of us will have to learn a significant new tool/skill to be able to contribute to the project. Additionally, one of our group has very limited python experience and one has only intermediate python skills.<br>
</p>
<p><b> Pyjamas </b>
As far as we can tell, Pyjamas will allow us to create the kind of client-side interface we want in a stable environment without too much of a headache. However, none of us has used Pyjamas before, so it may turn out that this technology is not ideal or presents tricky implementation issues.<br>
</p>
<p><b> Group Size </b>
Our group only has three members, which means that each person will have to contribute a significant amount to the code and make sure to keep on top of deadlines. Compared to a group of five, we have less room for slacking off.<br>
</p>
<p><b> Synchronization </b>
We are, at this point, assuming that we will be able to synchronize to a fine enough grain to make this project viable. If there is too much of a lag in the updates in each editor/console view, then it will create a very poor user experience, and we will have to think very carefully about how to work around this. Audio synchronization may also be an issue.<br>
</p>
<p><b> Server Issues </b>
We have been having problems setting up our testbed server (including OIT threatening to disable Christina's account), but we are hopeful that we will be able to resolve this before Spring Break.<br>
</p>
<p><b> Adoption </b>
We are designing this project with a specific user group in mind (namely Princeton undergraduates) but it's not clear if it will get much use. Adoption will also have a lot to do with how good the final product is, but there is still a question of how many people would want to use this tool in their day-to-day programming.<br>
</p>

<br>
<br>
Unknown end tag for </body><br>
<br>
<br>
<br>
<br>
<br>
Unknown end tag for </html><br>
<br>
