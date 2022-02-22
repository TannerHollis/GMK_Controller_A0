################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (9-2020-q2-update)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/USBDevice-master/Class/DFU/usbd_dfu.c 

OBJS += \
./Drivers/USBDevice-master/Class/DFU/usbd_dfu.o 

C_DEPS += \
./Drivers/USBDevice-master/Class/DFU/usbd_dfu.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/USBDevice-master/Class/DFU/%.o: ../Drivers/USBDevice-master/Class/DFU/%.c Drivers/USBDevice-master/Class/DFU/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F411xE -c -I../Core/Inc -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/LED_Controller" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/Joystick" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/RotaryEncoder" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/ButtonSwitch" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/Controller_Config" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/Serial_Comm" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/XPD_USB" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/USBDevice-master/Class/HID" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/USBDevice-master/Class/CDC" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/USBDevice-master/Class/DFU" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/USBDevice-master/Class/MSC" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/USBDevice-master/Include/private" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/USBDevice-master/PDs/STM32_XPD" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/USBDevice-master/Include" -I"C:/Users/thollis/Google Drive/Water_Valve_Sensor/GMK_Controller_A0/Drivers/USBDevice-master/Device" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Drivers-2f-USBDevice-2d-master-2f-Class-2f-DFU

clean-Drivers-2f-USBDevice-2d-master-2f-Class-2f-DFU:
	-$(RM) ./Drivers/USBDevice-master/Class/DFU/usbd_dfu.d ./Drivers/USBDevice-master/Class/DFU/usbd_dfu.o

.PHONY: clean-Drivers-2f-USBDevice-2d-master-2f-Class-2f-DFU

