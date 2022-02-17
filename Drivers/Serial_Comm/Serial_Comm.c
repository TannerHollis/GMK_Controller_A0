/*
 * Serial_Comm.c
 *
 *  Created on: Feb 5, 2022
 *      Author: TannerGaming
 */

#include "main.h"
#include <controller_config.h>
#include <serial_comm.h>
#include "string.h"

uint8_t buffer_in[CONTROLLER_CONFIG_LENGTH + 1];
uint8_t buffer_out[CONTROLLER_CONFIG_LENGTH + 1];

extern const uint8_t controller_configs[CONTROLLER_CONFIG_PROFILES][CONTROLLER_CONFIG_LENGTH];
extern uint8_t controller_config[CONTROLLER_CONFIG_LENGTH];
extern uint8_t controller_config_profile;

void Serial_Comm_CheckMessages(){
	int16_t retval;

	//Read from buffer
	retval = _read(0, (uint8_t *)buffer_in, sizeof(buffer_in));

	//Parse, if valid message length
	if(retval > 0){
		Serial_Comm_ParseMessages();
	}
}

/*
 * 	This function parses incoming messages:
 * 		- Instructions (First Byte)
 * 			1. 	0x0X = Read GMK Controller ID (Revision)
 * 			2. 	0x1X = Read Config Profile X
 * 			3. 	0x2X = Write Config to RAM
 * 			4. 	0x3X = Erase Flash Configuration
 * 			5. 	0x4X = Save Config X to Flash
 * 			6. 	0x5X = Auto-Calibrate Joysticks
 * 			7. 	0x6X = Get Controller Data Output
 * 			8. 	0x7X =
 * 			9. 	0x8X = Select Controller Config Profile X
 * 			10. 0x9X = Enable Keyboard Output
 * 			11. 0xAX = Disable Keyboard Output
 * 			12. 0xBX = Enable Mouse Output
 * 			13. 0xCX = Disable Mouse Output
 * 			14. 0xDX = Enable Gamepad Output
 * 			15. 0xFX = Disable Gamepad Output
 */
void Serial_Comm_ParseMessages(){
	uint8_t profile = buffer_in[0] & 0x0F;
	uint8_t instr = (buffer_in[0] & ~(0x0F)) >> 4;
	switch(instr){
		case 0:
			_write(0, (uint8_t *)gmk_controller_id, strlen(gmk_controller_id));
			break;
		case 1:
			_write(0, &(controller_configs[profile][0]), CONTROLLER_CONFIG_LENGTH);
			break;
		case 2:
			memcpy(&(controller_config[0]), &buffer_in[1], CONTROLLER_CONFIG_LENGTH);
			_write(0, &(controller_config[0]), CONTROLLER_CONFIG_LENGTH);
			break;
		case 3:
			memcpy((uint8_t *)(controller_configs[profile][0]), (uint8_t *)(buffer_in[1]), CONTROLLER_CONFIG_LENGTH);
			break;
		case 4:
			Flash_Erase();
			break;
		case 5:
			Flash_Program_Bytes(&(controller_configs[profile][0]), (uint8_t *)(buffer_in[1]), CONTROLLER_CONFIG_LENGTH);
			break;
		case 6:
			write_next_event_state(CALIBRATE_JOYSTICKS_EVENT);
			break;
		case 7:
			write_next_event_state(USB_EVENT_OUTPUT_CONTROLLER_DATA);
			break;
		case 8:
			//Do nothing...
			break;
		case 9:
			controller_config_profile = profile;
			write_next_event_state(USB_EVENT_CHANGE_CONFIG);
			break;
		case 10:
			//TODO: Implement Keyboard output enable
			break;
		case 11:
			//TODO: Implement Keyboard output disable
			break;
		case 12:
			//TODO: Implement Mouse output enable
			break;
		case 13:
			//TODO: Implement Mouse output disable
			break;
		case 14:
			//TODO: Implement Gamepad output enable
			break;
		case 15:
			//TODO: Implement Gamepad output disable
			break;
		default:
			break;
	}
}

void Flash_Erase(){
	//Unlock the Flash to enable the flash control register access
	HAL_FLASH_Unlock();

	FLASH_EraseInitTypeDef EraseInitStruct;
	uint32_t SECTORError;

	/* Fill EraseInit structure*/
	EraseInitStruct.TypeErase     = FLASH_TYPEERASE_SECTORS;
	EraseInitStruct.VoltageRange  = FLASH_VOLTAGE_RANGE_3;
	EraseInitStruct.Sector        = FLASH_SECTOR_5;
	EraseInitStruct.NbSectors     = 1;

	HAL_FLASHEx_Erase(&EraseInitStruct, &SECTORError);

	//Lock the Flash to disable the flash control register access
	HAL_FLASH_Lock();
}

void Flash_Program_Bytes(uint8_t *pdest, uint8_t *p_source, uint32_t length){
	//Unlock the Flash to enable the flash control register access
	HAL_FLASH_Unlock();

	for(uint32_t i = 0; i < length; i++){
		HAL_FLASH_Program(FLASH_TYPEPROGRAM_BYTE, pdest + i, p_source[i]);
	}

	//Lock the Flash to disable the flash control register access
	HAL_FLASH_Lock();
}
