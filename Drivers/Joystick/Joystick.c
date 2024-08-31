/*
 * Joystick.c
 *
 *	To Use:
 *		- Configure a timer on OC to trigger an ADC DMA request to a buffer.
 *			1. Initialize the Joystick by storing the adc buffer address to use.
 *			2. If auto calibration is desired, call this whenever.
 *			2. Upon ADC conversion complete, trigger the update.
 *		- Update function was measured to complete in about 3.80 uSeconds @ 72MHz.
 *
 *  Created on: Jan 17, 2022
 *      Author: THollis
 */

#include <joystick.h>

Joystick_HandleTypeDef Joystick_Init(uint16_t *x_buffer, uint16_t *y_buffer, uint8_t flip_axis_x, uint8_t flip_axis_y){
	Joystick_HandleTypeDef js;

	js.x.adc = x_buffer;
	js.x.min = UINT16_MAX;
	js.x.offset = 2048;
	js.x.max = 0;
	js.x.deadzone = JOYSTICK_DEADZONE;
	js.x.alivezone = JOYSTICK_ALIVEZONE;
	js.x.val = 0;
	js.x.flip_axis = flip_axis_x;

	js.y.adc = y_buffer;
	js.y.min = UINT16_MAX;
	js.y.offset = 2048;
	js.y.max = 0;
	js.y.deadzone = JOYSTICK_DEADZONE;
	js.y.alivezone = JOYSTICK_ALIVEZONE;
	js.y.val = 0;
	js.y.flip_axis = flip_axis_y;

	js.calibrate.iters_max = 0;
	js.calibrate.iters = 0;
	js.calibrate.flag = 0;
	js.calibrate.weight = 1.0f;

	return(js);
}

void Joystick_Calibrate(Joystick_HandleTypeDef *js, uint16_t iters, float weight){
	js->calibrate.iters_max = iters;
	js->calibrate.iters = iters;
	js->calibrate.flag = 1;
	js->calibrate.weight = weight;
}
/**
  * @brief  Updated the Joystick parameters using the adc buffer.
  *
  * @param  Joystick handle
  * @retval None
  */
void Joystick_Update(Joystick_HandleTypeDef *js){
	uint16_t x = *(js->x.adc);
	uint16_t y = *(js->y.adc);

	float x_val, x_sign;
	float y_val, y_sign;

	if(js->calibrate.flag && js->calibrate.iters > 0){
		js->x.offset = (uint16_t)((float)js->x.offset * (1 - js->calibrate.weight) + (float)x * js->calibrate.weight);
		js->y.offset = (uint16_t)((float)js->y.offset * (1 - js->calibrate.weight) + (float)y * js->calibrate.weight);
		js->calibrate.iters--;
	}
	else if(js->calibrate.flag){
		js->calibrate.flag = 0;
	}

	int16_t delta_x = x - js->x.offset;
	int16_t delta_y = y - js->y.offset;

	js->x.min = (x < js->x.min) ? x : js->x.min;
	js->x.max = (x > js->x.max) ? x : js->x.max;

	js->y.min = (y < js->y.min) ? y : js->y.min;
	js->y.max = (y > js->y.max) ? y : js->y.max;

	x_val = (delta_x > 0) ? (float)delta_x / (float)(js->x.max - js->x.offset) : -(float)delta_x / (float)(js->x.min - js->x.offset);
	y_val = (delta_y > 0) ? (float)delta_y / (float)(js->y.max - js->y.offset) : -(float)delta_y / (float)(js->y.min - js->y.offset);

	x_sign = (x_val > 0) ? x_val : -x_val;
	y_sign = (y_val > 0) ? y_val : -y_val;

	js->x.val = (x_sign > js->x.deadzone && x_sign < js->x.alivezone) ? x_val : 0;
	js->x.val = js->x.flip_axis ? -js->x.val : js->x.val; // Check for inverted
	js->y.val = (y_sign > js->y.deadzone && y_sign < js->y.alivezone) ? y_val : 0;
	js->y.val = js->y.flip_axis ? -js->y.val : js->y.val; // Check for inverted
}
