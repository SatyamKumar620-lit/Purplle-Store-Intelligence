from pipeline.zones import ZONES


def point_inside_zone(
    x,
    y,
    zone
):

    x1, y1, x2, y2 = zone

    return (
        x1 <= x <= x2
        and
        y1 <= y <= y2
    )


def get_zone_for_point(
    camera_id,
    x,
    y
):

    if camera_id not in ZONES:
        return None

    camera_zones = ZONES[camera_id]

    for zone_name, coords in camera_zones.items():

        if point_inside_zone(
            x,
            y,
            coords
        ):
            return zone_name

    return None