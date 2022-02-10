/*
 * Controller_Config.h
 *
 *  Created on: Feb 5, 2022
 *      Author: TannerGaming
 */

#ifndef CONTROLLER_CONFIG_CONTROLLER_CONFIG_H_
#define CONTROLLER_CONFIG_CONTROLLER_CONFIG_H_

#define CONTROLLER_CONFIG_LENGTH 2048
#define CONTROLLER_CONFIG_PROFILES 12

#define CONTROLLER_CONFIG_INPUTS 24
#define CONTROLLER_CONFIG_NAME_LENGTH 12

typedef enum {
	INPUT_BUTTON_AS_BUTTON = 0,
	INPUT_BUTTON_AS_JOYSTICK,
	INPUT_BUTTON_AS_KEYBOARD,
	INPUT_BUTTON_AS_TRIGGER,
	INPUT_JOYSTICK_AS_BUTTON,
	INPUT_JOYSTICK_AS_JOYSTICK,
	INPUT_JOYSTICK_AS_KEYBOARD,
	INPUT_JOYSTICK_AS_TRIGGER,
	INPUT_ENCODER_AS_BUTTON,
	INPUT_ENCODER_AS_JOYSTICK,
	INPUT_ENCODER_AS_KEYBOARD,
	INPUT_ENCODER_AS_TRIGGER,
	INPUT_NOT_CONFIGURED
} Input_Conversion_TypeDef;

typedef struct {
	char *name;
	uint8_t *config_buffer;
	uint8_t led_color[2];
	Input_Config_HandleTypeDef input_configs[CONTROLLER_CONFIG_INPUTS];
} Controller_Config_HandleTypeDef;

typedef struct {
	Input_Conversion_TypeDef input_type;
	uint16_t addr_start;
	uint16_t addr_end;
} Input_Config_HandleTypeDef;

uint32_t Flash_Write_Data (uint32_t StartPageAddress, uint32_t *Data, uint16_t numberofwords);
void Flash_Read_Data (uint32_t StartPageAddress, uint32_t *RxBuf, uint16_t numberofwords);
void Controller_Config_GetConfig(uint8_t config_profile);

#endif /* CONTROLLER_CONFIG_CONTROLLER_CONFIG_H_ */
