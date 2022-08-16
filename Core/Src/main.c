/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

#include "stm32f4xx_hal.h"
#include "usb_device.h"

#include "buttonswitch.h"
#include "led_controller.h"
#include "controller_config.h"
#include "rotary_encoder.h"
#include "joystick.h"
#include "serial_comm.h"

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;
DMA_HandleTypeDef hdma_adc1;

SPI_HandleTypeDef hspi1;

TIM_HandleTypeDef htim1;
TIM_HandleTypeDef htim2;
TIM_HandleTypeDef htim3;
TIM_HandleTypeDef htim4;

/* USER CODE BEGIN PV */

//Declare ADC buffer for joysticks
uint16_t adc_buffer[4];

//Create event buffer (FIFO) to store events to process
State_TypeDef event_state[EVENT_BUFFER_LENGTH];
uint8_t event_index_read = 0;
uint8_t event_index_write = 0;
uint8_t event_difference = 0;

//Keyboard Event buffer (FIFO) to store keyboard event addresses and string lengths
uint8_t *keyboard_event_string_addresses[KEYBOARD_EVENT_BUFFER_LENGTH];
uint8_t keyboard_event_string_lengths[KEYBOARD_EVENT_BUFFER_LENGTH];
uint8_t keyboard_event_index_read = 0;
uint8_t keyboard_event_index_write = 0;

//Declare Joysticks
Joystick_HandleTypeDef joysticks[2];

//Declare RotaryEncoder
RotaryEncoder_HandleTypeDef rotary_encoder;

//Declare ButtonSwitches
ButtonSwitch_HandleTypeDef buttons[14];

//Declare controller configuration profile, default to 0 on reset
uint8_t controller_config_profile = 0;

//Declare led controller
LED_Controller_HandleTypeDef led_controller;

//Declare controller configuration
Controller_Config_HandleTypeDef controller_config;

//Declare controller data
Controller_HandleTypeDef controller;
uint8_t controller_cdc_output_flag = 0;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_SPI1_Init(void);
static void MX_TIM1_Init(void);
static void MX_TIM2_Init(void);
static void MX_TIM3_Init(void);
static void MX_DMA_Init(void);
static void MX_ADC1_Init(void);
static void MX_TIM4_Init(void);
/* USER CODE BEGIN PFP */

