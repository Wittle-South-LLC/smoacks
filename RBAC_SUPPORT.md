RBAC Support
============

SMOACKS supports a very specific type of RBAC as part of code generation. The
basic use case is where you want to limit the ability to create data in a 
specific table / schema based on data values in another table.

Example Use Case
----------------

Your application manages calendar events. You support multiple calendars in
the application, and you want to limit creation (or deletion) of events in a
calendar to specific groups of users.

Let's look a how a sample schema might work for this:

* Calendar - One record per calendar that can have associated events
    * Examples: Birthday Calendar, Work Calendar, Family Calendar, ...
* Calendar Item - One record per item on the calendar. Examples: 
    * Joe's Birthday (Birthday Calendar)
    * Sales Meeting (Work Calendar)
    * Sally's Soccer Game (Family Calendar)

So the RBAC need is to allow/deny CRUD actions in the calendar item table
based on groups of users. This use case is supported in SMOACKS by
creating a authorization schema for the Calendar table that is keyed by
the calendar ID and a group ID, with an associated Role field.

How to configure RBAC support
-----------------------------

You need to create the authorization schema, and use the **smoacks-rbac-controlled**
keyword to link the table being controlled with the authorization table. In the
above example, you might create an CalendarAuth schema with three properties, the
calendar ID, a role field, and a group ID.

During test generation of the child table (CalendarItem), smoacks will generate
a setup method that will create a Roadmap entry and a RoadmapAuth entry using the
default role value specified in the smoacks configuration file.

Implementing RBAC checks
------------------------
The RBAC code generation is limited to creating a controlled record with a default
RBAC role. The presumption is that this default role has full ability to do CRUD
operations so that unit tests will pass. You will need to implement the actual
role checks in the generated API code, and write additional unit tests to verify
that non-privileged users are unable to access protected CRUD actions.
