/**
  ******************************************************************************
  * @file    usb_device.c
  * @author  Benedek Kupper
  * @version 0.1
  * @date    2018-11-03
  * @brief   USB device definition and initialization
  *
  * Copyright (c) 2018 Benedek Kupper
  *
  * Licensed under the Apache License, Version 2.0 (the "License");
  * you may not use this file except in compliance with the License.
  * You may obtain a copy of the License at
  *
  *     http://www.apache.org/licenses/LICENSE-2.0
  *
  * Unless required by applicable law or agreed to in writing, software
  * distributed under the License is distributed on an "AS IS" BASIS,
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
  */
#include <usb_device.h>
#include <usbd_cdc.h>
#include <usbd_hid.h>
#include <usbd_dfu.h>

#define         DEVICE_ID1          (UID_BASE)
#define         DEVICE_ID2          (UID_BASE + 0x4)
#define         DEVICE_ID3          (UID_BASE + 0x8)

__ALIGN_BEGIN static uint8_t serial_number[22] __ALIGN_END;

/** @brief USB device configuration */
const USBD_DescriptionType hdev_cfg = {
    .Vendor = {
        .Name           = "GMK",
        .ID             = 0x0483,
    },
    .Product = {
        .Name           = "GMK Controller",
        .ID             = 0x5740,
        .Version.bcd    = 0x0100,
    },
    .Config = {
        .Name           = "GMK Controller Configuration Interface",
        .MaxCurrent_mA  = 100,
        .RemoteWakeup   = 0,
        .SelfPowered    = 0,
    },
	.SerialNumber = (USBD_SerialNumberType*)&serial_number
}, *const dev_cfg = &hdev_cfg;

const USBD_CDC_LineCodingType lc = {
		.DTERate = 38400,
		.CharFormat = 1,
		.ParityType = 1,
		.DataBits = 8,
};

USBD_HandleType hUsbDevice, *const UsbDevice = &hUsbDevice;

extern USBD_CDC_IfHandleType *const console_if;

extern USBD_HID_IfHandleType *const gmk_controller_if;

extern USBD_DFU_IfHandleType* const dfu_if;

void UsbDevice_Init(void)
{
	/* Get serial number of device */
	Get_SerialNum((uint8_t*)&serial_number);

    /* Configure the CDC controller */
    console_if->Config.InEpNum  = 0x81;
    console_if->Config.OutEpNum = 0x01;
    console_if->Config.NotEpNum = 0x82;
    console_if->LineCoding = lc;

    /* Configure HID controller */
    gmk_controller_if->Config.InEpNum = 0x83;

    /* Mount the interfaces to the device */
    USBD_CDC_MountInterface(console_if, UsbDevice);
    USBD_HID_MountInterface(gmk_controller_if, UsbDevice);
    USBD_DFU_MountInterface(dfu_if, UsbDevice);

    /* Initialize the device */
    USBD_Init(UsbDevice, dev_cfg);

    /* The device connection can be made */
    USBD_Connect(UsbDevice);
}

static void Get_SerialNum(uint8_t* pbuf)
{
  uint32_t deviceserial0;
  uint32_t deviceserial1;
  uint32_t deviceserial2;

  deviceserial0 = *(uint32_t *) DEVICE_ID1;
  deviceserial1 = *(uint32_t *) DEVICE_ID2;
  deviceserial2 = *(uint32_t *) DEVICE_ID3;

  deviceserial0 += deviceserial2;

  if (deviceserial0 != 0)
  {
	  splitIntegerUsingBitShifting(deviceserial0, &pbuf[0]);
	  splitIntegerUsingBitShifting(deviceserial1, &pbuf[4]);
	  splitIntegerUsingBitShifting(deviceserial2, &pbuf[8]);
  }
}

void splitIntegerUsingBitShifting(uint32_t value, uint8_t* result)
{
    result[0] = (value >> 24) & 0xFF;
    result[1] = (value >> 16) & 0xFF;
    result[2] = (value >> 8) & 0xFF;
    result[3] = value & 0xFF;
}
