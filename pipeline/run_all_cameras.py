import os

videos = [

    # STORE 1

    r"data/Store 1/CAM 1 - zone.mp4",
    r"data/Store 1/CAM 2 - zone.mp4",
    r"data/Store 1/CAM 3 - entry.mp4",
    r"data/Store 1/CAM 5 - billing.mp4",

    # STORE 2

    r"data/Store 2/entry 1.mp4",
    r"data/Store 2/entry 2.mp4",
    r"data/Store 2/billing_area.mp4",
    r"data/Store 2/zone.mp4"
]

for video in videos:

    print(f"\nProcessing {video}")

    os.system(
        f'python pipeline/event_engine.py "{video}"'
    )

print("\nFinished Processing All Stores")