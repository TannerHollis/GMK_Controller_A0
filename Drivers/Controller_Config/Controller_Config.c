/*
 * Controller_Config.c
 *
 *  Created on: Feb 5, 2022
 *      Author: TannerGaming
 */

#include "main.h"
#include "stdint.h"
#include "Controller_Config.h"
#include "Joystick.h"
#include "ButtonSwitch.h"
#include "RotaryEncoder.h"

__attribute__((__section__(".user_data"))) const uint8_t controller_configs[CONTROLLER_CONFIG_PROFILES][CONTROLLER_CONFIG_LENGTH];
uint8_t controller_config_address;
Controller_Config_HandleTypeDef controller_config;

//Import Hardware TypeDefs
extern ButtonSwitch_HandleTypeDef *buttons;
extern Joystick_HandleTypeDef *joysticks;
extern RotaryEncoder_HandleTypeDef *rotary_encoder;

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

	//Store configuration buffer address, profile number and name into config
	controller_config.config_buffer = (uint8_t *)(controller_configs[controller_config_address]);
	controller_config.profile = (uint8_t)(*controller_configs[controller_config_address]);
	controller_config.led_color[0] = (uint8_t)(*controller_configs[controller_config_address + 1]);
	controller_config.led_color[1] = (uint8_t)(*controller_configs[controller_config_address + 2]);
	controller_config.name = (char *)(controller_configs[controller_config_address + 3]);

	//Declare input configuration counter
	uint8_t input_config_index = 0;
	uint8_t config_start_found = 1;

	for(uint16_t i = CONTROLLER_CONFIG_NAME_LENGTH + 3; i < CONTROLLER_CONFIG_LENGTH; i++){
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

	// TODO: Time Function processing time
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
		case INPUT_BUTTON_AS_JOYSTICK:
			Controller_Config_MapInputButtonAsJoystick(c, &(controller_config.config_buffer[ic->addr_start]));
			break;
		case INPUT_BUTTON_AS_KEYBOARD:
			Controller_Config_MapInputButtonAsKeyboard(c, &(controller_config.config_buffer[ic->addr_start]), ic->addr_end - ic->addr_start);
			break;
		case INPUT_BUTTON_AS_TRIGGER:
			Controller_Config_MapInputButtonAsTrigger(c, &(controller_config.config_buffer[ic->addr_start]));
			break;
		case INPUT_JOYSTICK_AS_BUTTON:
			Controller_Config_MapInputJoystickAsButton(c, &(controller_config.config_buffer[ic->addr_start]));
			break;
		case INPUT_JOYSTICK_AS_JOYSTICK:
			Controller_Config_MapInputJoystickAsJoystick(c, &(controller_config.config_buffer[ic->addr_start]));
			break;
		case INPUT_JOYSTICK_AS_KEYBOARD:
			Controller_Config_MapInputJoystickAsKeyboard(c, &(controller_config.config_buffer[ic->addr_start]), ic->addr_end - ic->addr_start);
			break;
		case INPUT_JOYSTICK_AS_TRIGGER:
			Controller_Config_MapInputJoystickAsJoystick(c, &(controller_config.config_buffer[ic->addr_start]));
		case INPUT_ENCODER_AS_BUTTON:
			Controller_Config_MapInputEncoderAsButton(c, &(controller_config.config_buffer[ic->addr_start]));
			break;
		case INPUT_ENCODER_AS_JOYSTICK:
			Controller_Config_MapInputEncoderAsJoystick(c, &(controller_config.config_buffer[ic->addr_start]));
			break;
		case INPUT_ENCODER_AS_KEYBOARD:
			Controller_Config_MapInputEncoderAsKeyboard(c, &(controller_config.config_buffer[ic->addr_start]), ic->addr_end - ic->addr_start);
			break;
		case INPUT_ENCODER_AS_TRIGGER:
			Controller_Config_MapInputEncoderAsTrigger(c, &(controller_config.config_buffer[ic->addr_start]));
			break;
		default:
			break;
	}
}

/*
 * Input Configuration Buffer:
 * 		Byte 0: Input Button
 * 		Byte 1: Output Button
 */
void Controller_Config_MapInputButtonAsButton(Controller_HandleTypeDef *c, uint8_t *ic_buffer){
	c->buttons._bits |= (buttons[ic_buffer[0]].is_held << ic_buffer[1]);
}

