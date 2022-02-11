/*
 * Controller_Config.c
 *
 *  Created on: Feb 5, 2022
 *      Author: TannerGaming
 */

#include "main.h"
#include "Controller_Config.h"

__attribute__((__section__(".user_data"))) const uint8_t controller_configs[CONTROLLER_CONFIG_PROFILES][CONTROLLER_CONFIG_LENGTH];
uint8_t controller_config_address;
Controller_Config_HandleTypeDef controller_config;

uint32_t Flash_Write_Data (uint32_t StartSectorAddress, uint32_t *Data, uint16_t numberofwords){
	static FLASH_EraseInitTypeDef EraseInitStruct;
	uint32_t SECTORError;
	int sofar = 0;

	/* Unlock the Flash to enable the flash control register access *************/
	HAL_FLASH_Unlock();

	/* Erase the user Flash area */

	/* Get the number of sector to erase from 1st sector */

	uint32_t StartSector = GetSector(StartSectorAddress);
	uint32_t EndSectorAddress = StartSectorAddress + numberofwords*4;
	uint32_t EndSector = GetSector(EndSectorAddress);

	/* Fill EraseInit structure*/
	EraseInitStruct.TypeErase     = FLASH_TYPEERASE_SECTORS;
	EraseInitStruct.VoltageRange  = FLASH_VOLTAGE_RANGE_3;
	EraseInitStruct.Sector        = StartSector;
	EraseInitStruct.NbSectors     = (EndSector - StartSector) + 1;

	/* Note: If an erase operation in Flash memory also concerns data in the data or instruction cache,
	 you have to make sure that these data are rewritten before they are accessed during code
	 execution. If this cannot be done safely, it is recommended to flush the caches by setting the
	 DCRST and ICRST bits in the FLASH_CR register. */
	if (HAL_FLASHEx_Erase(&EraseInitStruct, &SECTORError) != HAL_OK)
	{
		return HAL_FLASH_GetError();
	}

	/* Program the user Flash area word by word
	(area defined by FLASH_USER_START_ADDR and FLASH_USER_END_ADDR) ***********/

	while (sofar < numberofwords)
	{
		if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, StartSectorAddress, Data[sofar]) == HAL_OK)
		{
			StartSectorAddress += 4;  // use StartPageAddress += 2 for half word and 8 for double word
			sofar++;
		}
		else
		{
			/* Error occurred while writing data in Flash memory*/
			return HAL_FLASH_GetError();
		}
	}

	/* Lock the Flash to disable the flash control register access (recommended
	 to protect the FLASH memory against possible unwanted operation) *********/
	HAL_FLASH_Lock();

	return 0;
}

void Flash_Read_Data (uint32_t StartSectorAddress, uint32_t *RxBuf, uint16_t numberofwords)
{
	while (1)
	{

		*RxBuf = *(__IO uint32_t *)StartSectorAddress;
		StartSectorAddress += 4;
		RxBuf++;
		if (!(numberofwords--)) break;
	}
}

void Controller_Config_GetConfig(uint8_t config_profile){
	controller_config_address = config_profile * CONTROLLER_CONFIG_LENGTH;

	//Store configuration buffer address and name into config
	controller_config.config_buffer = (uint8_t *)(controller_configs[controller_config_address]);
	controller_config.name = (char *)(controller_configs[controller_config_address + 1]);

	//Declare input configuration counter
	uint8_t input_config_index = 0;
	uint8_t config_start_found = 1;

	for(uint16_t i = CONTROLLER_CONFIG_NAME_LENGTH + 2; i < CONTROLLER_CONFIG_LENGTH; i++){
		//If the input config start detected,
		if(config_start_found){
			controller_config.input_configs[input_config_index].input_type = controller_config.config_buffer[i];
			controller_config.input_configs[input_config_index].addr_start = i + 1;
			config_start_found = 0;
		}

		//If end byte (0xFF) detected, increment the input config counter
		if(controller_config.config_buffer[i] == 0xFF){
			controller_config.input_configs[input_config_index].addr_end = i;
			input_config_index++;
			config_start_found = 1;
		}
	}

	//Fill the remaining input configurations not used
	for(uint8_t i = input_config_index; i < CONTROLLER_CONFIG_INPUTS; i++){
		controller_config.input_configs[i].input_type = INPUT_NOT_CONFIGURED;
	}
}

void Controller_Config_ClearControllerData(Controller_HandleTypeDef *c){
	//Reset all bytes inside of the Controller Data to zero before update
	uint8_t *controller = (uint8_t *)c;
	for(uint8_t i = 0; i < sizeof(c); i++){
		*controller = 0x00;
		controller++;
	}
}

void Controller_Config_MapControllerData(Controller_HandleTypeDef *c){
	//Clear Controller Data
	Controller_Config_ClearControllerData(c);

	//Iterate through input configurations to compute output
	for(uint8_t i = 0; i < CONTROLLER_CONFIG_INPUTS; i++){
		Controller_Config_MapInputConfig(c, &(controller_config.input_configs[i]));
	}
}

void Controller_Config_MapInputConfig(Controller_HandleTypeDef *c, Input_Config_HandleTypeDef *ic){
	switch(ic->input_type){
		case INPUT_BUTTON_AS_BUTTON:
			Controller_Config_MapInputButtonAsButton(c, &(controller_config.config_buffer[ic->addr_start]));
			break;
	}
}

void Controller_Config_MapInputButtonAsButton(Controller_HandleTypeDef *c, uint8_t *ic_buffer){

}
