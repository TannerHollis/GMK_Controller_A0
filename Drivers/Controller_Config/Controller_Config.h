/*
 * Controller_Config.h
 *
 *  Created on: Feb 5, 2022
 *      Author: TannerGaming
 */

#ifndef CONTROLLER_CONFIG_CONTROLLER_CONFIG_H_
#define CONTROLLER_CONFIG_CONTROLLER_CONFIG_H_

#define CONTROLLER_CONFIG_LENGTH 2048
#define CONTROLLER_CONFIG_PROFILES 28

#define CONTROLLER_CONFIG_INPUTS 64
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
	Input_Conversion_TypeDef input_type;
	uint16_t addr_start;
	uint16_t addr_end;
} Input_Config_HandleTypeDef;

typedef struct {
	uint8_t profile;
	char *name;
	uint8_t *config_buffer;
	uint8_t led_color[2];
	Input_Config_HandleTypeDef input_configs[CONTROLLER_CONFIG_INPUTS];
} Controller_Config_HandleTypeDef;

typedef struct {
	union {
		struct {
			uint8_t a : 1;
			uint8_t b : 1;
			uint8_t x : 1;
			uint8_t y : 1;
			uint8_t lb : 1;
			uint8_t rb : 1;
			uint8_t lth : 1;
			uint8_t rth : 1;
			uint8_t up : 1;
			uint8_t down : 1;
			uint8_t left : 1;
			uint8_t right : 1;
			uint8_t start : 1;
			uint8_t back : 1;
			uint8_t _reserved : 2;
		};
		uint16_t _bits;
	} buttons;
	union {
		struct {
			struct {
				int16_t x;
				int16_t y;
			} left;
			struct {
				int16_t x;
				int16_t y;
			} right;
		};
		int16_t _bits[4];
	}joysticks;
	union {
		struct {
			uint8_t left;
			uint8_t right;
		};
		uint8_t _bits[2];
	} triggers;
} Controller_HandleTypeDef;

uint32_t Flash_Write_Data (uint32_t StartPageAddress, uint32_t *Data, uint16_t numberofwords);
void Flash_Read_Data (uint32_t StartPageAddress, uint32_t *RxBuf, uint16_t numberofwords);
void Controller_Config_GetConfig(uint8_t config_profile);
void Controller_Config_ClearControllerData(Controller_HandleTypeDef *c);
void Controller_Config_MapControllerData(Controller_HandleTypeDef *c);
void Controller_Config_MapInputConfig(Controller_HandleTypeDef *c, Input_Config_HandleTypeDef *ic);
void Controller_Config_MapInputButtonAsButton(Controller_HandleTypeDef *c, uint8_t *ic_buffer);
void Controller_Config_MapInputButtonAsJoystick(Controller_HandleTypeDef *c, uint8_t *ic_buffer);
void Controller_Config_MapInputButtonAsKeyboard(Controller_HandleTypeDef *c, uint8_t *ic_buffer, uint8_t str_length);
void Controller_Config_MapInputButtonAsTrigger(Controller_HandleTypeDef *c, uint8_t *ic_buffer);
void Controller_Config_MapInputJoystickAsButton(Controller_HandleTypeDef *c, uint8_t *ic_buffer);
void Controller_Config_MapInputJoystickAsJoystick(Controller_HandleTypeDef *c, uint8_t *ic_buffer);
void Controller_Config_MapInputJoystickAsKeyboard(Controller_HandleTypeDef *c, uint8_t *ic_buffer, uint8_t str_length);
void Controller_Config_MapInputJoystickAsTrigger(Controller_HandleTypeDef *c, uint8_t *ic_buffer);
void Controller_Config_MapInputEncoderAsButton(Controller_HandleTypeDef *c, uint8_t *ic_buffer);
void Controller_Config_MapInputEncoderAsJoystick(Controller_HandleTypeDef *c, uint8_t *ic_buffer);
void Controller_Config_MapInputEncoderAsKeyboard(Controller_HandleTypeDef *c, uint8_t *ic_buffer, uint8_t str_length);
void Controller_Config_MapInputEncoderAsTrigger(Controller_HandleTypeDef *c, uint8_t *ic_buffer);

#endif /* CONTROLLER_CONFIG_CONTROLLER_CONFIG_H_ */