/*
 * Input Configuration Buffer:
 * 		Byte 0: Input Button
 * 		Byte 1:
 * 			Bit 0: Output Joystick Left (0) or Output Joystick Right (1)
 * 			Bit 1: Axis X (0) or Axis Y (1)
 * 			Bit 2: Positive (0) or Negative (1)
 * 			Bits 3-7: Don't Care
 */
void Controller_Config_MapInputButtonAsJoystick(Controller_HandleTypeDef *c, uint8_t *ic_buffer){
	uint8_t js_out = GET_BIT(ic_buffer[1], 0);
	uint8_t xy = GET_BIT(ic_buffer[1], 1);
	uint8_t pn = GET_BIT(ic_buffer[1], 2);
	c->joysticks._bits[js_out*2 + xy] += (pn ? INT16_MIN : INT16_MAX) * (int16_t)buttons[ic_buffer[0]].is_held;
}

/*
 * Input Configuration Buffer:
 * 		Byte 0: Input Button
 * 		Byte 1: Byte 0 of String
 *
 * String length is calculate using the addr_end - addr_start of input configuration
 */
void Controller_Config_MapInputButtonAsKeyboard(Controller_HandleTypeDef *c, uint8_t *ic_buffer, uint8_t str_length){
	if(buttons[ic_buffer[0]].is_held){
		write_next_keyboard_event_state(&(ic_buffer[1]), str_length - 1);
	}
}

/*
 * Input Configuration Buffer:
 * 		Byte 0: Input Button
 * 		Byte 1:
 * 			Bit 0: Output Trigger L (0) or Output Trigger R (1)
 * 			Bits 1-7: Don't Care
 */
void Controller_Config_MapInputButtonAsTrigger(Controller_HandleTypeDef *c, uint8_t *ic_buffer){
	c->triggers._bits[ic_buffer[1]] += UINT8_MAX * (int16_t)buttons[ic_buffer[0]].is_held;
}

/*
 * Input Configuration Buffer:
 * 		Byte 0:
 * 			Bit 0: Input Joystick Left (0) or Input Joystick Right (1)
 * 			Bit 1: Axis X (0) or Axis Y (1)
 * 			Bit 2: Invert Axis (1)
 * 			Bit 3: Positive (0) or Negative (1)
 * 			Bits 4-7: Don't Care
 * 		Byte 1: Threshold 4th-Byte (float)
 * 		Byte 2: Threshold 3rd-Byte (float)
 * 		Byte 3: Threshold 2nd-Byte (float)
 * 		Byte 4: Threshold 1st-Byte (float)
 *		Byte 5: Output Button
 */
void Controller_Config_MapInputJoystickAsButton(Controller_HandleTypeDef *c, uint8_t *ic_buffer){
	uint8_t js_in = GET_BIT(ic_buffer[0], 0);
	uint8_t xy = GET_BIT(ic_buffer[0], 1);
	uint8_t invert = GET_BIT(ic_buffer[0], 2);
	uint8_t pn = GET_BIT(ic_buffer[0], 3);
	float *threshold = (float *)(&ic_buffer[1]);
	float val;
	if(xy){
		val = (invert) ? joysticks[js_in].y.val : -joysticks[js_in].y.val;
	}
	else{
		val = (invert) ? joysticks[js_in].x.val : -joysticks[js_in].x.val;
	}
	c->buttons._bits |= (pn ? val < *threshold : val > *threshold) << ic_buffer[5];
}

/*
 * Input Configuration Buffer:
 * 		Byte 0:
 * 			Bit 0: Input Joystick Left (0) or Input Joystick Right (1)
 * 			Bit 1: Invert X-Axis (1)
 * 			Bit 2: Invert Y-Axis (1)
 * 			Bit 3: Output Joystick Left (0) or Output Joystick Right (1)
 * 			Bits 4-7: Don't Care
 * 		Byte 1: X-Deadzone 4th-Byte (float)
 * 		Byte 2: X-Deadzone 3rd-Byte (float)
 * 		Byte 3: X-Deadzone 2nd-Byte (float)
 * 		Byte 4: X-Deadzone 1st-Byte (float)
 * 		Byte 5: Y-Deadzone 4th-Byte (float)
 * 		Byte 6: Y-Deadzone 3rd-Byte (float)
 * 		Byte 7: Y-Deadzone 2nd-Byte (float)
 * 		Byte 8: Y-Deadzone 1st-Byte (float)
 */