extern void Send_HID_Data(Controller_HandleTypeDef* controller);

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_SPI1_Init();
  MX_TIM1_Init();
  MX_TIM2_Init();
  MX_TIM3_Init();
  MX_DMA_Init();
  MX_ADC1_Init();
  MX_TIM4_Init();
  /* USER CODE BEGIN 2 */

  //Initialize USB
  HAL_USBD_Setup();
  UsbDevice_Init();

  //Start Timers 2 & 4
  HAL_TIM_Base_Start(&htim2);
  HAL_TIM_Base_Start(&htim4);

  //Start PWM Timer 3 channel 3
  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_3);

  //Start OC Timer 1 channels 1 through 4
  HAL_TIM_OC_Start_IT(&htim1, TIM_CHANNEL_1);
  HAL_TIM_OC_Start_IT(&htim1, TIM_CHANNEL_2);
  HAL_TIM_OC_Start_IT(&htim1, TIM_CHANNEL_3);
  HAL_TIM_OC_Start_IT(&htim1, TIM_CHANNEL_4);

  //Initialize Joysticks
  joysticks[0] = Joystick_Init(&adc_buffer[0], &adc_buffer[1]);
  joysticks[1] = Joystick_Init(&adc_buffer[2], &adc_buffer[3]);

  //Initialize RotaryEncoder
  rotary_encoder = RotaryEncoder_Init(&htim2, ENCODER_A_GPIO_Port, ENCODER_A_Pin, ENCODER_B_GPIO_Port, ENCODER_B_Pin);

  //Initialize ButtonSwitches
  buttons[0] = ButtonSwitch_Init(&htim2, SW_A_GPIO_Port, SW_A_Pin, GPIO_PIN_RESET);
  buttons[1] = ButtonSwitch_Init(&htim2, SW_B_GPIO_Port, SW_B_Pin, GPIO_PIN_RESET);
  buttons[2] = ButtonSwitch_Init(&htim2, SW_X_GPIO_Port, SW_X_Pin, GPIO_PIN_RESET);
  buttons[3] = ButtonSwitch_Init(&htim2, SW_Y_GPIO_Port, SW_Y_Pin, GPIO_PIN_RESET);
  buttons[4] = ButtonSwitch_Init(&htim2, SW_LB_GPIO_Port, SW_LB_Pin, GPIO_PIN_RESET);
  buttons[5] = ButtonSwitch_Init(&htim2, SW_RB_GPIO_Port, SW_RB_Pin, GPIO_PIN_RESET);
  buttons[6] = ButtonSwitch_Init(&htim2, SW_LTH_GPIO_Port, SW_LTH_Pin, GPIO_PIN_RESET);
  buttons[7] = ButtonSwitch_Init(&htim2, SW_RTH_GPIO_Port, SW_RTH_Pin, GPIO_PIN_RESET);
  buttons[8] = ButtonSwitch_Init(&htim2, SW_LEFT_GPIO_Port, SW_LEFT_Pin, GPIO_PIN_RESET);
  buttons[9] = ButtonSwitch_Init(&htim2, SW_RIGHT_GPIO_Port, SW_RIGHT_Pin, GPIO_PIN_RESET);
  buttons[10] = ButtonSwitch_Init(&htim2, SW_START_GPIO_Port, SW_START_Pin, GPIO_PIN_RESET);
  buttons[11] = ButtonSwitch_Init(&htim2, SW_BACK_GPIO_Port, SW_BACK_Pin, GPIO_PIN_RESET);
  buttons[12] = ButtonSwitch_Init(&htim2, SW_LT_GPIO_Port, SW_LT_Pin, GPIO_PIN_RESET);
  buttons[13] = ButtonSwitch_Init(&htim2, SW_RT_GPIO_Port, SW_RT_Pin, GPIO_PIN_RESET);

  //Initialize Led Controller
  led_controller = LED_Controller_Init(&htim3, &hspi1, R_CLK_GPIO_Port, R_CLK_Pin, &(htim3.Instance->CCR3));

  //Initialize controller configuration with first profile
  controller_config = Controller_Config_Init(controller_config_profile, &led_controller);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */

  //Initialize the event state buffer
  for(uint8_t i = 0; i < EVENT_BUFFER_LENGTH; i++){
	  event_state[i] = EVENT_WAIT;
  }

  while (1)
  {
	LED_Controller_Update(&led_controller); //Update LED Color
	switch(event_state[event_index_read]){
		case EVENT_WAIT:
			UpdateAllButtons(); //Read Button States
			break;
		case TIM_EVENT_1:
			HAL_ADC_Start_DMA(&hadc1, (uint32_t *)adc_buffer, 4); //Trigger Joystick ADC read
			break;
		case TIM_EVENT_2:
			Controller_Config_MapControllerData(&controller_config, &controller); //Map Controller Configuration Data
			break;
		case TIM_EVENT_3:
			write_next_event_state(USB_EVENT_HID_GAMEPAD_UPDATE);
			break;
		case TIM_EVENT_4:
			if(controller_cdc_output_flag){
				_write(0, &controller, sizeof(controller)); //Write to USB
				controller_cdc_output_flag = 0;
			}
			Serial_Comm_CheckMessages(); //Read incoming messages
			break;
		case ADC_EVENT_UPDATE:
			Joystick_Update(&(joysticks[0]));
			Joystick_Update(&(joysticks[1]));
			if(joysticks[0].calibrate.flag && joysticks[0].calibrate.iters > 1){
				LED_Controller_ProgressBarUpdate(&led_controller, (1 - ((float)joysticks[0].calibrate.iters / (float)joysticks[0].calibrate.iters_max)));
			}
			else if(joysticks[0].calibrate.iters == 1)
				LED_Controller_ProgressBarDisable(&led_controller);
			break;
		case GPIO_EVENT_ENCODER_UPDATE:
			RotaryEncoder_Update(&rotary_encoder);
			break;
		case USB_EVENT_CHANGE_PROFILE:
			Controller_Config_GetConfig(&controller_config, controller_config_profile);
			break;
		case CALIBRATE_JOYSTICKS_EVENT:
			LED_Controller_ProgressBarEnable(&led_controller);
			LED_Controller_ProgressBarUpdate(&led_controller, 0.0f);
			Joystick_Calibrate(&(joysticks[0]), 1000, 0.05f);
			Joystick_Calibrate(&(joysticks[1]), 1000, 0.05f);
			break;
		case USB_EVENT_PING:
			_write(0, &controller_config_profile, sizeof(controller_config_profile));
			break;
		case USB_EVENT_OUTPUT_CONTROLLER_DATA:
			controller_cdc_output_flag = 1;
			break;
		case USB_EVENT_HID_KEYBOARD_UPDATE:
			if(keyboard_event_index_write != keyboard_event_index_read){
				// TODO: Implement a Send Keyboard Event via HID
				event_index_read = (event_index_read + 1) % KEYBOARD_EVENT_BUFFER_LENGTH;
			}
			break;
		case USB_EVENT_HID_GAMEPAD_UPDATE:
			Send_HID_Data(&controller);
			RotaryEncoder_Update(&rotary_encoder); //Update RotaryEncoder periodically to clear speed and direction
			break;
	}
	if(event_index_read != event_index_write){
		event_index_read = (event_index_read + 1) % EVENT_BUFFER_LENGTH;
	}
	else
		write_next_event_state(EVENT_WAIT);
	event_difference = (event_index_write >= event_index_read) ? event_index_write - event_index_read : event_index_write + (UINT8_MAX - event_index_read);
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 5;
  RCC_OscInitStruct.PLL.PLLN = 72;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 3;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */

  /** Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion)
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV2;
  hadc1.Init.Resolution = ADC_RESOLUTION_12B;
  hadc1.Init.ScanConvMode = ENABLE;
  hadc1.Init.ContinuousConvMode = DISABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 4;
  hadc1.Init.DMAContinuousRequests = DISABLE;
  hadc1.Init.EOCSelection = ADC_EOC_SEQ_CONV;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_0;
  sConfig.Rank = 1;
  sConfig.SamplingTime = ADC_SAMPLETIME_15CYCLES;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_1;
  sConfig.Rank = 2;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_2;
  sConfig.Rank = 3;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_3;
  sConfig.Rank = 4;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief SPI1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI1_Init(void)
{

  /* USER CODE BEGIN SPI1_Init 0 */

  /* USER CODE END SPI1_Init 0 */

  /* USER CODE BEGIN SPI1_Init 1 */

  /* USER CODE END SPI1_Init 1 */
  /* SPI1 parameter configuration*/
  hspi1.Instance = SPI1;
  hspi1.Init.Mode = SPI_MODE_MASTER;
  hspi1.Init.Direction = SPI_DIRECTION_1LINE;
  hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi1.Init.NSS = SPI_NSS_SOFT;
  hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_8;
  hspi1.Init.FirstBit = SPI_FIRSTBIT_LSB;
  hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi1.Init.CRCPolynomial = 10;
  if (HAL_SPI_Init(&hspi1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI1_Init 2 */

  /* USER CODE END SPI1_Init 2 */

}

/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};
  TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 99;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 719;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_OC_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_ACTIVE;
  sConfigOC.Pulse = 179;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
  sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
  if (HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  __HAL_TIM_ENABLE_OCxPRELOAD(&htim1, TIM_CHANNEL_1);
  sConfigOC.Pulse = 359;
  if (HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  __HAL_TIM_ENABLE_OCxPRELOAD(&htim1, TIM_CHANNEL_2);
  sConfigOC.Pulse = 539;
  if (HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_3) != HAL_OK)
  {
    Error_Handler();
  }
  __HAL_TIM_ENABLE_OCxPRELOAD(&htim1, TIM_CHANNEL_3);
  sConfigOC.Pulse = 3599;
  if (HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_4) != HAL_OK)
  {
    Error_Handler();
  }
  __HAL_TIM_ENABLE_OCxPRELOAD(&htim1, TIM_CHANNEL_4);
  sBreakDeadTimeConfig.OffStateRunMode = TIM_OSSR_DISABLE;
  sBreakDeadTimeConfig.OffStateIDLEMode = TIM_OSSI_DISABLE;
  sBreakDeadTimeConfig.LockLevel = TIM_LOCKLEVEL_OFF;
  sBreakDeadTimeConfig.DeadTime = 0;
  sBreakDeadTimeConfig.BreakState = TIM_BREAK_DISABLE;
  sBreakDeadTimeConfig.BreakPolarity = TIM_BREAKPOLARITY_HIGH;
  sBreakDeadTimeConfig.AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE;
  if (HAL_TIMEx_ConfigBreakDeadTime(&htim1, &sBreakDeadTimeConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */

}

/**
  * @brief TIM2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM2_Init(void)
{

  /* USER CODE BEGIN TIM2_Init 0 */

  /* USER CODE END TIM2_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM2_Init 1 */

  /* USER CODE END TIM2_Init 1 */
  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 35999;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 4294967295;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV2;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim2, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM2_Init 2 */

  /* USER CODE END TIM2_Init 2 */

}

/**
  * @brief TIM3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM3_Init(void)
{

  /* USER CODE BEGIN TIM3_Init 0 */

  /* USER CODE END TIM3_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM3_Init 1 */

  /* USER CODE END TIM3_Init 1 */
  htim3.Instance = TIM3;
  htim3.Init.Prescaler = 2343;
  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim3.Init.Period = 255;
  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim3, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_LOW;
  sConfigOC.OCFastMode = TIM_OCFAST_ENABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM3_Init 2 */

  /* USER CODE END TIM3_Init 2 */
  HAL_TIM_MspPostInit(&htim3);

}

