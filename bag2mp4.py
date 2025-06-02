import argparse

import cv2

import rosbag

from cv_bridge import CvBridge

import os



def create_video_writer(output_dir, topic, width, height, fps=15):

    """指定したディレクトリとトピックで動画ライターを作成"""

    # 動画ファイル名の作成

    filename = os.path.join(output_dir, f"{topic.replace('/', '_')}.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4形式

    return cv2.VideoWriter(filename, fourcc, fps, (width, height))



def convert_bag_to_videos(bag_file, output_dir):

    bridge = CvBridge()

    video_writers = {}



    # 出力ディレクトリの作成

    if not os.path.exists(output_dir):

        os.makedirs(output_dir)



    # bagファイルを開く

    with rosbag.Bag(bag_file, 'r') as bag:

        for topic, msg, t in bag.read_messages():

            # Image型のトピックのみ動画に変換

            if msg._type == 'sensor_msgs/Image':

                # cv2に変換

                try:

                    cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")

                except Exception as e:

                    print(f"Error converting message for topic {topic}: {e}")

                    continue



                height, width = cv_image.shape[:2]



                # トピックごとにVideoWriterを作成

                if topic not in video_writers:

                    video_writers[topic] = create_video_writer(output_dir, topic, width, height)



                # フレームを書き込み

                video_writers[topic].write(cv_image)



    # 各VideoWriterを解放

    for writer in video_writers.values():

        writer.release()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert ROS bag topics to video files.")

    parser.add_argument("bag_file", type=str, help="Path to the ROS bag file.")

    parser.add_argument("output_dir", type=str, help="Directory to save the output videos.")

    args = parser.parse_args()



    convert_bag_to_videos(args.bag_file, args.output_dir)


