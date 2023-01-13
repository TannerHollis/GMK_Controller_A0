using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace GMK_Driver_NET
{
    public class ConfigAssociation
    {
        public string serialNumber { get; set; }
        public List<string> configFiles { get; set; }
        public string defaultConfigFile { get; set; }
    }

    public class DeviceAssociations
    {
        public List<ConfigAssociation> associations = new List<ConfigAssociation>();

        public static DeviceAssociations Load()
        {
            string jsonString = File.ReadAllText("deviceAssociations.json");
            return JsonSerializer.Deserialize<DeviceAssociations>(jsonString);
        }

        public void Save()
        {
            JsonSerializerOptions options = new JsonSerializerOptions();
            options.WriteIndented = true;

            string jsonString = JsonSerializer.Serialize<DeviceAssociations>(this, options);
            File.WriteAllText("deviceAssociations.json", jsonString);
        }

        public ConfigAssociation LookupSerialNumber(string serialNumber)
        {
            foreach(ConfigAssociation association in associations)
            {
                if(association.serialNumber.Equals(serialNumber))
                {
                    return association;
                }
            }
            return null;
        }

        public void AddNewDevice(string serialNumber)
        {
            ConfigAssociation configAssociation = new ConfigAssociation();
            configAssociation.serialNumber = serialNumber;
            associations.Add(configAssociation);
            Save();
        }

        public void AddConfiguration(string serialNumber, DeviceConfig config, bool setDefault)
        {
            ConfigAssociation configAssociation = LookupSerialNumber(serialNumber);

            string file = "Configs\\" + config.name + ".json";

            config.ToFile(file);
            configAssociation.configFiles.Add(file);
            
            if(configAssociation.defaultConfigFile == null || setDefault)
            {
                configAssociation.defaultConfigFile = file;
            }
            Save();
        }
    }
}