/**
  * @brief TIM4 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM4_Init(void)
{

  /* USER CODE BEGIN TIM4_Init 0 */

  /* USER CODE END TIM4_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM4_Init 1 */

  /* USER CODE END TIM4_Init 1 */
  htim4.Instance = TIM4;
  htim4.Init.Prescaler = 0;
  htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim4.Init.Period = 65535;
  htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim4.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim4) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim4, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim4, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM4_Init 2 */

  /* USER CODE END TIM4_Init 2 */

}

/**
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void)
{

  /* DMA controller clock enable */
  __HAL_RCC_DMA2_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA2_Stream0_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA2_Stream0_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA2_Stream0_IRQn);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(R_CLK_GPIO_Port, R_CLK_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pins : SW_B_Pin SW_Y_Pin SW_RT_Pin */
  GPIO_InitStruct.Pin = SW_B_Pin|SW_Y_Pin|SW_RT_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : SW_RTH_Pin SW_LEFT_Pin SW_LB_Pin SW_LT_Pin */
  GPIO_InitStruct.Pin = SW_RTH_Pin|SW_LEFT_Pin|SW_LB_Pin|SW_LT_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : R_CLK_Pin */
  GPIO_InitStruct.Pin = R_CLK_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(R_CLK_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : SW_BACK_Pin SW_START_Pin SW_LTH_Pin SW_RB_Pin
                           SW_RIGHT_Pin SW_X_Pin SW_A_Pin */
  GPIO_InitStruct.Pin = SW_BACK_Pin|SW_START_Pin|SW_LTH_Pin|SW_RB_Pin
                          |SW_RIGHT_Pin|SW_X_Pin|SW_A_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pin : ENCODER_A_Pin */
  GPIO_InitStruct.Pin = ENCODER_A_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(ENCODER_A_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : ENCODER_B_Pin */
  GPIO_InitStruct.Pin = ENCODER_B_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(ENCODER_B_GPIO_Port, &GPIO_InitStruct);

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI15_10_IRQn, 1, 0);
  HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);

}

