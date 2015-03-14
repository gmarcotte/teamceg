# Descriptive Name of Feature #

## Abstract ##
''A sentence or two that explains the core functionality of the design.''

## Features ##
''This should be a list and description of the sub-tasks that need to be done.
Each should be categorized and modularized as much as possible.''

## Pros ##
''Why should we have this design?  Who/what will benefit from its implementation?
How is this design better than other possible designs?''

## Cons ##
''What is bad about this design?  What are the usage cases that might break or invalidate it?  What could we do better, and why aren't we doing it?''

## Implementation Plan ##
### Server-Side Functionality ###
''Details on code that will run on our server''

### Client-Side Functionality ###
''Details on code that will run on the client's machine (either as app or in browser)''

### Filesystem Structure ###
''What data will we be storing long term on either the server or client filesystem, and how will it be structured?''

### Database Structure ###
''What data will we be storing long term in databases, and how will it be structured?''

## Testing, Logging and Measurability ##
''What systems will you use to make sure that the implementation works
as desired, to keep track of errors, to store data about usage, and
to perform useful metrics on that data?''

## Reliability and Fault-Tolerance ##
''What contract will we make with our users about reliability (uptime, data backup, etc.) and how will we uphold it.  How will we recover from catastrophic errors?''

## Other considerations ##
''Anything else we should think about in evaluating the design.  Possibilities are:''
  * ''Business aspects (will it make us money?  Does it cost us anything?)''
  * ''Distribution: Do we want to open source it? Are there particular places we should try to get it adopted?''
  * ''Documentation: what sorts of docs will be useful, both from a user and programmer standpoint?''