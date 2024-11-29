import re
from typing import Dict, Union, List, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class StorageDevice:
    capacity: int  # In GB
    type: str     # SSD, HDD, NVMe
    interface: Optional[str] = None  # SATA, M.2, etc.

class HardwareSpecParser:
    def __init__(self):
        # Like a master Jedi's knowledge, we store our patterns
        self.BRANDS = {
            'dell', 'hp', 'lenovo', 'asus', 'microsoft', 'acer', 'fujitsu', 
            'cisco', 'alphapc', 'toshiba', 'medion', 'lexmark', 'benq', 'apple',
            'kyocera', 'nec', 'samsung', 'sony', 'lg', 'msi', 'huawei'
        }

        self.CATEGORIES = {
            'laptop': ['ноутбук', 'laptop', 'notebook', 'thinkpad', 'latitude', 'zbook', 
                      'elitebook', 'probook', 'macbook', 'inspiron', 'vostro'],
            'server': ['server', 'сервер', 'poweredge', 'proliant', 'primergy', 'bladecenter'],
            'desktop': ['desktop', 'компьютер', 'системний', 'tower', 'optiplex', 'пк', 
                       'workstation', 'esprimo', 'thinkcentre'],
            'monitor': ['monitor', 'монітор', 'дисплей', 'lcd', 'led'],
            'printer': ['printer', 'принтер', 'ecosys', 'laserjet', 'мфу'],
            'smartphone': ['phone', 'смартфон', 'iphone'],
            'tablet': ['tablet', 'планшет', 'ipad']
        }

        self.PROCESSOR_FAMILIES = {
            'intel': ['core i3', 'core i5', 'core i7', 'core i9', 'xeon', 'celeron', 'pentium'],
            'amd': ['ryzen', 'epyc', 'athlon', 'a4', 'a6', 'a8', 'a10']
        }

        self.STORAGE_MULTIPLIERS = {
            'tb': 1000,
            'gb': 1,
            'mb': 0.001
        }

    def _normalize_storage_size(self, size: str, unit: str) -> int:
        """Convert storage size to GB"""
        try:
            size_num = float(size.replace(',', '.'))
            unit = unit.lower()
            for key, multiplier in self.STORAGE_MULTIPLIERS.items():
                if key in unit:
                    return int(size_num * multiplier)
            return int(size_num)  # assume GB if no unit specified
        except (ValueError, TypeError):
            return 0

    def _extract_brand_model(self, text: str) -> tuple:
        """Extract brand and model from text"""
        text = text.lower()
        found_brand = None

        # First try to find brand
        for brand in self.BRANDS:
            if brand in text:
                found_brand = brand.capitalize()
                # Try to find model after brand
                brand_pos = text.find(brand)
                after_brand = text[brand_pos + len(brand):].strip()

                # Common model patterns
                model_patterns = [
                    r'^[a-zA-Z0-9-]+\s*[a-zA-Z0-9-]+',  # Basic alphanumeric
                    r'(thinkpad|latitude|elitebook|probook|optiplex)\s*[a-zA-Z0-9-]+',
                    r'(poweredge|proliant)\s*[a-zA-Z0-9-]+',
                ]

                for pattern in model_patterns:
                    model_match = re.search(pattern, after_brand, re.IGNORECASE)
                    if model_match:
                        return found_brand, model_match.group(0).strip()

                # If no pattern matched, take next word
                next_words = re.search(r'^[a-zA-Z0-9-]+', after_brand)
                if next_words:
                    return found_brand, next_words.group(0).strip()

                break

        return found_brand, None

    def _extract_screen_info(self, text: str) -> dict:
        """Extract screen size and properties"""
        screen_info = {}

        # Screen size patterns
        size_patterns = [
            r'(\d{1,2}[.,]?\d*)[\s-]?(inch|"|inches|\'|\s?zoll)',
            r'(\d{1,2}[.,]?\d*)["\']',
            r'(\d{1,2}[.,]?\d*)[-\s]?(?:гб|gb|g|"|дюйм)'
        ]

        for pattern in size_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                size = match.group(1).replace(',', '.')
                screen_info['screen_size'] = f"{size}\""
                break

        # Resolution patterns
        resolutions = {
            'UHD': [r'uhd', r'3840x2160', r'4k'],
            'QHD': [r'qhd', r'2560x1440', r'2k'],
            'FHD': [r'fhd', r'1920x1080', r'1920\s*x\s*1080'],
            'HD+': [r'hd\+', r'1600x900'],
            'HD': [r'(?<!f)(?<!q)hd(?!\+)', r'1366x768']
        }

        for res_name, patterns in resolutions.items():
            if any(re.search(p, text, re.IGNORECASE) for p in patterns):
                screen_info['resolution'] = res_name
                break

        # Panel type
        panel_types = {
            'IPS': [r'\bips\b'],
            'TN': [r'\btn\b', r'tn\+film'],
            'VA': [r'\bva\b'],
            'PLS': [r'\bpls\b'],
            'OLED': [r'\boled\b'],
            'PVA': [r'\bpva\b']
        }

        for panel_name, patterns in panel_types.items():
            if any(re.search(p, text, re.IGNORECASE) for p in patterns):
                screen_info['panel_type'] = panel_name
                break

        return screen_info

    def _extract_processor(self, text: str) -> dict:
        """Extract processor information"""
        processor_info = {}

        # Complex processor patterns
        patterns = [
            # Intel modern
            r'(intel)?\s*(core\s*[iI][3579]-[0-9]{4,}[A-Z]*)',
            # Intel Xeon
            r'(intel)?\s*(xeon\s*(?:gold|silver|bronze|platinum)?\s*[A-Z0-9-]+)',
            # AMD Ryzen
            r'(amd)?\s*(ryzen\s*[3579])\s*([0-9]{4}[A-Z]*)',
            # AMD Others
            r'(amd)?\s*(a[468]|fx)-?([0-9]+)',
            # Basic Intel/AMD
            r'(intel|amd)\s*([a-zA-Z0-9-]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Combine all non-None groups
                parts = [p for p in match.groups() if p]
                processor_info['processor'] = ' '.join(parts).strip()

                # Try to extract clock speed
                clock_match = re.search(r'(\d+[.,]?\d*)\s*(?:ghz|ггц)', text, re.IGNORECASE)
                if clock_match:
                    processor_info['clock_speed'] = f"{clock_match.group(1)} GHz"

                # Try to extract cores
                cores_match = re.search(r'(\d+)\s*(?:core|ядер|cores?)', text, re.IGNORECASE)
                if cores_match:
                    processor_info['cores'] = cores_match.group(1)

                break

        return processor_info

    def _extract_memory(self, text: str) -> Optional[str]:
        """Extract RAM information"""
        patterns = [
            r'(\d+)\s*(?:gb|гб|g)\s*(?:ddr\d?)?\s*ram',
            r'(\d+)\s*(?:gb|гб|g)\s*(?:ddr\d?)',
            r'ram\s*(\d+)\s*(?:gb|гб|g)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)} GB"
        return None

    def _extract_storage(self, text: str) -> List[StorageDevice]:
        """Extract storage information"""
        storage_devices = []

        # Pattern for storage devices
        patterns = [
            # Format: size unit type
            r'(\d+(?:[.,]\d+)?)\s*(tb|gb|гб|тб)\s*(ssd|hdd|nvme|m\.2)?',
            # Format: type size unit
            r'(ssd|hdd|nvme|m\.2)?\s*(\d+(?:[.,]\d+)?)\s*(tb|gb|гб|тб)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()

                # Determine which group is which based on pattern
                if groups[0] and groups[0].lower() in ['ssd', 'hdd', 'nvme', 'm.2']:
                    # Type size unit pattern
                    size = groups[1]
                    unit = groups[2]
                    drive_type = groups[0]
                else:
                    # Size unit type pattern
                    size = groups[0]
                    unit = groups[1]
                    drive_type = groups[2] if groups[2] else 'HDD'  # Default to HDD if not specified

                # Normalize size to GB
                size_gb = self._normalize_storage_size(size, unit)

                # Determine storage type and interface
                if drive_type:
                    drive_type = drive_type.upper()
                    if drive_type == 'M.2':
                        storage_devices.append(StorageDevice(size_gb, 'SSD', 'M.2'))
                    elif drive_type == 'NVME':
                        storage_devices.append(StorageDevice(size_gb, 'SSD', 'NVMe'))
                    else:
                        storage_devices.append(StorageDevice(size_gb, drive_type))
                else:
                    storage_devices.append(StorageDevice(size_gb, 'HDD'))

        return storage_devices

    def _extract_gpu(self, text: str) -> Optional[str]:
        """Extract GPU information"""
        patterns = [
            r'(nvidia|amd)\s*(geforce|quadro|radeon)\s*([a-zA-Z0-9]+\s*[a-zA-Z0-9]*)\s*(\d+\s*gb)?',
            r'(intel)\s*(uhd|hd)\s*graphics\s*(\d+)?',
            r'(radeon|geforce)\s*([a-zA-Z0-9]+\s*[a-zA-Z0-9]*)\s*(\d+\s*gb)?'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Combine all non-None groups
                parts = [p for p in match.groups() if p]
                return ' '.join(parts).strip()
        return None

    def _extract_condition(self, text: str) -> Optional[str]:
        """Extract condition information"""
        conditions = {
            'New': [r'\bnew\b', r'новий'],
            'Used': [r'\bused\b', r'б[/\\]в', r'б/у', r'бв', r'бу', r'вживаний'],
            'Refurbished': [r'refurbished', r'ref', r'відновлений']
        }

        for condition, patterns in conditions.items():
            if any(re.search(p, text, re.IGNORECASE) for p in patterns):
                return condition
        return None

    def _extract_operating_system(self, text: str) -> Optional[str]:
        """Extract operating system information"""
        patterns = [
            (r'windows\s*(\d+)\s*(pro|home|enterprise)?', 'Windows'),
            (r'win\s*(\d+)\s*(pro|home|enterprise)?', 'Windows'),
            (r'w(\d+)\s*(pro|home|enterprise)?', 'Windows'),
            (r'macos|mac\s*os', 'MacOS'),
            (r'linux|ubuntu|debian|centos', 'Linux')
        ]

        for pattern, os_name in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if os_name == 'Windows':
                    version = match.group(1)
                    edition = match.group(2).capitalize() if match.group(2) else 'Pro'
                    return f"Windows {version} {edition}"
                return os_name
        return None

    def _determine_category(self, text: str) -> Optional[str]:
        """Determine device category"""
        text = text.lower()
        for category, keywords in self.CATEGORIES.items():
            if any(keyword.lower() in text for keyword in keywords):
                return category.capitalize()
        return None

    def parse(self, text: str) -> Dict[str, Any]:
        """Main parsing method"""
        # Initialize result dictionary
        result = {}

        # Extract brand and model
        brand, model = self._extract_brand_model(text)
        if brand:
            result['brand'] = brand
        if model:
            result['model'] = model

        # Extract category
        category = self._determine_category(text)
        if category:
            result['category'] = category

        # For display devices, extract screen information
        if category in ['Laptop', 'Monitor', 'Tablet']:
            screen_info = self._extract_screen_info(text)
            result.update(screen_info)

        # For computing devices, extract processor, memory, storage
        if category in ['Laptop', 'Desktop', 'Server']:
            # Processor
            processor_info = self._extract_processor(text)
            result.update(processor_info)

            # Memory
            ram = self._extract_memory(text)
            if ram:
                result['ram'] = ram

            # Storage
            storage_devices = self._extract_storage(text)


Items = [
    "Lenovo ThinkPad T470s i5-6300U 12GB 512GB SSD FHD WLAN BT Webcam Win 11 Pro",
    "Ноутбук HP ProBook 650 G1 Intel Core i5-4210M 8 GB RAM 320 GB HDD [15.6] Б/В",
    "Б/В Ноутбук HP EliteBook 8460P TN Intel Core i5 0 Гб 320 Гб HDD ( Клас B)",
    "Dell PowerEdge R740xd 28x 2,5 2x Gold 6248R 1536GB H740P 4x1,6TB SSD 12x2TB",
    "Cisco Switch Catalyst 3750X 48x 1GbE RJ45 2x PSU IP Services - WS-C3750X-48T-E"
]

HParser = HardwareSpecParser()
for xItem in Items:
    print(xItem)
    print(HParser.parse(xItem))
    print()