/* USER CODE BEGIN 4 */

void UpdateAllButtons(){
	for(uint8_t i = 0; i < 14; i++){
		ButtonSwitch_Update(&(buttons[i]));
	}
}

//Increment event_index_write and write to next event_state in buffer
void write_next_event_state(State_TypeDef next_state){
	event_index_write = (event_index_write + 1) % EVENT_BUFFER_LENGTH;
	event_state[event_index_write] = next_state;
}

//Increment keyboard_event_index_write and write to next event_state in buffer
void write_next_keyboard_event_state(uint8_t *string_address, uint8_t string_length){
	write_next_event_state(USB_EVENT_HID_KEYBOARD_UPDATE);
	keyboard_event_string_addresses[keyboard_event_index_write] = string_address;
	keyboard_event_string_lengths[keyboard_event_index_write] = string_length;
	event_index_write = (keyboard_event_index_write + 1) % KEYBOARD_EVENT_BUFFER_LENGTH;
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc){
	write_next_event_state(ADC_EVENT_UPDATE);
}

void HAL_TIM_OC_DelayElapsedCallback(TIM_HandleTypeDef *htim){
	switch(htim->Channel){
		case HAL_TIM_ACTIVE_CHANNEL_1:
			write_next_event_state(TIM_EVENT_1);
			break;
		case HAL_TIM_ACTIVE_CHANNEL_2:
			write_next_event_state(TIM_EVENT_2);
			break;
		case HAL_TIM_ACTIVE_CHANNEL_3:
			write_next_event_state(TIM_EVENT_3);
			break;
		case HAL_TIM_ACTIVE_CHANNEL_4:
			write_next_event_state(TIM_EVENT_4);
			break;
		default:
			break;
	}
}

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin){
	if(GPIO_Pin == ENCODER_A_Pin || GPIO_Pin == ENCODER_B_Pin){
		write_next_event_state(GPIO_EVENT_ENCODER_UPDATE);
	}
}

void HAL_SPI_TxCpltCallback(SPI_HandleTypeDef *hspi){
	LED_Controller_Latch(&led_controller, GPIO_PIN_SET); //Latch new led output
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
