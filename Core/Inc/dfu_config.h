#ifndef __DFU_CONFIG_H
#define __DFU_CONFIG_H

#include "stdint.h"

#define FLASH_VALID_SYMBOL 0xCA11AB1E

#define FLASH_APP_SIZE (96 * 1024)
#define FLASH_APP_ADDRESS 0x08008000
#define FLASH_APP_ADDRESS_END (FLASH_APP_ADDRESS + FLASH_APP_SIZE - 4)
#define FLASH_VALID_SYMBOL 0xCA11AB1E

typedef struct  __attribute__((__packed__)) DFU_Settings_TypeDef
{
	uint8_t dfuModeEnabledFromUser;
	uint8_t dfuModeArgument;
	uint16_t dfuTimeout_ms;
} DFU_Settings_TypeDef;

uint32_t shared_memory __attribute__((section(".dfuSharedSection")));

#endif
