/*
 * RotaryEncoder.h
 *
 *  Created on: Jan 13, 2022
 *      Author: THollis
 */

#ifndef ROTARYENCODER_ROTARY_ENCODER_H_
#define ROTARYENCODER_ROTARY_ENCODER_H_

#define ROTARYENCODER_LINEAR_SCALE 0.05f

#define ROTARYENCODER_STEPS_COUNT_BUFFER_MULTIPLIER 100

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

	struct{
		uint16_t last;
		uint16_t current;
	} time;

	struct{
		RotaryEncoder_StateTypeDef last;
		RotaryEncoder_StateTypeDef current;
		RotaryEncoder_StateTypeDef initial;
	} state;

	struct{
		float position;
		float increment;
	} rotation;

	struct{
		float position;
		float increment;
	} linear;

	struct{
		int16_t count;
		int16_t count_buffer;
		uint8_t complete;
	} steps;

	float ppr;		// Pulses per revolution
	float dpr; 		// Detents per revolution
	uint8_t dpp; 	// Detents per pulse
	float speed_rpm;
	float speed_hz;
	float timer_freq;
	uint8_t invert;
	RotaryEncoder_DirectionTypeDef direction;
	int8_t direction_counts;
} RotaryEncoder_HandleTypeDef;

RotaryEncoder_HandleTypeDef RotaryEncoder_Init(TIM_HandleTypeDef *htim, GPIO_TypeDef *a_port, uint16_t a_pin, GPIO_TypeDef *b_port, uint16_t b_pin, float pulses_per_revolution, float detents_per_pulse, float timer_freq, uint8_t invert);
RotaryEncoder_StateTypeDef RotaryEncoder_GetState(RotaryEncoder_HandleTypeDef *re);
void RotaryEncoder_Update(RotaryEncoder_HandleTypeDef *re);
RotaryEncoder_DirectionTypeDef RotaryEncoder_GetDirection(RotaryEncoder_StateTypeDef state, RotaryEncoder_StateTypeDef last_state);
RotaryEncoder_StateTypeDef RotaryEncoder_GetPreviousState(RotaryEncoder_StateTypeDef state, RotaryEncoder_DirectionTypeDef direction);
float RotaryEncoder_CalculateRotationalPosition(RotaryEncoder_HandleTypeDef *re);
float RotaryEncoder_CalculateLinearPosition(RotaryEncoder_HandleTypeDef *re);

#endif /* ROTARYENCODER_ROTARY_ENCODER_H_ */
