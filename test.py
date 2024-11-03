import json
import toml
import yaml
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import button_dialog, input_dialog
from prompt_toolkit.styles import Style

# Define your custom style
style = Style.from_dict({
    'dialog': 'bg:#000000 fg:#ffffff',  # Black background, white foreground
    'button': 'bg:#000000 fg:#ffffff',
    'button.focused': 'bg:#0080ff fg:#ffffff',
})

# Configuration structure
config = {
    "prefix": "",
    "token": "",
    "logging_channel_id": "",
    "rcon_host": "",
    "rcon_port": "",
    "rcon_password": "",
    "bot_owner_id": "",
    "rcon_prefix": "",
    "raw_rcon_prefix": "",
    "server_name": "",
    "server_start_command": ""
}

def configure_options():
    global config
    for key in config.keys():
        user_input = input_dialog(
            title="Configure Options",
            text=f"Enter value for '{key}':",
            style=style
        ).run()

        if user_input is not None:
            config[key] = user_input

def save_configuration():
    file_type = button_dialog(
        title="Save Configuration",
        text="Choose a file format to save the configuration:",
        buttons=[
            ("JSON", "json"),
            ("TOML", "toml"),
            ("YAML", "yml"),
            ("Cancel", "cancel"),
        ],
        style=style
    ).run()

    if file_type == "cancel":
        print("Configuration not saved.")
        return

    file_name = prompt("Enter the filename (without extension): ", style=style)
    if file_name:
        file_path = f"{file_name}.{file_type}"
        try:
            if file_type == "json":
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=4)
            elif file_type == "toml":
                with open(file_path, 'w') as f:
                    toml.dump(config, f)
            elif file_type == "yml":
                with open(file_path, 'w') as f:
                    yaml.dump(config, f)

            print(f"Configuration saved to {file_path}")
        except Exception as e:
            print(f"Failed to save configuration: {e}")

def main():
    configure_options()
    save_configuration()

if __name__ == "__main__":
    main()

