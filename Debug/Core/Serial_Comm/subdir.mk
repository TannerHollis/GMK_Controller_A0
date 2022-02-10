################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (9-2020-q2-update)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Serial_Comm/Serial_Comm.c 

OBJS += \
./Core/Serial_Comm/Serial_Comm.o 

C_DEPS += \
./Core/Serial_Comm/Serial_Comm.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Serial_Comm/%.o: ../Core/Serial_Comm/%.c Core/Serial_Comm/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F411xE -c -I../Core/Inc -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Core/Controller_Config" -I"C:/Users/TannerGaming/STM32CubeIDE/workspace_1.3.0/GMK_Controller_A0/Core/Serial_Comm" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Serial_Comm

clean-Core-2f-Serial_Comm:
	-$(RM) ./Core/Serial_Comm/Serial_Comm.d ./Core/Serial_Comm/Serial_Comm.o

.PHONY: clean-Core-2f-Serial_Comm

