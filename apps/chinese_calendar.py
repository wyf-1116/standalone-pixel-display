import datetime
from lunarcalendar import Converter, Solar, Lunar

# 3x5 Bitmaps for digits and characters
# Format: List of 5 rows, each row is a 3-bit integer (left to right)
BITMAPS = {
    "0": [0b111, 0b101, 0b101, 0b101, 0b111],
    "1": [0b010, 0b110, 0b010, 0b010, 0b111],
    "2": [0b111, 0b001, 0b111, 0b100, 0b111],
    "3": [0b111, 0b001, 0b011, 0b001, 0b111],
    "4": [0b101, 0b101, 0b111, 0b001, 0b001],
    "5": [0b111, 0b100, 0b111, 0b001, 0b111],
    "6": [0b111, 0b100, 0b111, 0b101, 0b111],
    "7": [0b111, 0b001, 0b010, 0b100, 0b100],
    "8": [0b111, 0b101, 0b111, 0b101, 0b111],
    "9": [0b111, 0b101, 0b111, 0b001, 0b111],
    "月": [0b111, 0b101, 0b111, 0b101, 0b101],
    "日": [0b111, 0b101, 0b111, 0b101, 0b111],
}

def get_lunar_data():
    """Fetches lunar date and returns components."""
    now = datetime.datetime.now()
    solar = Solar(now.year, now.month, now.day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar

def get_draw_commands(lunar):
    """Generates AWTRIX draw commands for "MM月DD日" format using compact 3x5 bitmaps."""
    commands = []
    
    month_str = str(lunar.month)
    day_str = str(lunar.day)
    
    draw_sequence = []
    for char in month_str:
        draw_sequence.append(char)
    draw_sequence.append("月")
    for char in day_str:
        draw_sequence.append(char)
    draw_sequence.append("日")
    
    char_width = 3
    char_height = 5
    num_elements = len(draw_sequence)
    
    # Total width: elements * 3px + (elements-1) * 1px gap
    total_width = (num_elements * char_width) + (num_elements - 1)
    
    # Center horizontally and vertically (3px top/bottom padding for 8px screen)
    start_x = max(0, (32 - total_width) // 2)
    start_y = 1 # 1px padding from top to leave space
    
    x_offset = start_x
    for char in draw_sequence:
        bitmap = BITMAPS.get(char)
        if bitmap:
            # Color: Red (#FF0000) for Chinese labels, White (#FFFFFF) for numbers
            color = "#FF0000" if char in ["月", "日"] else "#FFFFFF"
            for r in range(char_height):
                row_bits = bitmap[r]
                for c in range(char_width):
                    if (row_bits >> (2 - c)) & 1:
                        commands.append({"dp": [x_offset + c, start_y + r, color]})
        x_offset += 4 # 3px width + 1px gap
                
    return commands

def run():
    """Main entry point for the Chinese Calendar app."""
    try:
        lunar = get_lunar_data()
        draw_commands = get_draw_commands(lunar)
        
        payload = {
            "name": "chinese_calendar",
            "draw": draw_commands
        }
        return payload
    except Exception as e:
        print(f"Error in Chinese Calendar app: {e}")
        return None

if __name__ == "__main__":
    # Test locally
    print(run())
