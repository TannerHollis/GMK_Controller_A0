/*
 * ButtonSwitch.c
 *
 *	To Use:
 *		- Configure an update timer for debounce/long press counting
 *			- Consider using a separate timer to trigger the update function for CPU offloading.
 *			- Update function was measured to complete in about 2.56 uSeconds.
 *
 *  Created on: Jan 14, 2022
 *      Author: THollis
 */

#include "ButtonSwitch.h"

/**
  * @brief  Initialize the ButtonSwitch object.
  * @param  htim timer handle
  * @param	gpio_port
  * @param	gpio_pin
  * @param	normal_state normal pin contact state
  *
  * @retval Returns the ButtonSwitch object
  */
ButtonSwitch_HandleTypeDef ButtonSwitch_Init(TIM_HandleTypeDef *htim, GPIO_TypeDef *gpio_port, uint16_t gpio_pin, GPIO_PinState normal_state){
	ButtonSwitch_HandleTypeDef bs;
	bs.update_tim = htim;
	bs.GPIO_Port = gpio_port;
	bs.GPIO_Pin = gpio_pin;
	bs.last_time = bs.update_tim->Instance->CNT;
	bs.last_state = ButtonSwitch_GetPinState(&bs);
	bs.normal_state = normal_state;
	bs.is_long_press = 0;
	bs.is_short_press = 0;
	bs.update_freq = BTTNSWITCH_UPDATE_FREQ;
	ButtonSwitch_SetDebounce(&bs, BTTNSWITCH_DEBOUNCE);
	ButtonSwitch_SetLongPress(&bs, BTTNSWITCH_LONG_PRESS);

	return(bs);
}

/**
  * @brief  Set the debounce time in milliseconds
  * @param  bs ButtonSwitch handle
  * @param	debounce_ms debounce time in milliseconds
  */
void ButtonSwitch_SetDebounce(ButtonSwitch_HandleTypeDef *bs, float debounce_ms){
	bs->debounce.cnts = (uint16_t)(debounce_ms * bs->update_freq / 1000.0f);
	bs->debounce.ms = debounce_ms;
}

/**
  * @brief  Set the long-press time in milliseconds
  * @param  bs ButtonSwitch handle
  * @param	long_press_ms time in milliseconds
  */
void ButtonSwitch_SetLongPress(ButtonSwitch_HandleTypeDef *bs, float long_press_ms){
	bs->long_press.cnts = (uint16_t)(long_press_ms * bs->update_freq / 1000.0f);
	bs->long_press.ms = long_press_ms;
}

/**
  * @brief  Set the frequency and update the debounce and long press times accordingly.
  * @param  bs ButtonSwitch handle
  * @param	update_freq freq in Hz
  */
void ButtonSwitch_SetUpdateFreq(ButtonSwitch_HandleTypeDef *bs, float update_freq){
	bs->update_freq = update_freq;
	ButtonSwitch_SetDebounce(bs, bs->debounce.ms);
	ButtonSwitch_SetLongPress(bs, bs->long_press.ms);
}

/**
  * @brief  Set the debounce time in milliseconds
  * @param  bs ButtonSwitch handle
  * @param	debounce_ms debounce time in milliseconds
  *
  * @retval Returns the current pin state of the ButtonSwitch
  */
GPIO_PinState ButtonSwitch_GetPinState(ButtonSwitch_HandleTypeDef *bs){
	return((HAL_GPIO_ReadPin(bs->GPIO_Port, bs->GPIO_Pin)));
}

/**
  * @brief  Updates the ButtonSwitch object and calculates all related parameters.
  * 		1. Handles the state transitions
  * 		2. Checks debounce, long press times
  *
  * @param  bs ButtonSwitch handle
  */
void ButtonSwitch_Update(ButtonSwitch_HandleTypeDef *bs){
	//Before wasting ticks, capture entry time
	uint16_t time = bs->update_tim->Instance->CNT;

	//Get current pin state
	GPIO_PinState state = ButtonSwitch_GetPinState(bs);

	//Calculate time difference
	uint16_t delta_time = time - bs->last_time;

	//Check debounce/long press
	uint8_t is_debounce = (delta_time > bs->debounce.cnts) ? 1 : 0;
	uint8_t is_long_press = (delta_time > bs->long_press.cnts) ? 1 : 0;

	//Check state, start debounce, check long press
	if(state != bs->normal_state && state != bs->last_state && is_debounce){
		bs->last_state = state;
		bs->last_time = time;
	}
	else if(state == bs->normal_state && state != bs->last_state && is_debounce){
		bs->is_short_press = !is_long_press;
		bs->last_state = state;
		bs->last_time = time;
	}
	else if(state != bs->normal_state && is_debounce && is_long_press){
		bs->is_long_press = is_long_press;
	}
}

/**
  * @brief  Returns the long press status, then clears the long press
  *
  * @param  bs ButtonSwitch handle
  *
  * @retval Returns 1 for true, 0 for false
  */
uint8_t ButtonSwitch_GetLongPress(ButtonSwitch_HandleTypeDef *bs){
	if(bs->is_long_press){
		bs->is_long_press = 0;
		return(1);
	}
	else{
		return(0);
	}
}

/**
  * @brief  Returns the short press status, then clears the short press
  *
  * @param  bs ButtonSwitch handle
  *
  * @retval Returns 1 for true, 0 for false
  */
uint8_t ButtonSwitch_GetShortPress(ButtonSwitch_HandleTypeDef *bs){
	if(bs->is_short_press){
		bs->is_short_press = 0;
		return(1);
	}
	else{
		return(0);
	}
}
