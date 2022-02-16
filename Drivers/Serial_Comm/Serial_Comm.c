/*
 * Serial_Comm.c
 *
 *  Created on: Feb 5, 2022
 *      Author: TannerGaming
 */

#include "main.h"
#include "Serial_Comm.h"
#include "Controller_Config.h"
#include "string.h"

uint8_t buffer_in[CONTROLLER_CONFIG_LENGTH + 1];
uint8_t buffer_out[CONTROLLER_CONFIG_LENGTH + 1];

void Serial_Comm_CheckMessages(){
	int16_t retval;

	//Read from buffer
	retval = _read(0, (uint8_t *)buffer_in, sizeof(buffer_in));

	//Parse, if valid message length
	if(retval > 0){
		Serial_Comm_ParseMessages();
	}

	//Send outgoing messages
}

/*
 * 	This function parses incoming messages:
 * 		- Instructions (First Byte)
 * 			1. 0x0X = Read GMK Controller ID (Revision)
 * 			2. 0x1X = Read Config Profile X
 * 			3. 0x2X = Write Config Profile X
 * 			4. 0x3X = Read All Configs
 */
void Serial_Comm_ParseMessages(){
	if((buffer_in[0] & 0x00) == 0x00){
		_write(0, (uint8_t *)gmk_controller_id, strlen(gmk_controller_id));
	}
	else if((buffer_in[0] & 0x10) == 0x10){

	}
}