void Controller_Config_MapInputJoystickAsJoystick(Controller_HandleTypeDef *c, uint8_t *ic_buffer){
	uint8_t js_in = GET_BIT(ic_buffer[0], 0);
	uint8_t invert_x = GET_BIT(ic_buffer[0], 1);
	uint8_t invert_y = GET_BIT(ic_buffer[0], 2);
	uint8_t js_out = GET_BIT(ic_buffer[0], 3);
	float *deadzone_x = (float *)(&ic_buffer[1]);
	float *deadzone_y = (float *)(&ic_buffer[5]);
	float val_x = invert_x ? joysticks[js_in].x.val : -joysticks[js_in].x.val;
	float val_y = invert_y ? joysticks[js_in].y.val : -joysticks[js_in].y.val;
	c->joysticks._bits[js_out*2 + 0] += ((val_x > *deadzone_x || val_x < -*deadzone_x) ? val_x : 0) * -INT16_MIN;
	c->joysticks._bits[js_out*2 + 1] += ((val_y > *deadzone_y || val_y < -*deadzone_y) ? val_y : 0) * -INT16_MIN;
}

/*
 * Input Configuration Buffer:
 * 		Byte 0:
 * 			Bit 0: Input Joystick Left (0) or Input Joystick Right (1)
 * 			Bit 1: Axis X (0) or Axis Y (1)
 *	 	 	Bit 2: Invert Axis (1)
 *	 	 	Bit 3: Positive (0) or Negative (1)
 * 			Bits 4-7: Don't Care
 * 		Byte 1: Threshold 4th-Byte (float)
 * 		Byte 2: Threshold 3rd-Byte (float)
 * 		Byte 3: Threshold 2nd-Byte (float)
 * 		Byte 4: Threshold 1st-Byte (float)
 * 		Byte 5: Byte 0 of String
 */
void Controller_Config_MapInputJoystickAsKeyboard(Controller_HandleTypeDef *c, uint8_t *ic_buffer, uint8_t str_length){
	uint8_t js = GET_BIT(ic_buffer[0], 0);
	uint8_t xy = GET_BIT(ic_buffer[0], 1);
	uint8_t invert = GET_BIT(ic_buffer[0], 2);
	uint8_t pn = GET_BIT(ic_buffer[0], 3);
	float *threshold = (float *)(&ic_buffer[1]);
	float val;
	if(xy){
		val = (invert) ? joysticks[js].y.val : -joysticks[js].y.val;
	}
	else{
		val = (invert) ? joysticks[js].x.val : -joysticks[js].x.val;
	}
	if(pn ? val < *threshold : val > *threshold){
		write_next_keyboard_event_state(&(ic_buffer[5]), str_length - 5);
	}
}

/*
 * Input Configuration Buffer:
 * 		Byte 0:
 * 			Bit 0: Input Joystick Left (0) or Input Joystick Right (1)
 * 			Bit 1: Axis X (0) or Axis Y (1)
 *	 	 	Bit 2: Invert Axis (1)
 *	 	 	Bit 3: Positive (0) or Negative (1)
 *	 	 	Bit 4: Output Trigger L (0) or Output Trigger R (1)
 * 			Bits 5-7: Don't Care
 * 		Byte 1: Threshold 4th-Byte (float)
 * 		Byte 2: Threshold 3rd-Byte (float)
 * 		Byte 3: Threshold 2nd-Byte (float)
 * 		Byte 4: Threshold 1st-Byte (float)
 */
void Controller_Config_MapInputJoystickAsTrigger(Controller_HandleTypeDef *c, uint8_t *ic_buffer){
	uint8_t js_in = GET_BIT(ic_buffer[0], 0);
	uint8_t xy = GET_BIT(ic_buffer[0], 1);
	uint8_t invert = GET_BIT(ic_buffer[0], 2);
	uint8_t pn = GET_BIT(ic_buffer[0], 3);
	uint8_t tr_out = GET_BIT(ic_buffer[0], 4);
	float *threshold = (float *)(&ic_buffer[1]);
	float val;
	if(xy){
		val = (invert) ? joysticks[js_in].y.val : -joysticks[js_in].y.val;
	}
	else{
		val = (invert) ? joysticks[js_in].x.val : -joysticks[js_in].x.val;
	}
	if(pn ? val < *threshold : val > *threshold){
		c->triggers._bits[tr_out] += val * UINT8_MAX;
	}
}

/*
 * Input Configuration Buffer:
 * 		Byte 0:
 * 			Bit 0: Direction Based (0) or Speed Based (1)
 * 			Bit 1: Direction CW (0) or CCW (1)
 * 			Bit 2: Invert Direction (1)
 * 			Bits 3-7: Don't Care
 * 		Byte 1: Speed Threshold 4th-Byte (float)
 * 		Byte 2: Speed Threshold 3rd-Byte (float)
 * 		Byte 3: Speed Threshold 2nd-Byte (float)
 * 		Byte 4: Speed Threshold 1st-Byte (float)
 * 		Byte 5: Output Button
 */
