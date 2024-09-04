/*
 * led_controller.c
 *
 *	To Use:
 *		- Initialize this function with the following inputs:
 *			- update_timer, configured for around 120Hz
 *				- This timer controls the psuedo PWM individual LED brightness.
 *				- The period should be set to 256.
 *				- This time also controls the PWM for nOE channel for overal dimming
 *			- spi, configured for LSB first
 *			- r_clk_port, the register clk GPIO port
 *			- r_clk_pin, the register clk pin
 *			- nOE_channel, the address of the nOE PWM CCR register, for dimming
 *		- Call LED_Controller_Update() when you want to update the led controller color.
 *			- This function should be consistenly called when idle to mimic PWM through shift register output.
 *		- Update function was measured to complete in about 22.1 uSeconds @ 72MHz.
 *
 *  Created on: Feb 15, 2022
 *      Author: TannerGaming
 */

#include "main.h"
#include "led_controller.h"

uint8_t led_data_buffer[LED_DATA_OUT_SIZE];

LED_Controller_HandleTypeDef LED_Controller_Init(TIM_HandleTypeDef *update_timer, SPI_HandleTypeDef *spi, GPIO_TypeDef *r_clk_port, uint16_t r_clk_pin, uint32_t *nOE_channel){
	LED_Controller_HandleTypeDef lc;
	lc.update_timer = update_timer;
	lc.spi = spi;
	lc.r_clk_port = r_clk_port;
	lc.r_clk_pin = r_clk_pin;

	//Initialize LED colors
	for(uint8_t i = 0; i < LEDS; i++){
		lc.leds[i].r = 0;
		lc.leds[i].g = 0;
		lc.leds[i].b = 0;
	}
	lc.debugLED = 0;
	lc.logoLED.r = 0;
	lc.logoLED.g = 0;
	lc.logoLED.b = 0;
	lc.progress_bar = 0;
	lc.progress_bar_val = 0;
	lc.nOE_channel = nOE_channel;
	lc.brightness = DEFAULT_BRIGHTNESS;
	LED_Controller_UpdateBrightness(&lc, lc.brightness);
	return(lc);
}

void LED_Controller_Latch(LED_Controller_HandleTypeDef *lc, GPIO_PinState state){
	HAL_GPIO_WritePin(lc->r_clk_port, lc->r_clk_pin, state);
}

void LED_Controller_UpdateBrightness(LED_Controller_HandleTypeDef *lc, uint16_t brightness){
	*lc->nOE_channel = brightness;
	lc->brightness = brightness;
}

void LED_Controller_Update(LED_Controller_HandleTypeDef *lc){
	uint16_t timer_cnt = lc->update_timer->Instance->CNT;
	for(uint8_t i = 0; i < LED_DATA_OUT_SIZE; i++){
		led_data_buffer[i] = 0;
	}
	LED_Color_TypeDef led_data[LEDS];
	if(lc->progress_bar){
		for(uint8_t i = 0; i < LEDS; i++){
			led_data[i].r = (lc->progress_bar_val > 0.25f*i) ? 255 : 0;
			led_data[i].g = 0;
			led_data[i].b = 0;
		}
	}
	else{
		for(uint8_t i = 0; i < LEDS; i++){
			led_data[i] = lc->leds[i];
		}
	}

	led_data_buffer[0] |= (led_data[0].r > timer_cnt) << 5;
	led_data_buffer[0] |= (led_data[0].g > timer_cnt) << 6;
	led_data_buffer[0] |= (led_data[0].b > timer_cnt) << 7;
	led_data_buffer[0] |= (led_data[1].r > timer_cnt) << 2;
	led_data_buffer[0] |= (led_data[1].g > timer_cnt) << 3;
	led_data_buffer[0] |= (led_data[1].b > timer_cnt) << 4;
	led_data_buffer[1] |= (led_data[2].r > timer_cnt) << 7;
	led_data_buffer[0] |= (led_data[2].g > timer_cnt) << 0;
	led_data_buffer[0] |= (led_data[2].b > timer_cnt) << 1;
	led_data_buffer[1] |= (led_data[3].r > timer_cnt) << 1;
	led_data_buffer[1] |= (led_data[3].g > timer_cnt) << 2;
	led_data_buffer[1] |= (led_data[3].b > timer_cnt) << 3;
	for(uint8_t i = 0; i < LED_DATA_OUT_SIZE; i++){
		led_data_buffer[i] = ~led_data_buffer[i];
	}
	LED_Controller_Latch(lc, GPIO_PIN_RESET);
	HAL_SPI_Transmit_IT(lc->spi, led_data_buffer, LED_DATA_OUT_SIZE);
}

void LED_Controller_ProgressBarEnable(LED_Controller_HandleTypeDef *lc){
	lc->progress_bar = 1;
}

void LED_Controller_ProgressBarUpdate(LED_Controller_HandleTypeDef *lc, float val){
	lc->progress_bar_val = val;
}

void LED_Controller_ProgressBarDisable(LED_Controller_HandleTypeDef *lc){
	lc->progress_bar = 0;
}
