import os
import yaml
import sys

def convert_yaml(input_folder):
    config_folder = os.path.join(input_folder, 'config')
    yaml_file_path = os.path.join(config_folder, 'versions.yaml')
    
    if not os.path.exists(yaml_file_path):
        print(f"Filen 'versions.yaml' ble ikke funnet i mappen: {yaml_file_path}")
        return

    # Les inn original YAML-fil
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Ny struktur som vi skal bygge
    new_structure = {}

    # Iterer gjennom den opprinnelige strukturen og omorganiser informasjonen
    for device_name, device_info in data.items():
        # For å hente ut versjonsinformasjon
        version = device_info.get('Version')
        if 'SerialNrs' in device_info:
            # Hvis det finnes en liste med SerialNrs, koble til hver serialnummer
            for serial in device_info['SerialNrs']:
                # Lag en ny nøkkel for hvert serialnummer
                panel_name = f"BridgeControlPanel{serial}"
                
                # Opprett en ny struktur for panelnavnet
                if panel_name not in new_structure:
                    new_structure[panel_name] = {'SerialNr': serial}

                # Legg til informasjon om enheten (MPS174, MPS179 osv.)
                if 'MPS179' in device_name:
                    new_structure[panel_name]['MPS179'] = {'Version': version}
                elif 'MPS174' in device_name:
                    new_structure[panel_name]['MPS174'] = {'Version': version}
                elif 'BridgePanelDisplay' in device_name:
                    new_structure[panel_name]['MPS179_Display'] = {'Version': version}

    # Lagre ny struktur til YAML-fil
    output_file_path = os.path.join(input_folder, 'converted_versions.yaml')
    with open(output_file_path, 'w') as file:
        yaml.dump(new_structure, file, default_flow_style=False, allow_unicode=True)
    
    print(f"Den nye YAML-strukturen er lagret til: {output_file_path}")

#Kjør på
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Bruk: python script.py <mappenavn>")
        sys.exit(1)

    input_folder = sys.argv[1]
    convert_yaml(input_folder)