/*
 * keyboard_if.c
 *
 *  Created on: Jul 29, 2021
 *      Author: THollis
 */

#include <usbd_hid.h>
#include "stm32xxxx.h"
#include "Controller_Config.h"
#include <stdio.h>
#include <string.h>

#define lowByte(w) ((uint8_t) ((w) & 0xff))
#define highByte(w) ((uint8_t) ((w) >> 8))

uint8_t ReportDescriptor[65] = {
	0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
    0x09, 0x05,                    // USAGE (Game Pad)
    0xa1, 0x01,                    // COLLECTION (Application)
    0xa1, 0x00,                    //   COLLECTION (Physical)
    0x85, 0x01,                    //     REPORT_ID (1)
    0x05, 0x09,                    //     USAGE_PAGE (Button)
    0x19, 0x01,                    //     USAGE_MINIMUM (Button 1)
    0x29, 0x10,                    //     USAGE_MAXIMUM (Button 16)
    0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
    0x25, 0x01,                    //     LOGICAL_MAXIMUM (1)
    0x95, 0x10,                    //     REPORT_COUNT (16)
    0x75, 0x01,                    //     REPORT_SIZE (1)
    0x81, 0x02,                    //     INPUT (Data,Var,Abs)
    0x05, 0x01,                    //     USAGE_PAGE (Generic Desktop)
    0x09, 0x30,                    //     USAGE (X)
    0x09, 0x31,                    //     USAGE (Y)
    0x09, 0x32,                    //     USAGE (Z)
    0x09, 0x33,                    //     USAGE (Rx)
    0x16, 0x01, 0x80,              //     LOGICAL_MINIMUM (-32767)
    0x26, 0xff, 0x7f,              //     LOGICAL_MAXIMUM (32767)
    0x75, 0x10,                    //     REPORT_SIZE (16)
    0x95, 0x04,                    //     REPORT_COUNT (4)
    0x81, 0x02,                    //     INPUT (Data,Var,Abs)
    0x09, 0x34,                    //     USAGE (Ry)
    0x09, 0x35,                    //     USAGE (Rz)
    0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
    0x26, 0xff, 0x00,              //     LOGICAL_MAXIMUM (255)
    0x75, 0x08,                    //     REPORT_SIZE (8)
    0x95, 0x02,                    //     REPORT_COUNT (2)
    0x81, 0x02,                    //     INPUT (Data,Var,Abs)
    0xc0,                          //   END_COLLECTION
    0xc0                          // END_COLLECTION
};

static const USBD_HID_ReportConfigType gmk_controller_hid_report =
{
		.Desc = ReportDescriptor,
		.DescLength = 65,
		.MaxId = 1,
		.Input =
		{
			.Interval_ms = 1,
			.MaxSize = 13,
		},
		.Feature =
		{
			.MaxSize = 13,
		},
		.Output =
		{
			.Interval_ms = 200,
			.MaxSize = 1,
		},
};

static const USBD_HID_AppType gmk_controller_app =
{
		.Name = "GMK HID Controller",
		.Report = &gmk_controller_hid_report,
};

USBD_HID_IfHandleType _gmk_controller_if = {
		.App = &gmk_controller_app,
}, *const gmk_controller_if = &_gmk_controller_if;

struct {
	uint8_t report_id;
	uint8_t buttons[2];
	uint8_t joysticks[8];
	uint8_t triggers[2];
} hid_output_data;

void Send_HID_Data(Controller_HandleTypeDef* controller){
	hid_output_data.report_id = 1;
	hid_output_data.buttons[0] = lowByte(controller->buttons._bits);
	hid_output_data.buttons[1] = highByte(controller->buttons._bits);
	hid_output_data.joysticks[0] = lowByte(controller->joysticks.left.x);
	hid_output_data.joysticks[1] = highByte(controller->joysticks.left.x);
	hid_output_data.joysticks[2] = lowByte(controller->joysticks.left.y);
	hid_output_data.joysticks[3] = highByte(controller->joysticks.left.y);
	hid_output_data.joysticks[4] = lowByte(controller->joysticks.right.x);
	hid_output_data.joysticks[5] = highByte(controller->joysticks.right.x);
	hid_output_data.joysticks[6] = lowByte(controller->joysticks.right.y);
	hid_output_data.joysticks[7] = highByte(controller->joysticks.right.y);
	hid_output_data.triggers[0] = controller->triggers.left;
	hid_output_data.triggers[1] = controller->triggers.right;
	USBD_HID_ReportIn(gmk_controller_if, &hid_output_data, sizeof(hid_output_data)); //Send GMK Controller HID Data
}
