ENTRY_LINE = 500

def get_direction(prev_y,current_y):

    if prev_y < ENTRY_LINE and current_y > ENTRY_LINE:
        return "ENTRY"

    if prev_y > ENTRY_LINE and current_y < ENTRY_LINE:
        return "EXIT"

    return None
