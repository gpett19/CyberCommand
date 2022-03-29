//This is going to be a C implementation of reverseShell.py.
// Having the lower-level capabilites of C might be useful in the future, and 
// ideally it will help with some of the issues we're having with running commands.

//A lot of this code is taken from the example here:
// https://www.geeksforgeeks.org/socket-programming-cc/

#include <sys/socket.h>
#include <stdio.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#define PORT 8000 //Server host port
#define ADDRESS "192.168.1.101" //Kali address

//Create the socket.
int main(int argc, char *argv[])
{
	int sock = 0, valread;
	struct sockaddr_in serv_addr;
	char *hello = "Hello from client";
	char buffer[1024] = {0};
	if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		printf("\n Socket creation error \n");
		return -1;
	}
	
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);
	
	//Convert Address to binary form. Kali address provided here
	if(inet_pton(AF_INET, ADDRESS, &serv_addr.sin_addr)<=0)
	{
		printf("\nInvalid address/ Address not supported \n");
		return -1;
	}
	
	if(connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
	{
		printf("\n Connection Failed \n");
		return -1;
	}
	
	//Communicate with the server...
	send(sock, hello, strlen(hello), 0);
	//This doesn't print until after the value is read... wtf?
	printf("Hello message sent\n");
	valread = read(sock, buffer, 1024);
	printf("%s\n", buffer);
	return 0;
}
