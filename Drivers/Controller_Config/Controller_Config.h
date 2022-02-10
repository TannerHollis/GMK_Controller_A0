/*
 * Controller_Config.h
 *
 *  Created on: Feb 5, 2022
 *      Author: TannerGaming
 */

#ifndef CONTROLLER_CONFIG_CONTROLLER_CONFIG_H_
#define CONTROLLER_CONFIG_CONTROLLER_CONFIG_H_

#define CONTROLLER_CONFIG_LENGTH 64
#define CONTROLLER_CONFIG_PROFILES 15

uint32_t Flash_Write_Data (uint32_t StartPageAddress, uint32_t *Data, uint16_t numberofwords);
void Flash_Read_Data (uint32_t StartPageAddress, uint32_t *RxBuf, uint16_t numberofwords);


#endif /* CONTROLLER_CONFIG_CONTROLLER_CONFIG_H_ */
