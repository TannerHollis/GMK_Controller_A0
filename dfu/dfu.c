#include "dfu.h"
#include "cmsis_gcc.h"
#include "stm32f4xx.h"

//DFU_Settings_TypeDef shared_memory __attribute__((section(".dfuSharedSection")));

void Bootloader_JumpToApp(uint32_t address)
{
	void (*runApplication)(void) = *((const void **)(address + 4)); // Skip the symbol (+4)

	/* Set the main stack pointer */
	__set_MSP(*((uint32_t *)address));

	SCB->VTOR = address;

	/* Jump to application */
	runApplication();
}

uint8_t Bootloader_CheckSymbol(uint32_t address, uint32_t symbol)
{
	uint32_t value = *(uint32_t*)address;
	return value == symbol;
}

uint32_t GetSector(uint32_t Address)
{
    uint32_t sector = 0;

    if (Address < 0x08004000) {
        sector = FLASH_SECTOR_0;  // Sector 0, 16 KB
    } else if (Address < 0x08008000) {
        sector = FLASH_SECTOR_1;  // Sector 1, 16 KB
    } else if (Address < 0x0800C000) {
        sector = FLASH_SECTOR_2;  // Sector 2, 16 KB
    } else if (Address < 0x08010000) {
        sector = FLASH_SECTOR_3;  // Sector 3, 16 KB
    } else if (Address < 0x08020000) {
        sector = FLASH_SECTOR_4;  // Sector 4, 64 KB
    } else if (Address < 0x08040000) {
        sector = FLASH_SECTOR_5;  // Sector 5, 128 KB
    } else if (Address < 0x08060000) {
        sector = FLASH_SECTOR_6;  // Sector 6, 128 KB
    } else if (Address < 0x08080000) {
        sector = FLASH_SECTOR_7;  // Sector 7, 128 KB
    }

    return sector;
}
