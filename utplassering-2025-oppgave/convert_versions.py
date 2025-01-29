import os
import yaml
import sys

def check_consistency(data, config_folder):
    if not os.path.exists(config_folder):
        print(f"Konfigurasjonsmappen finnes ikke: {config_folder}")
        return ["Konfigurasjonsmappen mangler."]

    config_contents = set(os.listdir(config_folder))
    issues = []

    for device_name, device_info in data.items():
        if 'SerialNrs' in device_info:
            for serial in device_info['SerialNrs']:
                if not any(str(serial) in item for item in config_contents):
                    issues.append(f"Mangler konfigurasjon for SerialNr: {serial} i mappen 'config'")
    
    return issues

def build_new_structure(data):
    new_structure = {}

    for thruster_id in range(1, 10):
        thruster_key = f"Thruster0{thruster_id}"
        if thruster_key not in data:
            print(f"Vi hopper over {thruster_key}, siden den ikke er i dataene.")
            continue

        device_info = data[thruster_key]
        
        mps_179_panel = device_info.get('MPS179_BridgePanel', {})
        mps_179_display = device_info.get('MPS179_BridgePanelDisplay', {})
        mps_174_panel = device_info.get('MPS174_BridgePanel', {})

        mps_179_version = mps_179_panel.get('Version')
        mps_179_display_version = mps_179_display.get('Version')
        mps_174_version = mps_174_panel.get('Version')

        if 'SerialNrs' in mps_179_panel:
            for serial in mps_179_panel['SerialNrs']:
                panel_name = f"BridgeControlPanel{serial}"
                
                if panel_name not in new_structure:
                    new_structure[panel_name] = {'SerialNr': serial}

                if mps_179_version:
                    new_structure[panel_name].setdefault('MPS179', {})['Version'] = mps_179_version
                if mps_179_display_version:
                    new_structure[panel_name].setdefault('MPS179_Display', {})['Version'] = mps_179_display_version
                if mps_174_version:
                    new_structure[panel_name].setdefault('MPS174', {})['Version'] = mps_174_version

        print(f"Behandlet {thruster_key}: {new_structure}")

    return new_structure

def convert_yaml(input_folder):
    try:
        yaml_file_path = os.path.join(input_folder, 'versions.yaml')
        config_folder = os.path.join(input_folder, 'config')
        
        if not os.path.exists(yaml_file_path):
            print(f"Filen 'versions.yaml' ble ikke funnet i mappen: {yaml_file_path}")
            return

        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)

        issues = check_consistency(data, config_folder)
        if issues:
            print("Inkonsekvent data funnet:")
            for issue in issues:
                print(f" - {issue}")
        else:
            print("Versions.yaml og config-mappen er konsistent.")

        new_structure = build_new_structure(data)

        output_file_path = os.path.join(input_folder, 'converted_versions.yaml')
        with open(output_file_path, 'w') as file:
            yaml.dump(new_structure, file, default_flow_style=False, allow_unicode=True)
        
        print(f"Den nye YAML-strukturen er lagret til: {output_file_path}")
    
    except Exception as e:
        print(f"Det oppstod en feil: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Bruk: python script.py <mappenavn>")
        sys.exit(1)

    input_folder = sys.argv[1]
    convert_yaml(input_folder)