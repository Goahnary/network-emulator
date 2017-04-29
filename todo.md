## Goal: create a simulator composed of network routers

## Requirements of the program we need to meet:

* Allow routrers to run on different machines in ANY configuration.
  * Locate routers anywhere on the network (By IP Address & Port)
* Update/keep track of forwarding table
  * Create forwarding tables for new nodes based on the current graph
* Ability to add router to network and initialize connections to other routers
  * Make an option to display the network topology when prompted to add/drop/etc...
* ~~Accomodate up to 10 network routers~~
* Have a program for visualization that updates in (near) real time
  * only has to show a snapshot of the network when there is a change
* Dynamically generated weights instead of user input
* Show link weights on visualization snapshot
* Implement a thread handling user input to allow visualization to run throughout the program
* Send data from one node to another
  * Propogate one packet and trace its route to show that it follows the current forwarding table
* Make routers work independently (run and listen for input) on every device (Jared)
