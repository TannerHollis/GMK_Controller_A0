################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/USBDevice-master/Device/usbd.c \
../Drivers/USBDevice-master/Device/usbd_ctrl.c \
../Drivers/USBDevice-master/Device/usbd_desc.c \
../Drivers/USBDevice-master/Device/usbd_ep.c \
../Drivers/USBDevice-master/Device/usbd_if.c \
../Drivers/USBDevice-master/Device/usbd_microsoft_os.c \
../Drivers/USBDevice-master/Device/usbd_utils.c 

OBJS += \
./Drivers/USBDevice-master/Device/usbd.o \
./Drivers/USBDevice-master/Device/usbd_ctrl.o \
./Drivers/USBDevice-master/Device/usbd_desc.o \
./Drivers/USBDevice-master/Device/usbd_ep.o \
./Drivers/USBDevice-master/Device/usbd_if.o \
./Drivers/USBDevice-master/Device/usbd_microsoft_os.o \
./Drivers/USBDevice-master/Device/usbd_utils.o 

C_DEPS += \
./Drivers/USBDevice-master/Device/usbd.d \
./Drivers/USBDevice-master/Device/usbd_ctrl.d \
./Drivers/USBDevice-master/Device/usbd_desc.d \
./Drivers/USBDevice-master/Device/usbd_ep.d \
./Drivers/USBDevice-master/Device/usbd_if.d \
./Drivers/USBDevice-master/Device/usbd_microsoft_os.d \
./Drivers/USBDevice-master/Device/usbd_utils.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/USBDevice-master/Device/%.o Drivers/USBDevice-master/Device/%.su: ../Drivers/USBDevice-master/Device/%.c Drivers/USBDevice-master/Device/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F411xE -c -I../Core/Inc -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/LED_Controller" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/Joystick" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/RotaryEncoder" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/ButtonSwitch" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/Controller_Config" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/Serial_Comm" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/XPD_USB" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Class/HID" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Class/CDC" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Class/DFU" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Class/MSC" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Include/private" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/PDs/STM32_XPD" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Include" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Device" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Drivers-2f-USBDevice-2d-master-2f-Device

clean-Drivers-2f-USBDevice-2d-master-2f-Device:
	-$(RM) ./Drivers/USBDevice-master/Device/usbd.d ./Drivers/USBDevice-master/Device/usbd.o ./Drivers/USBDevice-master/Device/usbd.su ./Drivers/USBDevice-master/Device/usbd_ctrl.d ./Drivers/USBDevice-master/Device/usbd_ctrl.o ./Drivers/USBDevice-master/Device/usbd_ctrl.su ./Drivers/USBDevice-master/Device/usbd_desc.d ./Drivers/USBDevice-master/Device/usbd_desc.o ./Drivers/USBDevice-master/Device/usbd_desc.su ./Drivers/USBDevice-master/Device/usbd_ep.d ./Drivers/USBDevice-master/Device/usbd_ep.o ./Drivers/USBDevice-master/Device/usbd_ep.su ./Drivers/USBDevice-master/Device/usbd_if.d ./Drivers/USBDevice-master/Device/usbd_if.o ./Drivers/USBDevice-master/Device/usbd_if.su ./Drivers/USBDevice-master/Device/usbd_microsoft_os.d ./Drivers/USBDevice-master/Device/usbd_microsoft_os.o ./Drivers/USBDevice-master/Device/usbd_microsoft_os.su ./Drivers/USBDevice-master/Device/usbd_utils.d ./Drivers/USBDevice-master/Device/usbd_utils.o ./Drivers/USBDevice-master/Device/usbd_utils.su

.PHONY: clean-Drivers-2f-USBDevice-2d-master-2f-Device

