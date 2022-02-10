################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (9-2020-q2-update)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/hal_usb.c \
../Core/Src/main.c \
../Core/Src/stm32f4xx_hal_msp.c \
../Core/Src/stm32f4xx_it.c \
../Core/Src/syscalls.c \
../Core/Src/sysmem.c \
../Core/Src/system_stm32f4xx.c \
../Core/Src/usb_device.c 

OBJS += \
./Core/Src/hal_usb.o \
./Core/Src/main.o \
./Core/Src/stm32f4xx_hal_msp.o \
./Core/Src/stm32f4xx_it.o \
./Core/Src/syscalls.o \
./Core/Src/sysmem.o \
./Core/Src/system_stm32f4xx.o \
./Core/Src/usb_device.o 

C_DEPS += \
./Core/Src/hal_usb.d \
./Core/Src/main.d \
./Core/Src/stm32f4xx_hal_msp.d \
./Core/Src/stm32f4xx_it.d \
./Core/Src/syscalls.d \
./Core/Src/sysmem.d \
./Core/Src/system_stm32f4xx.d \
./Core/Src/usb_device.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/%.o: ../Core/Src/%.c Core/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F411xE -c -I../Core/Inc -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/Joystick" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/RotaryEncoder" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/ButtonSwitch" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/Controller_Config" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/Serial_Comm" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/XPD_USB" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Class/HID" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Class/CDC" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Class/DFU" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Class/MSC" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Include/private" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/PDs/STM32_XPD" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Include" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Drivers/USBDevice-master/Device" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src

clean-Core-2f-Src:
	-$(RM) ./Core/Src/hal_usb.d ./Core/Src/hal_usb.o ./Core/Src/main.d ./Core/Src/main.o ./Core/Src/stm32f4xx_hal_msp.d ./Core/Src/stm32f4xx_hal_msp.o ./Core/Src/stm32f4xx_it.d ./Core/Src/stm32f4xx_it.o ./Core/Src/syscalls.d ./Core/Src/syscalls.o ./Core/Src/sysmem.d ./Core/Src/sysmem.o ./Core/Src/system_stm32f4xx.d ./Core/Src/system_stm32f4xx.o ./Core/Src/usb_device.d ./Core/Src/usb_device.o

.PHONY: clean-Core-2f-Src

