/*
 * keyboard_if.c
 *
 *  Created on: Jul 29, 2021
 *      Author: THollis
 */

#include <usbd_dfu.h>
#include <stm32f4xx_hal_flash.h>
#include <stm32f4xx_hal_flash_ex.h>
#include <dfu.h>


/**
 * @brief Erase entire application firmware
 * @param addr: start address of application
 * @return Result of the flash erase operation
 */
static USBD_DFU_StatusType FlashIf_Erase(uint8_t *addr)
{
    FLASH_EraseInitTypeDef eraseInitStruct;
    uint32_t sectorError = 0;

    HAL_FLASH_Unlock();

    uint32_t address = (uint32_t)addr;
    uint32_t sector = GetSector(address);

    eraseInitStruct.TypeErase = FLASH_TYPEERASE_SECTORS;
    eraseInitStruct.Sector = sector;
    eraseInitStruct.NbSectors = 1;
    eraseInitStruct.VoltageRange = FLASH_VOLTAGE_RANGE_3;

    if (HAL_FLASHEx_Erase(&eraseInitStruct, &sectorError) != HAL_OK)
    {
        HAL_FLASH_Lock();
        return DFU_ERROR_ERASE;
    }

    HAL_FLASH_Lock();
    return DFU_ERROR_NONE;
}

/**
 * @brief Get approximating timeout for the upcoming flash operation(s).
 * @param addr: start address of the following operation(s)
 * @param len: (byte) length of the operation(s)
 * @return Expected time of next operation(s)
 */
static uint16_t FlashIf_GetTimeout_ms(uint8_t *addr, uint32_t len)
{
    return len * 1;
}

/**
 * @brief Writes the passed data to the specified flash address.
 * @param addr: target address to write to
 * @param data: flash contents to write
 * @param len: amount of bytes to write
 * @return Result of the flash program operation
 */
static USBD_DFU_StatusType FlashIf_Write(uint8_t *addr, uint8_t *data, uint32_t len)
{
    HAL_FLASH_Unlock();

    for (uint32_t i = 0; i < len; i++)
    {
        if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_BYTE, (uint32_t)(addr + i), data[i]) != HAL_OK)
        {
            HAL_FLASH_Lock();
            return DFU_ERROR_WRITE;
        }
    }

    HAL_FLASH_Lock();
    return DFU_ERROR_NONE;
}

/**
 * @brief Reads from the flash memory.
 * @param addr: source pointer
 * @param data: destination pointer
 * @param len: amount of bytes to read
 */
static void FlashIf_Read(uint8_t *addr, uint8_t *data, uint32_t len)
{
    while (len-- > 0)
        *data++ = *addr++;
}

/**
 * @brief Writes a validity signature to the end of the flash to indicate upgrade success.
 * @return Result of the flash program operation
 */
static USBD_DFU_StatusType FlashIf_Manifest(void)
{
    USBD_DFU_StatusType retval = DFU_ERROR_NONE;
    return retval;
}

static const USBD_DFU_AppType dfu_app =
{
		.Name = "GMK Controller Firmware Updater",
		.Firmware.Address = 0x08008000,
		.Firmware.TotalSize = (96 * 1024),
		.Init = HAL_FLASH_Unlock,
		.Deinit = HAL_FLASH_Lock,
		.Write = FlashIf_Write,
		.Read = FlashIf_Read,
		.Manifest = FlashIf_Manifest,
		.Erase = FlashIf_Erase,
		.GetTimeout_ms = FlashIf_GetTimeout_ms
};

USBD_DFU_IfHandleType _dfu_if = {
		.App = &dfu_app,
}, *const dfu_if = &_dfu_if;

