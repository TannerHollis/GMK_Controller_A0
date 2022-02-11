/*
 * ButtonSwitch.h
 *
 *  Created on: Jan 14, 2022
 *      Author: THollis
 */

#ifndef BUTTONSWITCH_BUTTONSWITCH_H_
#define BUTTONSWITCH_BUTTONSWITCH_H_

#include "main.h"

//Define standard timer freq and times (ms)
#define BTTNSWITCH_UPDATE_FREQ 1000.0f
#define BTTNSWITCH_DEBOUNCE 20.0f
#define BTTNSWITCH_LONG_PRESS 50000.0f

typedef struct {
	TIM_HandleTypeDef *update_tim;
	GPIO_TypeDef *GPIO_Port;
	uint16_t GPIO_Pin;
	uint16_t last_time;
	GPIO_PinState last_state;
	GPIO_PinState normal_state;
	uint8_t is_long_press;
	uint8_t is_short_press;
	uint8_t is_held;
	float update_freq;
	struct {
		float ms;
		uint16_t cnts;
	} long_press;
	struct {
		float ms;
		uint16_t cnts;
	} debounce;
} ButtonSwitch_HandleTypeDef;

ButtonSwitch_HandleTypeDef ButtonSwitch_Init(TIM_HandleTypeDef *htim, GPIO_TypeDef *gpio_port, uint16_t gpio_pin, GPIO_PinState normal_state);
void ButtonSwitch_SetDebounce(ButtonSwitch_HandleTypeDef *bs, float debounce_ms);
void ButtonSwitch_SetLongPress(ButtonSwitch_HandleTypeDef *bs, float long_press_ms);
void ButtonSwitch_SetUpdateFreq(ButtonSwitch_HandleTypeDef *bs, float update_freq);
GPIO_PinState ButtonSwitch_GetPinState(ButtonSwitch_HandleTypeDef *bs);
void ButtonSwitch_Update(ButtonSwitch_HandleTypeDef *bs);
uint8_t ButtonSwitch_GetLongPress(ButtonSwitch_HandleTypeDef *bs);
uint8_t ButtonSwitch_GetShortPress(ButtonSwitch_HandleTypeDef *bs);

#endif /* BUTTONSWITCH_BUTTONSWITCH_H_ */
