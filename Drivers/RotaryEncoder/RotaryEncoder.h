/*
 * RotaryEncoder.h
 *
 *  Created on: Jan 13, 2022
 *      Author: THollis
 */

#ifndef ROTARYENCODER_ROTARYENCODER_H_
#define ROTARYENCODER_ROTARYENCODER_H_

#include "main.h"

#define ROTARYENCODER_UPDATE_TIM_FREQ 1000.0f
#define ROTARYENCODER_PPR 24.0f

typedef enum{
	NONE,
	CLOCKWISE,
	COUNTERCLOCKWISE
} RotaryEncoder_DirectionTypeDef;

typedef enum{
	STATE_00 = 0,
	STATE_01,
	STATE_10,
	STATE_11
} RotaryEncoder_StateTypeDef;

typedef struct{
	TIM_HandleTypeDef *update_tim;
	struct {
		GPIO_TypeDef *GPIO_Port;
		uint16_t GPIO_Pin;
	} a;
	struct {
		GPIO_TypeDef *GPIO_Port;
		uint16_t GPIO_Pin;
	} b;
	uint16_t last_time;
	RotaryEncoder_StateTypeDef last_state;
	float position;
	float ppr;
	float speed_rpm;
	float speed_hz;
	RotaryEncoder_DirectionTypeDef direction;
} RotaryEncoder_HandleTypeDef;

RotaryEncoder_HandleTypeDef RotaryEncoder_Init(TIM_HandleTypeDef *htim, GPIO_TypeDef *a_port, uint16_t a_pin, GPIO_TypeDef *b_port, uint16_t b_pin);
RotaryEncoder_StateTypeDef RotaryEncoder_GetState(RotaryEncoder_HandleTypeDef *re);
void RotaryEncoder_Update(RotaryEncoder_HandleTypeDef *re);
RotaryEncoder_DirectionTypeDef RotaryEncoder_GetDirection(RotaryEncoder_StateTypeDef state, RotaryEncoder_StateTypeDef last_state);

#endif /* ROTARYENCODER_ROTARYENCODER_H_ */
