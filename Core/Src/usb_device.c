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

/** @brief USB device configuration */
const USBD_DescriptionType hdev_cfg = {
    .Vendor = {
        .Name           = "STMicroelectronics",
        .ID             = 0x0483,
    },
    .Product = {
        .Name           = "GMK Controller",
        .ID             = 0x5740,
        .Version.bcd    = 0x0100,
    },
    .Config = {
        .Name           = "GMK Controller Configuration",
        .MaxCurrent_mA  = 100,
        .RemoteWakeup   = 0,
        .SelfPowered    = 0,
    },
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

void UsbDevice_Init(void)
{
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

    /* Initialize the device */
    USBD_Init(UsbDevice, dev_cfg);

    /* The device connection can be made */
    USBD_Connect(UsbDevice);
}
