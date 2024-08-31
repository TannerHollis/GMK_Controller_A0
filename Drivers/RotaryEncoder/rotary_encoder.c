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
 *		- Update function was measured to complete in  ~4.19 uSeconds @ 72MHz.
 *
 *  Created on: Jan 13, 2022
 *      Author: THollis
 */

#include "main.h"
#include <rotary_encoder.h>


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
RotaryEncoder_HandleTypeDef RotaryEncoder_Init(TIM_HandleTypeDef *htim, GPIO_TypeDef *a_port, uint16_t a_pin, GPIO_TypeDef *b_port, uint16_t b_pin, float pulses_per_revolution, float timer_freq, uint8_t invert)
{
	RotaryEncoder_HandleTypeDef re;
	re.update_tim = htim;
	re.a.GPIO_Port = a_port;
	re.a.GPIO_Pin = a_pin;
	re.b.GPIO_Port = b_port;
	re.b.GPIO_Pin = b_pin;

	re.time.last = htim->Instance->CNT;
	re.state.last = RotaryEncoder_GetState(&re);
	re.state.initial = re.state.last;
	re.steps.count = 0;
	re.steps.count_buffer = 0;
	re.ppr = pulses_per_revolution;
	re.rotation.position = 0;
	re.rotation.increment = 360.0f / re.ppr / 4;
	re.linear.position = 0;
	re.linear.increment = 1.0f / re.ppr / 4;
	re.speed_rpm = 0;
	re.speed_hz = 0;
	re.direction = NONE;
	re.direction_counts = 0;

	re.timer_freq = timer_freq;

	return(re);
}

/**
  * @brief  Initialize the RotaryEncoder object.
  * @param	re RotaryEncoder handle
  *
  * @retval Returns the RotaryEncoder state
  */
RotaryEncoder_StateTypeDef RotaryEncoder_GetState(RotaryEncoder_HandleTypeDef *re){
	uint8_t a_state = !HAL_GPIO_ReadPin(re->a.GPIO_Port, re->a.GPIO_Pin);
	uint8_t b_state = !HAL_GPIO_ReadPin(re->b.GPIO_Port, re->b.GPIO_Pin);

	if(!re->invert)
		return((RotaryEncoder_StateTypeDef)(b_state << 1 | a_state));
	else
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
	re->state.last = re->state.current;
	re->state.current = RotaryEncoder_GetState(re);

	//Calculate direction
	RotaryEncoder_DirectionTypeDef direction = RotaryEncoder_GetDirection(re->state.current, re->state.last);
	re->direction_counts = (direction == re->direction) ? re->direction_counts + 1 : 0;
	re->direction = direction;

	//Update rotational/linear positions
	RotaryEncoder_CalculateRotationalPosition(re);
	RotaryEncoder_CalculateLinearPosition(re);

	//Calculate updated
	re->steps.complete = (re->state.current == re->state.initial) && (re->direction_counts >= 3);

	if(re->steps.complete){
		re->steps.count += re->direction == CLOCKWISE ? 1 : -1;
		re->steps.count_buffer = re->direction == CLOCKWISE ?
				ROTARYENCODER_STEPS_COUNT_BUFFER_MULTIPLIER :
				-ROTARYENCODER_STEPS_COUNT_BUFFER_MULTIPLIER;
		re->direction_counts = 0;
	}

	//Store current state/time as previous state/time
	re->time.last = re->time.current;
	re->time.current = time;
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
	switch(last_state){
		case STATE_00:
			if(state == STATE_01){
				direction = COUNTERCLOCKWISE;
			}
			if(state == STATE_10){
				direction = CLOCKWISE;
			}
			break;
		case STATE_01:
			if(state == STATE_11){
				direction = COUNTERCLOCKWISE;
			}
			if(state == STATE_00){
				direction = CLOCKWISE;
			}
			break;
		case STATE_11:
			if(state == STATE_10){
				direction = COUNTERCLOCKWISE;
			}
			if(state == STATE_01){
				direction = CLOCKWISE;
			}
			break;
		case STATE_10:
			if(state == STATE_00){
				direction = COUNTERCLOCKWISE;
			}
			if(state == STATE_11){
				direction = CLOCKWISE;
			}
			break;
		default:
			break;
	}
	return(direction);
}

/**
  * @brief  Calculate rotational speed in hz
  *
  * @param	re RotaryEncoder handle
  *
  * @retval	Returns the rotational speed in hz
  */
float RotaryEncoder_CalculateSpeedHz(RotaryEncoder_HandleTypeDef *re){
	re->speed_hz =  re->timer_freq / (float)(re->time.current - re->time.last) / re->ppr;
	return re->speed_hz;
}

/**
  * @brief  Calculate rotational speed in rpm
  *
  * @param	re RotaryEncoder handle
  *
  * @retval	Returns the rotational speed in rpm
  */
float RotaryEncoder_CalculateSpeedRPM(RotaryEncoder_HandleTypeDef *re){
	re->speed_rpm = RotaryEncoder_CalculateSpeedHz(re) * 60.0f;
	return re->speed_rpm;
}

/**
  * @brief  Calculate rotational position
  *
  * @param	re RotaryEncoder handle
  *
  * @retval	Returns the rotational position
  */
float RotaryEncoder_CalculateRotationalPosition(RotaryEncoder_HandleTypeDef *re){
	//Increment/Decrement position
	if(re->direction == CLOCKWISE){
		//Calculate the rotational position
		re->rotation.position += (re->rotation.position + re->rotation.increment < 360.0f) ? re->rotation.increment : -360.0f + re->rotation.increment;
	}
	else if(re->direction == COUNTERCLOCKWISE){
		//Calculate the rotational position
		re->rotation.position -= (re->rotation.position - re->rotation.increment > 0.0f) ? re->rotation.increment : -360.0f + re->rotation.increment;
	}
	return re->rotation.position;
}

/**
  * @brief  Calculate linear position
  *
  * @param	re RotaryEncoder handle
  *
  * @retval	Returns the linear position
  */
float RotaryEncoder_CalculateLinearPosition(RotaryEncoder_HandleTypeDef *re){
	//Increment/Decrement position
	if(re->direction == CLOCKWISE){
		//Calculate the linear position
		re->linear.position += ((re->linear.position + re->linear.increment) > 1.0f) ? 0 : re->linear.increment;
	}
	else if(re->direction == COUNTERCLOCKWISE){
		//Calculate the linear position
		re->linear.position -= ((re->linear.position - re->linear.increment) < 0.0f) ? 0 : re->linear.increment;
	}
	return re->linear.position;
}
