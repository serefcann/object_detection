import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Göreli klasör yollarını tam yola çevir
    cfg["paths"]["input_dir"] = os.path.join(BASE_DIR, cfg["paths"]["input_dir"])
    cfg["paths"]["output_dir"] = os.path.join(BASE_DIR, cfg["paths"]["output_dir"])
    
    # Klasörler yoksa oluştur
    os.makedirs(cfg["paths"]["input_dir"], exist_ok=True)
    os.makedirs(cfg["paths"]["output_dir"], exist_ok=True)

    # Varsayılan dosya yollarını tam yola çevir
    cfg["paths"]["default_video_input"] = os.path.join(
        cfg["paths"]["input_dir"], cfg["paths"]["default_video_input"]
    )
    cfg["paths"]["default_video_output"] = os.path.join(
        cfg["paths"]["output_dir"], cfg["paths"]["default_video_output"]
    )
    cfg["paths"]["default_image_input"] = os.path.join(
        cfg["paths"]["input_dir"], cfg["paths"]["default_image_input"]
    )
    cfg["paths"]["default_image_output"] = os.path.join(
        cfg["paths"]["output_dir"], cfg["paths"]["default_image_output"]
    )

    return cfg


# Modül import edilir edilmez config'i bir kere yükle
CONFIG = load_config()