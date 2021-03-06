/*
 * Serial_Comm.h
 *
 *  Created on: Feb 5, 2022
 *      Author: TannerGaming
 */

#ifndef SERIAL_COMM_SERIAL_COMM_H_
#define SERIAL_COMM_SERIAL_COMM_H_

extern int _read(int32_t file, uint8_t *ptr, int32_t len);
extern int _write(int32_t file, uint8_t *ptr, int32_t len);

void Serial_Comm_CheckMessages();
void Serial_Comm_ParseMessages();
void Flash_Erase();
void Flash_Program_Bytes(uint8_t *pdest, uint8_t *p_source, uint32_t length);

#endif /* SERIAL_COMM_SERIAL_COMM_H_ */
