################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (9-2020-q2-update)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../USBDevice-master/Device/usbd.c \
../USBDevice-master/Device/usbd_ctrl.c \
../USBDevice-master/Device/usbd_desc.c \
../USBDevice-master/Device/usbd_ep.c \
../USBDevice-master/Device/usbd_if.c \
../USBDevice-master/Device/usbd_microsoft_os.c \
../USBDevice-master/Device/usbd_utils.c 

OBJS += \
./USBDevice-master/Device/usbd.o \
./USBDevice-master/Device/usbd_ctrl.o \
./USBDevice-master/Device/usbd_desc.o \
./USBDevice-master/Device/usbd_ep.o \
./USBDevice-master/Device/usbd_if.o \
./USBDevice-master/Device/usbd_microsoft_os.o \
./USBDevice-master/Device/usbd_utils.o 

C_DEPS += \
./USBDevice-master/Device/usbd.d \
./USBDevice-master/Device/usbd_ctrl.d \
./USBDevice-master/Device/usbd_desc.d \
./USBDevice-master/Device/usbd_ep.d \
./USBDevice-master/Device/usbd_if.d \
./USBDevice-master/Device/usbd_microsoft_os.d \
./USBDevice-master/Device/usbd_utils.d 


# Each subdirectory must supply rules for building sources it contributes
USBDevice-master/Device/%.o: ../USBDevice-master/Device/%.c USBDevice-master/Device/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F411xE -c -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Hardware_Libraries/ButtonSwitch" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Hardware_Libraries/Joystick" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Hardware_Libraries/RotaryEncoder" -I../Core/Inc -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Core/Controller_Config" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Core/Serial_Comm" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/XPD_USB" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Class/DFU" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Class/MSC" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Include/private" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/PDs/STM32_XPD" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Include" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Device" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Class/CDC" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Class/HID" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-USBDevice-2d-master-2f-Device

clean-USBDevice-2d-master-2f-Device:
	-$(RM) ./USBDevice-master/Device/usbd.d ./USBDevice-master/Device/usbd.o ./USBDevice-master/Device/usbd_ctrl.d ./USBDevice-master/Device/usbd_ctrl.o ./USBDevice-master/Device/usbd_desc.d ./USBDevice-master/Device/usbd_desc.o ./USBDevice-master/Device/usbd_ep.d ./USBDevice-master/Device/usbd_ep.o ./USBDevice-master/Device/usbd_if.d ./USBDevice-master/Device/usbd_if.o ./USBDevice-master/Device/usbd_microsoft_os.d ./USBDevice-master/Device/usbd_microsoft_os.o ./USBDevice-master/Device/usbd_utils.d ./USBDevice-master/Device/usbd_utils.o

.PHONY: clean-USBDevice-2d-master-2f-Device

