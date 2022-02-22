################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (9-2020-q2-update)
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include Drivers/XPD_USB/subdir.mk
-include Drivers/USBDevice-master/Device/subdir.mk
-include Drivers/USBDevice-master/Class/MSC/subdir.mk
-include Drivers/USBDevice-master/Class/HID/subdir.mk
-include Drivers/USBDevice-master/Class/DFU/subdir.mk
-include Drivers/USBDevice-master/Class/CDC/subdir.mk
-include Drivers/Serial_Comm/subdir.mk
-include Drivers/STM32F4xx_HAL_Driver/Src/subdir.mk
-include Drivers/RotaryEncoder/subdir.mk
-include Drivers/LED_Controller/subdir.mk
-include Drivers/Joystick/subdir.mk
-include Drivers/Controller_Config/subdir.mk
-include Drivers/ButtonSwitch/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := GMK_Controller_A0
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
GMK_Controller_A0.elf \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
GMK_Controller_A0.list \

OBJCOPY_BIN += \
GMK_Controller_A0.bin \


# All Target
all: main-build

# Main-build Target
main-build: GMK_Controller_A0.elf secondary-outputs

# Tool invocations
GMK_Controller_A0.elf: $(OBJS) $(USER_OBJS) C:\Users\thollis\Google\ Drive\Water_Valve_Sensor\GMK_Controller_A0\STM32F411CCUX_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-gcc -o "GMK_Controller_A0.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m4 -T"C:\Users\thollis\Google Drive\Water_Valve_Sensor\GMK_Controller_A0\STM32F411CCUX_FLASH.ld" --specs=nosys.specs -Wl,-Map="GMK_Controller_A0.map" -Wl,--gc-sections -static --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

GMK_Controller_A0.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "GMK_Controller_A0.list"
	@echo 'Finished building: $@'
	@echo ' '

GMK_Controller_A0.bin: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objcopy  -O binary $(EXECUTABLES) "GMK_Controller_A0.bin"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) GMK_Controller_A0.bin GMK_Controller_A0.elf GMK_Controller_A0.list default.size.stdout
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST) $(OBJCOPY_BIN)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