void Controller_Config_MapInputEncoderAsButton(Controller_HandleTypeDef *c, uint8_t *ic_buffer){
	uint8_t speed_based = GET_BIT(ic_buffer[0], 0);
	uint8_t ccw = GET_BIT(ic_buffer[0], 1);
	uint8_t invert = GET_BIT(ic_buffer[0], 2);
	RotaryEncoder_DirectionTypeDef dir = (invert) ? (ccw) ? CLOCKWISE : COUNTERCLOCKWISE : (ccw) ? COUNTERCLOCKWISE : CLOCKWISE;
	float *speed_threshold = (float *)(&ic_buffer[1]);
	if(ccw && rotary_encoder->direction == dir){
		if(speed_based)
			c->buttons._bits |= (rotary_encoder->speed_rpm > *speed_threshold) << ic_buffer[5];
		else
			c->buttons._bits |= 0x01 << ic_buffer[5];
	}
}

/*
 * Input Configuration Buffer:
 * 		Byte 0:
 * 			Bit 0: Linear Based (0) or Binary Based (1)
 * 			Bit 1: Direction Based (0) or Speed Based (1)
 * 			Bit 2: Direction CW (0) or CCW (1)
 * 			Bit 3: Invert Direction (1)
 * 			Bits 4-7: Don't Care
 * 		Byte 1: Speed Threshold 4th-Byte (float)
 * 		Byte 2: Speed Threshold 3rd-Byte (float)
 * 		Byte 3: Speed Threshold 2nd-Byte (float)
 * 		Byte 4: Speed Threshold 1st-Byte (float)
 * 		Byte 5: Linear Middle 4th-Byte (float)
 * 		Byte 6: Linear Middle 3rd-Byte (float)
 * 		Byte 7: Linear Middle 2nd-Byte (float)
 * 		Byte 8: Linear Middle 1st-Byte (float)
* 		Byte 9: Linear Deadzone 4th-Byte (float)
 * 		Byte 10: Linear Deadzone 3rd-Byte (float)
 * 		Byte 11: Linear Deadzone 2nd-Byte (float)
 * 		Byte 12: Linear Deadzone 1st-Byte (float)
 * 		Byte 13:
 * 			Bit 0: Output Joystick Left (0) or Output Joystick Right (1)
 * 			Bit 1: Axis X (0) or Axis Y (1)
 * 			Bit 2: Positive (0) or Negative (1)
 * 			Bits 3-7: Don't Care
 */
void Controller_Config_MapInputEncoderAsJoystick(Controller_HandleTypeDef *c, uint8_t *ic_buffer){
	uint8_t binary_based = GET_BIT(ic_buffer[0], 0);
	uint8_t speed_based = GET_BIT(ic_buffer[0], 1);
	uint8_t ccw = GET_BIT(ic_buffer[0], 2);
	uint8_t invert = GET_BIT(ic_buffer[0], 3);
	RotaryEncoder_DirectionTypeDef dir = (invert) ? (ccw) ? CLOCKWISE : COUNTERCLOCKWISE : (ccw) ? COUNTERCLOCKWISE : CLOCKWISE;
	float *speed_threshold = (float *)(&ic_buffer[1]);
	float *linear_middle = (float *)(&ic_buffer[5]);
	float *linear_deadzone = (float *)(&ic_buffer[9]);
	uint8_t js_out = GET_BIT(ic_buffer[13], 0);
	uint8_t xy = GET_BIT(ic_buffer[13], 1);
	uint8_t pn = GET_BIT(ic_buffer[13], 2);
	if(binary_based){
		if(ccw && rotary_encoder->direction == dir){
			if(speed_based)
				c->joysticks._bits[js_out*2 + xy] += (pn ? INT16_MIN : INT16_MAX) * (int16_t)(rotary_encoder->speed_rpm > *speed_threshold);
			else
				c->joysticks._bits[js_out*2 + xy] += (pn ? INT16_MIN : INT16_MAX);
		}
	}
	else{
		float val = rotary_encoder->position_linear - *linear_middle;
		c->joysticks._bits[js_out*2 + xy] += (val > *linear_deadzone || val < -*linear_deadzone) ? ((invert) ? val * INT16_MIN : val * -INT16_MIN) : 0;
	}
}

