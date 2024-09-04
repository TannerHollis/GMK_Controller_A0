#ifndef __DFU_H
#define __DFU_H

#include "dfu_config.h"

typedef struct  __attribute__((__packed__)) DFU_Settings_TypeDef
{
	uint8_t dfuModeEnabledFromUser;
	uint8_t dfuModeArgument;
	uint16_t dfuTimeout_ms;
} DFU_Settings_TypeDef;

void Bootloader_JumpToApp(uint32_t address);
uint8_t Bootloader_CheckSymbol(uint32_t address, uint32_t symbol);
uint32_t GetSector(uint32_t Address);

#endif
