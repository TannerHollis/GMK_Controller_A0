/*
 * Joystick.h
 *
 *  Created on: Jan 17, 2022
 *      Author: THollis
 */

#ifndef JOYSTICK_JOYSTICK_H_
#define JOYSTICK_JOYSTICK_H_

#include "main.h"

#define JOYSTICK_DEADZONE 0.025f
#define JOYSTICK_ALIVEZONE 1.1f
#define JOYSTICK_FILTER_SAMPLES 5
#define JOYSTICK_FILTER_ALPHA 0.8f

typedef struct Joystick_AxisTypeDef
{
	uint16_t *adc;
	uint16_t min;
	uint16_t max;
	uint16_t offset;
	float deadzone;
	float alivezone;
	float val;
	float filteredVal;
	float* vals;
	uint8_t invert;
} Joystick_AxisTypeDef;

typedef struct{
	Joystick_AxisTypeDef x;
	Joystick_AxisTypeDef y;
	struct{
		uint16_t iters_max;
		uint16_t iters;
		uint8_t flag;
		float weight;
	} calibrate;
	uint8_t filtWrite;
	uint8_t filtRead;
	float* filterCoeffs;
} Joystick_HandleTypeDef;

Joystick_HandleTypeDef Joystick_Init(uint16_t *x_buffer, uint16_t *y_buffer, uint8_t flip_x, uint8_t flip_y);
void Joystick_Calibrate(Joystick_HandleTypeDef *js, uint16_t iters, float weight);
void Joystick_Update(Joystick_HandleTypeDef *js);

#endif /* JOYSTICK_JOYSTICK_H_ */
