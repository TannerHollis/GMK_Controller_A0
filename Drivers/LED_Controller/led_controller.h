/*
 * led_controller.h
 *
 *  Created on: Feb 15, 2022
 *      Author: TannerGaming
 */

#ifndef LED_CONTROLLER_LED_CONTROLLER_H_
#define LED_CONTROLLER_LED_CONTROLLER_H_

#define LEDS 4
#define LED_DATA_OUT_SIZE 2
#define DEFAULT_BRIGHTNESS 32

typedef struct {
	uint8_t r;
	uint8_t g;
	uint8_t b;
} LED_Color_TypeDef;

typedef struct {
	TIM_HandleTypeDef *update_timer;
	LED_Color_TypeDef leds[LEDS];
	SPI_HandleTypeDef *spi;
	GPIO_TypeDef *r_clk_port;
	uint16_t r_clk_pin;
	uint16_t brightness;
	uint32_t *nOE_channel;
} LED_Controller_HandleTypeDef;

LED_Controller_HandleTypeDef LED_Controller_Init(TIM_HandleTypeDef *update_timer, SPI_HandleTypeDef *spi, GPIO_TypeDef *r_clk_port, uint16_t r_clk_pin, uint32_t *nOE_channel);
void LED_Controller_Latch(LED_Controller_HandleTypeDef *lc, GPIO_PinState state);
void LED_Controller_Update_Brightness(LED_Controller_HandleTypeDef *lc, uint16_t brightness);
void LED_Controller_Update(LED_Controller_HandleTypeDef *lc);

#endif /* LED_CONTROLLER_LED_CONTROLLER_H_ */