/*
 * Input Configuration Buffer:
 * 		Byte 0:
 * 			Bit 0: Direction Based (0) or Speed Based (1)
 * 			Bit 1: Direction CW (0) or CCW (1)
 * 			Bit 2: Invert Direction (1)
 * 			Bits 3-7: Don't Care
 * 		Byte 1: Speed Threshold 4th-Byte (float)
 * 		Byte 2: Speed Threshold 3rd-Byte (float)
 * 		Byte 3: Speed Threshold 2nd-Byte (float)
 * 		Byte 4: Speed Threshold 1st-Byte (float)
 * 		Byte 5: Byte 0 of String
 */
void Controller_Config_MapInputEncoderAsKeyboard(Controller_HandleTypeDef *c, uint8_t *ic_buffer, uint8_t str_length){
	uint8_t speed_based = GET_BIT(ic_buffer[0], 0);
	uint8_t ccw = GET_BIT(ic_buffer[0], 1);
	uint8_t invert = GET_BIT(ic_buffer[0], 2);
	RotaryEncoder_DirectionTypeDef dir = (invert) ? (ccw) ? CLOCKWISE : COUNTERCLOCKWISE : (ccw) ? COUNTERCLOCKWISE : CLOCKWISE;
	float *speed_threshold = (float *)(&ic_buffer[1]);
	if(ccw && rotary_encoder->direction == dir){
		if(speed_based){
			if(rotary_encoder->speed_rpm > *speed_threshold)
				write_next_keyboard_event_state(&(ic_buffer[5]), str_length - 5);
		}
		else
			write_next_keyboard_event_state(&(ic_buffer[5]), str_length - 5);
	}
}

/*
 * Input Configuration Buffer:
 * 		Byte 0:
 * 			Bit 0: Linear Based (0) or Binary Based (1)
 * 			Bit 1: Direction Based (0) or Speed Based (1)
 * 			Bit 2: Direction CW (0) or CCW (1)
 * 			Bit 3: Invert Direction (1)
 * 			Bits 4-7: Don't Care
 * 		Byte 1: Speed Threshold 4th-Byte (float)
 * 		Byte 2: Speed Threshold 3rd-Byte (float)
 * 		Byte 3: Speed Threshold 2nd-Byte (float)
 * 		Byte 4: Speed Threshold 1st-Byte (float)
 * 		Byte 5: Linear Middle 4th-Byte (float)
 * 		Byte 6: Linear Middle 3rd-Byte (float)
 * 		Byte 7: Linear Middle 2nd-Byte (float)
 * 		Byte 8: Linear Middle 1st-Byte (float)
* 		Byte 9: Linear Deadzone 4th-Byte (float)
 * 		Byte 10: Linear Deadzone 3rd-Byte (float)
 * 		Byte 11: Linear Deadzone 2nd-Byte (float)
 * 		Byte 12: Linear Deadzone 1st-Byte (float)
 * 		Byte 13:
 * 			Bit 0: Output Trigger Left (0) or Output Trigger Right (1)
 * 			Bits 3-7: Don't Care
 */
void Controller_Config_MapInputEncoderAsTrigger(Controller_HandleTypeDef *c, uint8_t *ic_buffer){
	uint8_t binary_based = GET_BIT(ic_buffer[0], 0);
	uint8_t speed_based = GET_BIT(ic_buffer[0], 1);
	uint8_t ccw = GET_BIT(ic_buffer[0], 2);
	uint8_t invert = GET_BIT(ic_buffer[0], 3);
	RotaryEncoder_DirectionTypeDef dir = (invert) ? (ccw) ? CLOCKWISE : COUNTERCLOCKWISE : (ccw) ? COUNTERCLOCKWISE : CLOCKWISE;
	float *speed_threshold = (float *)(&ic_buffer[1]);
	float *linear_middle = (float *)(&ic_buffer[5]);
	float *linear_deadzone = (float *)(&ic_buffer[9]);
	uint8_t tr_out = GET_BIT(ic_buffer[13], 0);
	if(binary_based){
		if(ccw && rotary_encoder->direction == dir){
			if(speed_based)
				c->triggers._bits[tr_out] += UINT8_MAX * (int16_t)(rotary_encoder->speed_rpm > *speed_threshold);
			else
				c->triggers._bits[tr_out] += UINT8_MAX;
		}
	}
	else{
		float val = rotary_encoder->position_linear - *linear_middle;
		c->triggers._bits[tr_out] += (val > *linear_deadzone || val < -*linear_deadzone) ? ((invert) ? (1 - val) * UINT8_MAX : val * UINT8_MAX) : 0;
	}
}
