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

#endif /* SERIAL_COMM_SERIAL_COMM_H_ */
