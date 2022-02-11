/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

typedef enum {
	EVENT_WAIT,
	TIM_EVENT_1,
	TIM_EVENT_2,
	TIM_EVENT_3,
	TIM_EVENT_4,
	ADC_EVENT_UPDATE,
	GPIO_EVENT_ENCODER_UPDATE,
	USB_EVENT_HID_KEYBOARD_UPDATE,
	USB_EVENT_HID_GAMEPAD_UPDATE
} State_TypeDef;

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

static const char gmk_controller_id[] = "GMK Controller (Rev. A0)\n";

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

#define GET_BIT(byte, n) ( (byte & (0x01 << n)) >> n)

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

void UpdateAllButtons();
void write_next_event_state(State_TypeDef next_state);
void write_next_keyboard_event_state(uint8_t *string_address, uint8_t string_length);

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define SW_B_Pin GPIO_PIN_13
#define SW_B_GPIO_Port GPIOC
#define SW_Y_Pin GPIO_PIN_14
#define SW_Y_GPIO_Port GPIOC
#define SW_RT_Pin GPIO_PIN_15
#define SW_RT_GPIO_Port GPIOC
#define JYSTK_L_X_Pin GPIO_PIN_0
#define JYSTK_L_X_GPIO_Port GPIOA
#define JYSTK_L_Y_Pin GPIO_PIN_1
#define JYSTK_L_Y_GPIO_Port GPIOA
#define JYSTK_R_X_Pin GPIO_PIN_2
#define JYSTK_R_X_GPIO_Port GPIOA
#define JYSTK_R_Y_Pin GPIO_PIN_3
#define JYSTK_R_Y_GPIO_Port GPIOA
#define SW_RTH_Pin GPIO_PIN_4
#define SW_RTH_GPIO_Port GPIOA
#define SR_CLK_Pin GPIO_PIN_5
#define SR_CLK_GPIO_Port GPIOA
#define R_CLK_Pin GPIO_PIN_6
#define R_CLK_GPIO_Port GPIOA
#define SR_DATA_Pin GPIO_PIN_7
#define SR_DATA_GPIO_Port GPIOA
#define nOE_Pin GPIO_PIN_0
#define nOE_GPIO_Port GPIOB
#define SW_BACK_Pin GPIO_PIN_1
#define SW_BACK_GPIO_Port GPIOB
#define SW_START_Pin GPIO_PIN_2
#define SW_START_GPIO_Port GPIOB
#define SW_LTH_Pin GPIO_PIN_10
#define SW_LTH_GPIO_Port GPIOB
#define SW_RB_Pin GPIO_PIN_12
#define SW_RB_GPIO_Port GPIOB
#define SW_RIGHT_Pin GPIO_PIN_13
#define SW_RIGHT_GPIO_Port GPIOB
#define SW_LEFT_Pin GPIO_PIN_8
#define SW_LEFT_GPIO_Port GPIOA
#define SW_LB_Pin GPIO_PIN_9
#define SW_LB_GPIO_Port GPIOA
#define SW_LT_Pin GPIO_PIN_10
#define SW_LT_GPIO_Port GPIOA
#define ENCODER_A_Pin GPIO_PIN_15
#define ENCODER_A_GPIO_Port GPIOA
#define ENCODER_A_EXTI_IRQn EXTI15_10_IRQn
#define ENCODER_B_Pin GPIO_PIN_3
#define ENCODER_B_GPIO_Port GPIOB
#define SW_X_Pin GPIO_PIN_4
#define SW_X_GPIO_Port GPIOB
#define SW_A_Pin GPIO_PIN_5
#define SW_A_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

#define EVENT_BUFFER_LENGTH 128
#define KEYBOARD_EVENT_BUFFER_LENGTH 128

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
