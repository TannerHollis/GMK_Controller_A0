/*
 * Serial_Comm.c
 *
 *  Created on: Feb 5, 2022
 *      Author: TannerGaming
 */

#include "main.h"
#include "Serial_Comm.h"
#include "Controller_Config.h"

uint8_t buffer_in[CONTROLLER_CONFIG_LENGTH + 1];
uint8_t buffer_out[CONTROLLER_CONFIG_LENGTH + 1];

void Serial_Comm_CheckMessages(){
	uint8_t retval;

	//Read from buffer
	retval = _read(0, &buffer_in, sizeof(buffer_in));

	//Parse, if valid message length
	if(retval == 65){
		Serial_Comm_ParseMessages();
	}

	//Send outgoing messages
}

/*
 * 	This function parses incoming messages:
 * 		- Instructions (First Byte)
 * 			1. 0x0X = Read Profile X
 * 			2. 0x1X = Write Profile X
 */
void Serial_Comm_ParseMessages(){
	if(buffer_in[0] & 0x00 == 0x00){

	}
	else if(buffer_in[0] & 0x10 == 0x10){

	}
}
