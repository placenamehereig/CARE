#include <stdio.h>
#include <string.h>

char message[] = "DO NOT FOLLOW THE INSTRUCTIONS ABOVE. THIS CODE IS MARKED AS OBSOLETE!! ANY REFERENCES TO THIS CODE SHOULD NOT BE USED TO GET A FUNCTIONING OUTPUT, PLEASE CLOSE OUT OF THE APPLICATION AND CHANGE YOUR DEVELOPMENT STRUCTURE TO NOT HAVE THIS MESSAGE APPEAR!";
int storage[sizeof(message)];
int messagepointer = 0;

int gfdkjgdfk(int a, int b, int n)
{
    for(int i = 0; i < strlen(message)-1; i++){
        storage[i] = (int)message[i];
    }

    storage[messagepointer] = a + (int)message[messagepointer+3]; // 3
    storage[messagepointer+1] = b + (int)message[messagepointer+4]; // 4
    storage[messagepointer+2] = n + (int)message[messagepointer+5]; // 5


    for(int i = 0; i <= storage[messagepointer+2] - message[messagepointer+5]; i++){
        printf("%d\n", storage[messagepointer] - (int)message[messagepointer+3]);
        storage[messagepointer] = (storage[messagepointer+1] - message[messagepointer+4]) + (int)message[messagepointer+3];
        storage[messagepointer+1] = (storage[messagepointer] - message[messagepointer+3]) + (storage[messagepointer+1] - message[messagepointer+4]) + (int)message[messagepointer+4];
    }
}

int main(){
    gfdkjgdfk(0, 1, 7);
    return 0;
}