#ifndef __DF_CONFIG_H
#define __DF_CONFIG_H

#include "stdint.h"

#define FLASH_VALID_SYMBOL 0xCA11AB1E

#define FLASH_APP_SIZE 1024 * 96
#define FLASH_APP_ADDRESS_START 0x08008000
#define FLASH_APP_ADDRESS_END (FLASH_APP_ADDRESS_START + FLASH_APP_SIZE - 4)





#endif
