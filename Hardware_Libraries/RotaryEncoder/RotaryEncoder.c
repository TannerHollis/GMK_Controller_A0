/*
 * RotaryEncoder.c
 *
 *	To Use:
 *		- Format update timer for 1600Hz
 *			- If different:
 *				- Must be conscience of the timing constraint due to the update function.
 *				- Must update define for update frequency.
 *			- Configure the counter period for 0.25s which triggers the update function.
 *		- Configure IRQs for each encoder pin to trigger the respective Update function.
 *			- Encoder calculations are also updated periodically on a separate timer for zero speed calculations.
 *
 *  Created on: Jan 13, 2022
 *      Author: THollis
 */

#include "RotaryEncoder.h"

/**
  * @brief  Initialize the RotaryEncoder object.
  * @param  htim timer handle
  * @param	a_port
  * @param	a_pin
  * @param	b_port
  * @param	b_pin
  *
  * @retval Returns the RotaryEncoder object
  */
RotaryEncoder_HandleTypeDef RotaryEncoder_Init(TIM_HandleTypeDef *htim, GPIO_TypeDef *a_port, uint16_t a_pin, GPIO_TypeDef *b_port, uint16_t b_pin){
	RotaryEncoder_HandleTypeDef re;
	re.update_tim = htim;
	re.a.GPIO_Port = a_port;
	re.a.GPIO_Pin = a_pin;
	re.b.GPIO_Port = b_port;
	re.b.GPIO_Pin = b_pin;

	re.last_time = htim->Instance->CNT;
	re.last_state = RotaryEncoder_GetState(&re);
	re.ppr = ROTARYENCODER_PPR;
	re.position = 0;
	re.speed_rpm = 0;
	re.speed_hz = 0;
	re.direction = NONE;

	return(re);
}

/**
  * @brief  Initialize the RotaryEncoder object.
  * @param	re RotaryEncoder handle
  *
  * @retval Returns the RotaryEncoder state
  */
RotaryEncoder_StateTypeDef RotaryEncoder_GetState(RotaryEncoder_HandleTypeDef *re){
	uint8_t a_state = HAL_GPIO_ReadPin(re->a.GPIO_Port, re->a.GPIO_Pin);
	uint8_t b_state = HAL_GPIO_ReadPin(re->b.GPIO_Port, re->b.GPIO_Pin);

	return((RotaryEncoder_StateTypeDef)(a_state << 1 | b_state));
}

/**
  * @brief  Updates the RotaryEncoder object
  * 		1. Checks the state
  * 		2. Checks the direction
  * 		3. Increments/Decrements the position
  * 		4. Calculates the speed
  *
  * @param	re RotaryEncoder handle
  */
void RotaryEncoder_Update(RotaryEncoder_HandleTypeDef *re){
	//Before wasting ticks, capture entry time
	uint16_t time = re->update_tim->Instance->CNT;

	//Get current state of encoder
	RotaryEncoder_StateTypeDef state = RotaryEncoder_GetState(re);

	//Calculate direction
	re->direction = RotaryEncoder_GetDirection(state, re->last_state);

	//Increment/Decrement position
	if(re->direction == CLOCKWISE){
		re->position += 360.0f / re->ppr;
		if(re->position > 360.0f){
			re->position -= 360.0f;
		}
	}
	if(re->direction == COUNTERCLOCKWISE){
		re->position -= 360.0f / re->ppr;
		if(re->position < 0.0f){
			re->position += 360.0f;
		}
	}

	//Calculate rotational speed
	re->speed_hz =  ROTARYENCODER_UPDATE_TIM_FREQ / (float)(time - re->last_time) / re->ppr;
	re->speed_rpm = re->speed_hz * 60.0f;

	//Store current state/time as previous state/time
	re->last_state = state;
	re->last_time = time;
}

/**
  * @brief  Check the state transition using an expected state order.
  * 		Using gray-code, counting to 3. The expected order is as follows:
  * 		1. 0, 0
  * 		2. 0, 1
  * 		3. 1, 1
  * 		4. 1, 0
  *
  * @param	state
  * @param	last_state
  *
  * @retval	Returns the direction
  */
RotaryEncoder_DirectionTypeDef RotaryEncoder_GetDirection(RotaryEncoder_StateTypeDef state, RotaryEncoder_StateTypeDef last_state){
	RotaryEncoder_DirectionTypeDef direction = NONE;
	switch(state){
		case STATE_00:
			if(last_state == STATE_01){
				direction = CLOCKWISE;
			}
			if(last_state == STATE_10){
				direction = COUNTERCLOCKWISE;
			}
			if(last_state == STATE_00){
				direction = NONE;
			}
			break;
		case STATE_01:
			if(last_state == STATE_11){
				direction = CLOCKWISE;
			}
			if(last_state == STATE_00){
				direction = COUNTERCLOCKWISE;
			}
			if(last_state == STATE_01){
				direction = NONE;
			}
			break;
		case STATE_11:
			if(last_state == STATE_10){
				direction = CLOCKWISE;
			}
			if(last_state == STATE_01){
				direction = COUNTERCLOCKWISE;
			}
			if(last_state == STATE_11){
				direction = NONE;
			}
			break;
		case STATE_10:
			if(last_state == STATE_00){
				direction = CLOCKWISE;
			}
			if(last_state == STATE_11){
				direction = COUNTERCLOCKWISE;
			}
			if(last_state == STATE_10){
				direction = NONE;
			}
			break;
		default:
			break;
	}
	return(direction);
}
