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

extern const uint8_t controller_configs[CONTROLLER_CONFIG_PROFILES][CONTROLLER_CONFIG_LENGTH];

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
 * 			2. 0x4X = Read Config Profile X
 * 			3. 0x8X = Write Config Profile X
 * 			4. 0xCX = Read All Configs
 */
void Serial_Comm_ParseMessages(){
	uint8_t profile = buffer_in[0] & 0x3F;
	uint8_t instr = (buffer_in[0] & ~(0x3F)) >> 6;
	if(instr == 0){
		_write(0, (uint8_t *)gmk_controller_id, strlen(gmk_controller_id));
	}
	else if(instr == 1){
		_write(0, &(controller_configs[profile][0]), CONTROLLER_CONFIG_LENGTH);
	}
	else if(instr == 2){
		memcpy(&(controller_configs[profile][0]), &buffer_in[1], CONTROLLER_CONFIG_LENGTH);
	}
	else if(instr == 3){
		//memcpy((uint8_t *)(controller_configs[profile][0]), (uint8_t *)(buffer_in[1]), CONTROLLER_CONFIG_LENGTH);
	}
}
