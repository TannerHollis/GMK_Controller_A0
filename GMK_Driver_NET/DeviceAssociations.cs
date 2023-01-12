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
        public string defaultConfig { get; set; }
    }

    public class DeviceAssociations
    {
        public List<ConfigAssociation> associations = new List<ConfigAssociation>();

        public static DeviceAssociations Load()
        {
            string jsonString = File.ReadAllText("deviceAssociations.json");
            return JsonSerializer.Deserialize<DeviceAssociations>(jsonString);
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
    }
}
