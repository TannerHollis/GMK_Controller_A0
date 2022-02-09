################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (9-2020-q2-update)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Hardware_Libraries/Joystick/Joystick.c 

OBJS += \
./Hardware_Libraries/Joystick/Joystick.o 

C_DEPS += \
./Hardware_Libraries/Joystick/Joystick.d 


# Each subdirectory must supply rules for building sources it contributes
Hardware_Libraries/Joystick/%.o: ../Hardware_Libraries/Joystick/%.c Hardware_Libraries/Joystick/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F411xE -c -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Hardware_Libraries/ButtonSwitch" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Hardware_Libraries/Joystick" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Hardware_Libraries/RotaryEncoder" -I../Core/Inc -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Core/Controller_Config" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Core/Serial_Comm" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/XPD_USB" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Class/DFU" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Class/MSC" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Include/private" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/PDs/STM32_XPD" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Include" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Device" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Class/CDC" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/USBDevice-master/Class/HID" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Hardware_Libraries-2f-Joystick

clean-Hardware_Libraries-2f-Joystick:
	-$(RM) ./Hardware_Libraries/Joystick/Joystick.d ./Hardware_Libraries/Joystick/Joystick.o

.PHONY: clean-Hardware_Libraries-2f-Joystick

