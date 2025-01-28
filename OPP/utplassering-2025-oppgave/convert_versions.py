import os
import yaml
import sys

def check_consistency(data, config_contents):
    issues = []
    for device_name, device_info in data.items():
        if 'SerialNrs' in device_info:
            for serial in device_info['SerialNrs']:
                # Søke file ellers mappe med SerialNr
                if not any(str(serial) in item for item in config_contents):
                    issues.append(f"Mangler konfigurasjon for SerialNr: {serial} i mappen 'config'")
    return issues

def build_new_structure(data):
    new_structure = {}
    for device_name, device_info in data.items():
        version = device_info.get('Version')
        if 'SerialNrs' in device_info:
            for serial in device_info['SerialNrs']:
                panel_name = f"BridgeControlPanel{serial}"
                
                if panel_name not in new_structure:
                    new_structure[panel_name] = {'SerialNr': serial}
                
                # Legg til informasjon om versjon
                if 'MPS179' in device_name:
                    new_structure[panel_name].setdefault('MPS179', {})['Version'] = version
                elif 'MPS174' in device_name:
                    new_structure[panel_name].setdefault('MPS174', {})['Version'] = version
                elif 'BridgePanelDisplay' in device_name:
                    new_structure[panel_name].setdefault('MPS179_Display', {})['Version'] = version
    return new_structure

def convert_yaml(input_folder):
    try:
        config_folder = os.path.join(input_folder, 'config')
        yaml_file_path = os.path.join(config_folder, 'versions.yaml')
        
        if not os.path.exists(yaml_file_path):
            print(f"Filen 'versions.yaml' ble ikke funnet i mappen: {yaml_file_path}")
            return

        # Les inn original YAML-fil
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)

        # Få helle filler fra mappe config
        config_contents = os.listdir(config_folder)

        # Sjekke for konsistence
        issues = check_consistency(data, config_contents)
        if issues:
            print("Inkonsekvent data funnet:")
            for issue in issues:
                print(f" - {issue}")
        else:
            print("Versions.yaml og config-mappen er konsistent.")

        # Lage ny struktor
        new_structure = build_new_structure(data)

        # Lagre struktor
        output_file_path = os.path.join(input_folder, 'converted_versions.yaml')
        with open(output_file_path, 'w') as file:
            yaml.dump(new_structure, file, default_flow_style=False, allow_unicode=True)
        
        print(f"Den nye YAML-strukturen er lagret til: {output_file_path}")
    
    except Exception as e:
        print(f"Det oppstod en feil: {e}")

# Kjør på
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Bruk: python script.py <mappenavn>")
        sys.exit(1)

    input_folder = sys.argv[1]
    convert_yaml(input_folder)
