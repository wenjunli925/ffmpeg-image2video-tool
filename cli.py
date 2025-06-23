import argparse
import os
from converter import convert_sequence_to_video

def main():
    parser = argparse.ArgumentParser(description="Convert image sequence to video")
    parser.add_argument("--input", required=True, help="Input pattern (e.g. img_%04d.png)")
    parser.add_argument("--output", help="Output video file (default: output.mp4 in same folder)")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second")

    args = parser.parse_args()

    if args.output:
        output_path = args.output
    else:
        input_folder = os.path.dirname(args.input)
        output_path = os.path.join(input_folder, "output.mp4") if input_folder else "output.mp4"

    success, error = convert_sequence_to_video(args.input, output_path, args.fps)

    if success:
        print(f"Video created successfully: {output_path}")
    else:
        print("Error:", error)

if __name__ == "__main__":
    main()
